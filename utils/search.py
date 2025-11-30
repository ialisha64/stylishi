"""
Lightning-fast FAISS-based vector similarity search
Handles 50k+ items with <100ms query time
"""

import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except AttributeError:
        pass

import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Tuple
import pandas as pd


class FashionSearchEngine:
    """
    Production FAISS search engine for fashion similarity
    Uses IndexFlatIP for exact cosine similarity (embeddings are L2-normalized)
    """

    def __init__(self, index_path: str = "embeddings/fashion.index",
                 metadata_path: str = "embeddings/metadata.pkl"):
        """
        Initialize search engine with pre-built index

        Args:
            index_path: Path to FAISS index file
            metadata_path: Path to metadata pickle (image paths, etc.)
        """
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index = None
        self.metadata = None
        self.loaded = False

    def load(self):
        """Load FAISS index and metadata"""
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"Index not found at {self.index_path}. "
                f"Run 'python download_dataset.py' first!"
            )

        print(f"📚 Loading FAISS index from {self.index_path}...")
        self.index = faiss.read_index(str(self.index_path))
        print(f"✓ Index loaded | {self.index.ntotal:,} items indexed")

        # Load metadata
        if self.metadata_path.exists():
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            print(f"✓ Metadata loaded | {len(self.metadata)} entries")
        else:
            print("⚠️  No metadata found, using index-only mode")
            self.metadata = [{"image_path": f"item_{i}.jpg"}
                           for i in range(self.index.ntotal)]

        self.loaded = True

    def search(self, query_embedding: np.ndarray, k: int = 10) -> List[dict]:
        """
        Find k most similar items to query

        Args:
            query_embedding: L2-normalized embedding vector (512,)
            k: Number of results to return

        Returns:
            List of dicts with 'image_path', 'similarity', 'rank'
        """
        if not self.loaded:
            self.load()

        # Ensure 2D shape for FAISS
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        # Search (returns distances and indices)
        # For normalized vectors with IndexFlatIP, distance = cosine similarity
        similarities, indices = self.index.search(
            query_embedding.astype('float32'), k
        )

        # Build results
        results = []
        for rank, (idx, sim) in enumerate(zip(indices[0], similarities[0])):
            result = {
                'rank': rank + 1,
                'similarity': float(sim),
                'similarity_pct': f"{float(sim) * 100:.1f}%",
                'index': int(idx),
            }

            # Add metadata if available
            if self.metadata and idx < len(self.metadata):
                result.update(self.metadata[int(idx)])
            else:
                result['image_path'] = f"images_catalog/item_{int(idx)}.jpg"

            results.append(result)

        return results

    def get_stats(self) -> dict:
        """Get index statistics"""
        if not self.loaded:
            self.load()

        return {
            'total_items': self.index.ntotal,
            'embedding_dim': self.index.d,
            'index_type': type(self.index).__name__,
        }


class IndexBuilder:
    """
    Utility class to build FAISS index from embeddings
    Used by download_dataset.py
    """

    @staticmethod
    def build_index(embeddings: np.ndarray,
                   metadata: List[dict],
                   save_path: str = "embeddings/fashion.index",
                   metadata_path: str = "embeddings/metadata.pkl"):
        """
        Build and save FAISS index

        Args:
            embeddings: Array of L2-normalized embeddings (N, 512)
            metadata: List of metadata dicts (image paths, etc.)
            save_path: Where to save index
            metadata_path: Where to save metadata
        """
        print(f"🔨 Building FAISS index from {len(embeddings):,} embeddings...")

        # Ensure embeddings are normalized and float32
        embeddings = embeddings.astype('float32')
        faiss.normalize_L2(embeddings)  # Ensure L2 norm = 1

        # Create index (IndexFlatIP for exact cosine similarity)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)

        # Add vectors
        index.add(embeddings)
        print(f"✓ Added {index.ntotal:,} vectors to index")

        # Save index
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(save_path))
        print(f"✓ Index saved to {save_path}")

        # Save metadata
        metadata_path = Path(metadata_path)
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        print(f"✓ Metadata saved to {metadata_path}")

        return index


if __name__ == "__main__":
    # Test with dummy data
    print("Creating test index...")
    test_embeddings = np.random.randn(1000, 512).astype('float32')
    test_metadata = [{'image_path': f'test_{i}.jpg'} for i in range(1000)]

    IndexBuilder.build_index(
        test_embeddings,
        test_metadata,
        save_path="embeddings/test.index",
        metadata_path="embeddings/test_metadata.pkl"
    )

    # Test search
    engine = FashionSearchEngine(
        index_path="embeddings/test.index",
        metadata_path="embeddings/test_metadata.pkl"
    )
    query = np.random.randn(512).astype('float32')
    query = query / np.linalg.norm(query)

    results = engine.search(query, k=5)
    print(f"\n✓ Found {len(results)} results:")
    for r in results:
        print(f"  Rank {r['rank']}: {r['image_path']} ({r['similarity_pct']})")
