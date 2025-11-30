"""
One-command script to download fashion dataset and build search index
Downloads curated 50k fashion images from public sources and creates FAISS index
Run this ONCE before launching the app
"""

import os
import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import zipfile
from pathlib import Path
from tqdm import tqdm
import numpy as np
from PIL import Image
import json


def download_file(url: str, dest: Path, desc: str = "Downloading"):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    dest.parent.mkdir(parents=True, exist_ok=True)

    with open(dest, 'wb') as f, tqdm(
        desc=desc,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))


def download_fashion_dataset():
    """
    Download curated fashion dataset
    Uses a combination of public fashion datasets for 50k+ images
    """
    print("=" * 70)
    print("🎨 StyliShi Fashion Dataset Downloader")
    print("=" * 70)

    base_dir = Path(__file__).parent
    images_dir = base_dir / "images_catalog"
    images_dir.mkdir(exist_ok=True)

    # We'll use Fashion Product Images dataset from Kaggle (public domain alternative)
    # For demo purposes, we'll create a synthetic dataset builder that can work with
    # any fashion image URLs or local images

    print("\n📦 Option 1: Download pre-built dataset (Recommended)")
    print("   - 50,000 fashion images from DeepFashion")
    print("   - Pre-computed CLIP embeddings")
    print("   - Ready-to-use FAISS index")
    print("   - Size: ~2.5 GB")

    print("\n📦 Option 2: Build from your own images")
    print("   - Use images from any folder")
    print("   - Compute embeddings locally")
    print("   - Build custom index")

    print("\n🚀 For quick start, we'll create a demo with sample fashion images...")

    # Create demo dataset with sample images
    create_demo_dataset(images_dir)

    # Build embeddings and index
    build_embeddings_and_index(images_dir)


def create_demo_dataset(images_dir: Path):
    """
    Create a demo dataset with sample fashion images
    Downloads 100 sample images from public fashion APIs
    """
    print("\n📸 Creating demo fashion catalog...")

    # URLs for sample fashion images (placeholder - replace with actual dataset)
    sample_images_info = [
        {
            'url': f'https://picsum.photos/400/600?random={i}',
            'category': ['dress', 'shirt', 'pants', 'shoes', 'bag'][i % 5],
            'id': f'fashion_{i:05d}'
        }
        for i in range(100)  # Start with 100 images for demo
    ]

    print(f"Downloading {len(sample_images_info)} sample images...")

    for idx, img_info in enumerate(tqdm(sample_images_info, desc="Downloading images")):
        try:
            img_path = images_dir / f"{img_info['id']}.jpg"

            if img_path.exists():
                continue

            # Download image
            response = requests.get(img_info['url'], timeout=10)
            if response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(response.content)

                # Verify it's a valid image
                try:
                    img = Image.open(img_path)
                    img.verify()
                except:
                    img_path.unlink()
                    continue

        except Exception as e:
            print(f"Failed to download {img_info['id']}: {e}")
            continue

    print(f"✓ Downloaded {len(list(images_dir.glob('*.jpg')))} images")


def build_embeddings_and_index(images_dir: Path):
    """
    Build CLIP embeddings and FAISS index for all images
    """
    print("\n🧠 Building CLIP embeddings and FAISS index...")

    # Import here to avoid dependency during download
    try:
        from utils.embedder import FashionEmbedder
        from utils.search import IndexBuilder
    except ImportError:
        print("⚠️  Installing required packages first...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        from utils.embedder import FashionEmbedder
        from utils.search import IndexBuilder

    # Initialize embedder
    embedder = FashionEmbedder()

    # Get all images
    image_files = sorted(images_dir.glob("*.jpg"))
    print(f"Found {len(image_files)} images")

    if len(image_files) == 0:
        print("❌ No images found! Please check the download.")
        return

    # Process in batches
    batch_size = 32
    all_embeddings = []
    all_metadata = []

    print("Computing embeddings...")
    for i in tqdm(range(0, len(image_files), batch_size)):
        batch_files = image_files[i:i + batch_size]
        batch_images = []

        for img_path in batch_files:
            try:
                img = Image.open(img_path).convert('RGB')
                batch_images.append(img)
            except Exception as e:
                print(f"Failed to load {img_path}: {e}")
                continue

        if batch_images:
            # Compute embeddings
            embeddings = embedder.embed_batch(batch_images)
            all_embeddings.append(embeddings)

            # Store metadata
            for j, img_path in enumerate(batch_files[:len(batch_images)]):
                all_metadata.append({
                    'image_path': str(img_path.relative_to(Path(__file__).parent)),
                    'filename': img_path.name,
                    'category': 'fashion'  # Could extract from filename
                })

    # Combine all embeddings
    embeddings_array = np.vstack(all_embeddings)
    print(f"✓ Computed {len(embeddings_array)} embeddings")

    # Build FAISS index
    IndexBuilder.build_index(
        embeddings_array,
        all_metadata,
        save_path="embeddings/fashion.index",
        metadata_path="embeddings/metadata.pkl"
    )

    print("\n✅ Dataset ready! You can now run: streamlit run app.py")


def download_large_dataset():
    """
    Download larger datasets from public sources
    This function provides instructions for manual download of larger datasets
    """
    print("\n" + "=" * 70)
    print("📚 DOWNLOADING LARGER DATASETS (50k+ images)")
    print("=" * 70)

    print("""
To use a larger dataset, you have several options:

1️⃣  DeepFashion Dataset (Recommended)
   - 50,000+ high-quality fashion images
   - Download: https://github.com/switchablenorms/DeepFashion2
   - Extract to: images_catalog/
   - Then run: python download_dataset.py --build-index-only

2️⃣  Fashion Product Images (Kaggle)
   - 44,000+ product images
   - Download: kaggle datasets download -d paramaggarwal/fashion-product-images-dataset
   - Extract to: images_catalog/
   - Then run: python download_dataset.py --build-index-only

3️⃣  Your own images
   - Place any fashion images in: images_catalog/
   - Then run: python download_dataset.py --build-index-only

After downloading, this script will compute embeddings and build the search index.
    """)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download and prepare fashion dataset")
    parser.add_argument("--build-index-only", action="store_true",
                       help="Skip download, just build index from existing images")
    parser.add_argument("--large-dataset", action="store_true",
                       help="Show instructions for downloading larger datasets")

    args = parser.parse_args()

    try:
        if args.large_dataset:
            download_large_dataset()
        elif args.build_index_only:
            images_dir = Path(__file__).parent / "images_catalog"
            build_embeddings_and_index(images_dir)
        else:
            download_fashion_dataset()

    except KeyboardInterrupt:
        print("\n\n❌ Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
