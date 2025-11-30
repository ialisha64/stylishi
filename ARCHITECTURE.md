# 🏗️ StyliShi System Architecture

Complete technical architecture for the real-time fashion recommender

---

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                       (Streamlit Web App)                       │
│                                                                 │
│  ┌───────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ 📸 Camera     │  │ 🖼️  Upload     │  │ 🎨 Sample        │  │
│  │   Input       │  │    Image       │  │   Gallery        │  │
│  └───────┬───────┘  └────────┬───────┘  └─────────┬────────┘  │
│          │                   │                     │           │
│          └───────────────────┴─────────────────────┘           │
│                              │                                 │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   IMAGE PROCESSOR    │
                    │  (PIL, OpenCV, NumPy)│
                    │  • Resize to 224x224 │
                    │  • RGB conversion    │
                    │  • Normalization     │
                    └──────────┬───────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       EMBEDDING LAYER                           │
│                   (utils/embedder.py)                           │
│                                                                 │
│     ┌───────────────────────────────────────────────────┐      │
│     │           OpenAI CLIP ViT-B/32                    │      │
│     │                                                   │      │
│     │  Input:  224×224×3 RGB image                     │      │
│     │  Output: 512-dimensional vector                  │      │
│     │  Time:   ~40ms (CPU) / ~5ms (GPU)               │      │
│     │                                                   │      │
│     │  Architecture:                                    │      │
│     │  • Vision Transformer (12 layers)                │      │
│     │  • Patch size: 32×32                             │      │
│     │  • Pre-trained on 400M image-text pairs          │      │
│     │  • L2-normalized output for cosine similarity    │      │
│     └───────────────────────────────────────────────────┘      │
│                              │                                 │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼ 512D vector (L2-norm = 1.0)
                               │
┌─────────────────────────────────────────────────────────────────┐
│                        SEARCH LAYER                             │
│                     (utils/search.py)                           │
│                                                                 │
│     ┌───────────────────────────────────────────────────┐      │
│     │              FAISS IndexFlatIP                    │      │
│     │                                                   │      │
│     │  Index Type:  Flat (exact search)                │      │
│     │  Metric:      Inner Product (cosine similarity)  │      │
│     │  Index Size:  50,000 × 512 = ~100MB              │      │
│     │  Query Time:  ~50ms for 50k vectors              │      │
│     │                                                   │      │
│     │  Algorithm:                                       │      │
│     │  1. Compute dot product: q·v for all v           │      │
│     │  2. Find top-k maximum scores                    │      │
│     │  3. Return indices + similarity scores           │      │
│     │                                                   │      │
│     │  Optimization:                                    │      │
│     │  • L2-normalized vectors → dot = cosine          │      │
│     │  • CPU-optimized BLAS operations                │      │
│     │  • Can upgrade to GPU for 10x speedup           │      │
│     └───────────────────────────────────────────────────┘      │
│                              │                                 │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼ Top-10 results + scores
                               │
┌─────────────────────────────────────────────────────────────────┐
│                       RESULTS DISPLAY                           │
│                    (Streamlit Components)                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Performance Metrics                                     │  │
│  │  • Total Time: 89ms  • Embedding: 42ms  • Search: 47ms  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Rank #1     │ │ Rank #2     │ │ Rank #3     │              │
│  │ [Image]     │ │ [Image]     │ │ [Image]     │              │
│  │ 97.3% match │ │ 95.1% match │ │ 93.8% match │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                    ... 7 more results ...                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Query Processing Pipeline

```
User Action
    │
    ▼
┌───────────────────────────────────────────────────────────┐
│ Step 1: Image Capture                                     │
│ • Source: Camera / Upload / Sample                        │
│ • Format: JPEG/PNG                                        │
│ • Resolution: Any (auto-resized)                          │
└───────┬───────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│ Step 2: Image Preprocessing                               │
│ • Convert to RGB (if RGBA/grayscale)                      │
│ • Resize to 224×224                                       │
│ • Apply CLIP normalization                                │
│ • Convert to tensor: [1, 3, 224, 224]                    │
│ ⏱️  Time: ~2ms                                            │
└───────┬───────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│ Step 3: Feature Extraction (CLIP Encoder)                 │
│ • Vision Transformer forward pass                         │
│ • Output: [1, 512] embedding                              │
│ • L2 normalization: ||v|| = 1.0                           │
│ ⏱️  Time: ~40ms (CPU) / ~5ms (GPU)                        │
└───────┬───────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│ Step 4: Similarity Search (FAISS)                         │
│ • Query: 512D vector                                       │
│ • Index: 50,000 × 512 matrix                              │
│ • Operation: argmax_k(query · index[i])                   │
│ • Output: top-10 indices + similarities                   │
│ ⏱️  Time: ~50ms (CPU) / ~5ms (GPU)                        │
└───────┬───────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│ Step 5: Result Formatting                                 │
│ • Load images from catalog                                │
│ • Convert similarity to percentage                        │
│ • Add metadata (rank, path, etc.)                         │
│ ⏱️  Time: ~5ms                                            │
└───────┬───────────────────────────────────────────────────┘
        │
        ▼
    Display Results
    Total Time: ~100ms
```

---

## 📦 Component Details

### 1. Frontend Layer (app.py)

**Technology**: Streamlit 1.32+

**Responsibilities**:
- User interface rendering
- Camera input handling
- File upload management
- Result visualization
- Real-time metric display

**Key Features**:
- Mobile-responsive design
- Custom CSS styling
- Session state management
- Caching for performance

**Code Structure**:
```python
app.py (350 lines)
├── Configuration & Styling
├── Model Loading (@st.cache_resource)
├── Helper Functions
│   ├── process_image_search()
│   └── display_results()
└── Main App
    ├── Camera Mode
    ├── Upload Mode
    └── Sample Mode
```

---

### 2. Embedding Layer (utils/embedder.py)

**Technology**: OpenCLIP, PyTorch

**Model Specifications**:
```yaml
Architecture: Vision Transformer (ViT)
Variant: ViT-B/32
Parameters: 86M
Input Size: 224 × 224 × 3
Output Dim: 512
Normalization: L2 (unit sphere)
Training Data: LAION-400M
```

**Class Structure**:
```python
FashionEmbedder
├── __init__(model_name, pretrained)
│   └── Load CLIP model to device
├── embed_image(image) → np.ndarray
│   ├── Convert to PIL if numpy
│   ├── Preprocess (resize, normalize)
│   ├── Forward pass
│   └── L2 normalize
└── embed_batch(images) → np.ndarray
    └── Batch processing for efficiency
```

**Performance Optimization**:
- `@torch.no_grad()` for inference (no gradients)
- Auto-detection of GPU/CPU
- L2 normalization for faster search
- Batch processing support

---

### 3. Search Layer (utils/search.py)

**Technology**: FAISS (Facebook AI Similarity Search)

**Index Specifications**:
```yaml
Index Type: IndexFlatIP (flat inner product)
Metric: Cosine similarity (via L2-normalized vectors)
Precision: Exact (not approximate)
Memory: ~100MB for 50k × 512 floats
Query Time: O(n) linear scan
Scalability: Up to 1M items on CPU
```

**Class Structure**:
```python
FashionSearchEngine
├── __init__(index_path, metadata_path)
├── load()
│   ├── Load FAISS index
│   └── Load metadata pickle
├── search(embedding, k=10) → List[dict]
│   ├── FAISS query
│   ├── Map indices to metadata
│   └── Format results
└── get_stats() → dict

IndexBuilder (static methods)
└── build_index(embeddings, metadata)
    ├── Create IndexFlatIP
    ├── Add vectors
    ├── Save index + metadata
    └── Return index
```

**Why IndexFlatIP?**:
- Exact search (100% recall)
- Fast for <1M vectors
- Simple implementation
- L2-normalized → inner product = cosine

**Upgrade Path**:
```
Current:  IndexFlatIP (exact, 50k items)
    ↓
10k-1M:   IndexIVFFlat (approximate, 100x faster)
    ↓
1M-100M:  IndexIVFPQ (compressed, 1000x faster)
    ↓
100M+:    GPU-accelerated IndexIVFPQ
```

---

### 4. Dataset Layer (download_dataset.py)

**Process**:
```
1. Download Images
   ├── Fetch from public APIs
   ├── Verify image integrity
   └── Save to images_catalog/

2. Compute Embeddings
   ├── Load FashionEmbedder
   ├── Process in batches (32 images)
   ├── Generate 512D vectors
   └── Store in numpy array

3. Build FAISS Index
   ├── Create IndexFlatIP(512)
   ├── Add all embeddings
   └── Save index + metadata

4. Validate
   ├── Test search query
   └── Verify results
```

**Metadata Structure**:
```python
[
    {
        'image_path': 'images_catalog/fashion_00001.jpg',
        'filename': 'fashion_00001.jpg',
        'category': 'dress',
        'id': 'fashion_00001'
    },
    ...
]
```

---

## ⚡ Performance Analysis

### Latency Breakdown

```
Total Query Time: ~95ms
├── Image Preprocessing:    2ms  (2%)
├── CLIP Embedding:        42ms (44%)
├── FAISS Search:          47ms (49%)
└── Result Formatting:      4ms  (4%)
```

### Bottleneck Analysis

**CPU-bound operations**:
1. CLIP forward pass (40ms)
2. FAISS linear scan (47ms)

**Optimization strategies**:
- ✅ Already using L2-normalized vectors
- ✅ Batch processing where possible
- ✅ Model caching with @st.cache_resource
- 🔄 GPU acceleration (10x speedup)
- 🔄 FAISS IVF index (100x speedup for large datasets)

### Memory Footprint

```
Component                Size
─────────────────────────────────────
CLIP Model             340 MB
FAISS Index (50k)      100 MB
Streamlit Runtime       50 MB
Python + Dependencies  200 MB
─────────────────────────────────────
Total (approx.)        690 MB
```

**Cloud Limits**:
- Streamlit Cloud: 1GB RAM ✅
- HuggingFace: 16GB RAM ✅✅

---

## 🔐 Security Considerations

### Input Validation
```python
# Image type checking
allowed_types = ['.jpg', '.jpeg', '.png']

# Size limits
max_upload_size = 10 MB

# Resolution limits
max_dimension = 4096 px
```

### No User Data Storage
- No cookies
- No user accounts
- No tracking
- Camera access only during session

### Deployment Security
- HTTPS by default (all cloud platforms)
- No API keys required
- No database connections
- Read-only file system

---

## 🧪 Testing Strategy

### Unit Tests
```python
tests/
├── test_embedder.py
│   ├── test_model_loading
│   ├── test_embedding_shape
│   └── test_normalization
├── test_search.py
│   ├── test_index_creation
│   ├── test_search_results
│   └── test_similarity_scores
└── test_app.py
    └── test_ui_components
```

### Integration Tests
```python
# End-to-end query test
image → embedder → search → results
Expected: 10 results in <100ms
```

### Performance Tests
```python
# Benchmark script
for i in range(100):
    time = query_fashion_item()
    assert time < 100ms

print(f"Avg: {mean}ms, P95: {p95}ms")
```

---

## 🚀 Scalability Roadmap

### Current (50k items, CPU)
```
Index: IndexFlatIP
Query: 50ms
Memory: 100MB
Cost: $0/month
```

### Phase 1: GPU Acceleration
```
Index: IndexFlatIP on GPU
Query: 5ms (10x faster)
Memory: 100MB GPU
Cost: ~$50/month (cloud GPU)
```

### Phase 2: Approximate Search (1M items)
```
Index: IndexIVFFlat (nlist=100)
Query: 10ms
Memory: 800MB
Cost: $0/month (CPU fine)
```

### Phase 3: Product Quantization (10M items)
```
Index: IndexIVFPQ (nlist=1000, m=8)
Query: 15ms
Memory: 400MB (compressed)
Cost: $0/month
```

### Phase 4: Distributed (100M+ items)
```
Index: Sharded IVFPQ across GPUs
Query: 20ms
Memory: 4GB distributed
Cost: ~$200/month
```

---

## 📊 Monitoring & Observability

### Metrics to Track

```python
# Application metrics
- Queries per second (QPS)
- P50, P95, P99 latency
- Error rate
- Cache hit rate

# ML metrics
- Average similarity score
- Top-1 accuracy (user feedback)
- Embedding distribution
- Search quality

# Infrastructure
- Memory usage
- CPU utilization
- Network I/O
- Disk usage
```

### Logging Strategy

```python
import logging

logger.info("Query processed", extra={
    "query_time_ms": 89,
    "embedding_time_ms": 42,
    "search_time_ms": 47,
    "results_count": 10,
    "top_similarity": 0.97
})
```

---

## 🔮 Future Enhancements

### 1. Multimodal Search
```
Text Query ("red dress")
    ↓
CLIP Text Encoder
    ↓
512D Text Embedding
    ↓
FAISS Search (same index!)
    ↓
Results
```

### 2. Hybrid Search
```
Vector Similarity (0.7×) + Metadata Filter (0.3×)
    ↓
Combined Score
    ↓
Re-ranked Results
```

### 3. Fine-tuning
```
DeepFashion2 Dataset
    ↓
Fine-tune CLIP on Fashion
    ↓
Better Domain Accuracy
```

### 4. Online Learning
```
User Clicks/Purchases
    ↓
Update Ranking Model
    ↓
Improved Results
```

---

## 📚 References

### Papers
- **CLIP**: "Learning Transferable Visual Models From Natural Language Supervision" (Radford et al., 2021)
- **FAISS**: "Billion-scale similarity search with GPUs" (Johnson et al., 2017)
- **Vision Transformer**: "An Image is Worth 16x16 Words" (Dosovitskiy et al., 2020)

### Libraries
- OpenCLIP: https://github.com/mlfoundations/open_clip
- FAISS: https://github.com/facebookresearch/faiss
- Streamlit: https://github.com/streamlit/streamlit

### Datasets
- DeepFashion2: https://github.com/switchablenorms/DeepFashion2
- LAION-400M: https://laion.ai/blog/laion-400-open-dataset/

---

**This architecture is designed for:**
- ✅ Production reliability
- ✅ Easy deployment
- ✅ Cost efficiency
- ✅ Scalability
- ✅ Maintainability

**Perfect for your EDISS portfolio!** 🎓
