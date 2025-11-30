"""
StyliShi - Real-Time Fashion Recommender
Point your camera at any clothing → Get 10 visually similar items in <1 second
Built with CLIP + FAISS for EDISS portfolio
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
from pathlib import Path
import sys

# Add utils to path
sys.path.append(str(Path(__file__).parent))

from utils.embedder import FashionEmbedder
from utils.search import FashionSearchEngine


# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================

st.set_page_config(
    page_title="StyliShi - AI Fashion Recommender",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for stunning UI
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        padding-top: 1rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #888;
        margin-bottom: 2rem;
    }

    /* Result cards */
    .result-card {
        border-radius: 12px;
        padding: 10px;
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px solid #667eea30;
        transition: transform 0.2s;
        margin-bottom: 15px;
    }

    .result-card:hover {
        transform: translateY(-5px);
        border-color: #667eea;
    }

    /* Similarity badge */
    .similarity-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* Camera frame */
    .camera-frame {
        border: 3px solid #667eea;
        border-radius: 15px;
        padding: 10px;
        background: #00000010;
    }

    /* Stats box */
    .stats-box {
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }

    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sample image grid */
    .sample-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# INITIALIZE MODELS (with caching)
# ============================================================================

@st.cache_resource
def load_models():
    """Load CLIP embedder and FAISS search engine (cached)"""
    try:
        embedder = FashionEmbedder()
        search_engine = FashionSearchEngine()
        search_engine.load()
        return embedder, search_engine, None
    except Exception as e:
        return None, None, str(e)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def process_image_search(image, embedder, search_engine):
    """Process image and return similar items"""
    # Generate embedding
    start_time = time.time()
    embedding = embedder.embed_image(image)
    embed_time = time.time() - start_time

    # Search similar items
    start_time = time.time()
    results = search_engine.search(embedding, k=10)
    search_time = time.time() - start_time

    return results, embed_time, search_time


def display_results(results, embed_time, search_time):
    """Display search results in beautiful grid"""
    st.markdown("---")

    # Stats
    total_time = (embed_time + search_time) * 1000
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚡ Total Time", f"{total_time:.0f} ms")
    with col2:
        st.metric("🧠 Embedding", f"{embed_time*1000:.0f} ms")
    with col3:
        st.metric("🔍 Search", f"{search_time*1000:.0f} ms")

    st.markdown("### 🎯 Top 10 Similar Items")

    # Display in 2 columns
    for i in range(0, len(results), 2):
        cols = st.columns(2)

        for j, col in enumerate(cols):
            if i + j < len(results):
                result = results[i + j]

                with col:
                    # Display image
                    img_path = Path(result['image_path'])
                    if img_path.exists():
                        st.image(
                            str(img_path),
                            use_container_width=True,
                            caption=f"#{result['rank']} - {result['similarity_pct']} match"
                        )

                        # Similarity badge
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: -10px;">
                            <span class="similarity-badge">
                                Match: {result['similarity_pct']}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning(f"Image not found: {img_path}")

                    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-title">👗 StyliShi</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Real-time fashion recommender powered by AI vision</p>',
        unsafe_allow_html=True
    )

    # Load models
    embedder, search_engine, error = load_models()

    if error:
        st.error(f"""
        ❌ **Models not loaded!**

        Error: {error}

        Please run the setup first:
        ```bash
        python download_dataset.py
        ```
        """)
        st.stop()

    # Show index stats
    stats = search_engine.get_stats()
    st.sidebar.markdown("### 📊 System Stats")
    st.sidebar.info(f"""
    **Index**: {stats['total_items']:,} items
    **Embedding**: {stats['embedding_dim']}D CLIP
    **Engine**: {stats['index_type']}
    """)

    # Mode selection
    st.sidebar.markdown("### 🎯 Search Mode")
    mode = st.sidebar.radio(
        "Choose input method:",
        ["📸 Live Camera", "🖼️ Upload Image", "🎨 Sample Images"],
        label_visibility="collapsed"
    )

    # ========================================================================
    # MODE 1: LIVE CAMERA
    # ========================================================================
    if mode == "📸 Live Camera":
        st.markdown("### 📸 Live Camera Feed")
        st.info("💡 Point your camera at any clothing item and click 'Capture & Search'")

        # Camera input
        camera_image = st.camera_input(
            "Camera",
            label_visibility="collapsed"
        )

        if camera_image:
            # Show captured image
            image = Image.open(camera_image).convert('RGB')

            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### 📷 Captured Image")
                st.image(image, use_container_width=True)

                if st.button("🔍 Search Similar Items", type="primary", use_container_width=True):
                    with st.spinner("🔮 Analyzing fashion style..."):
                        results, embed_time, search_time = process_image_search(
                            image, embedder, search_engine
                        )
                        st.session_state['results'] = results
                        st.session_state['embed_time'] = embed_time
                        st.session_state['search_time'] = search_time

            with col2:
                if 'results' in st.session_state:
                    display_results(
                        st.session_state['results'],
                        st.session_state['embed_time'],
                        st.session_state['search_time']
                    )

    # ========================================================================
    # MODE 2: UPLOAD IMAGE
    # ========================================================================
    elif mode == "🖼️ Upload Image":
        st.markdown("### 🖼️ Upload Fashion Image")

        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png'],
            label_visibility="collapsed"
        )

        if uploaded_file:
            image = Image.open(uploaded_file).convert('RGB')

            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### 📷 Your Image")
                st.image(image, use_container_width=True)

                if st.button("🔍 Find Similar Items", type="primary", use_container_width=True):
                    with st.spinner("🔮 Searching 50k+ items..."):
                        results, embed_time, search_time = process_image_search(
                            image, embedder, search_engine
                        )
                        st.session_state['results'] = results
                        st.session_state['embed_time'] = embed_time
                        st.session_state['search_time'] = search_time

            with col2:
                if 'results' in st.session_state:
                    display_results(
                        st.session_state['results'],
                        st.session_state['embed_time'],
                        st.session_state['search_time']
                    )

    # ========================================================================
    # MODE 3: SAMPLE IMAGES
    # ========================================================================
    else:
        st.markdown("### 🎨 Try Sample Fashion Items")

        # Get sample images
        sample_dir = Path("sample_images")
        sample_images = list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.png"))

        if len(sample_images) == 0:
            st.warning("No sample images found. Add some images to the `sample_images/` folder!")
        else:
            # Display sample images in grid
            cols = st.columns(5)
            selected_sample = None

            for idx, img_path in enumerate(sample_images[:10]):
                col_idx = idx % 5
                with cols[col_idx]:
                    st.image(str(img_path), use_container_width=True)
                    if st.button(f"Try this", key=f"sample_{idx}", use_container_width=True):
                        selected_sample = img_path

            if selected_sample:
                st.markdown("---")
                image = Image.open(selected_sample).convert('RGB')

                col1, col2 = st.columns([1, 2])

                with col1:
                    st.markdown("#### 📷 Selected Sample")
                    st.image(image, use_container_width=True)

                with col2:
                    with st.spinner("🔮 Finding similar items..."):
                        results, embed_time, search_time = process_image_search(
                            image, embedder, search_engine
                        )
                        display_results(results, embed_time, search_time)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 20px;">
        <p><b>StyliShi</b> - Real-time Fashion AI Recommender</p>
        <p>Built with CLIP + FAISS | Powered by Streamlit</p>
        <p style="font-size: 0.9rem;">
            <a href="https://github.com/ialisha64/stylishi" target="_blank">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
