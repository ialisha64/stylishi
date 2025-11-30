"""
Quick test script to verify LookGPT installation
Run this after setup to ensure everything works
"""

import sys
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_dependencies():
    """Check if all required packages are installed"""
    print_header("1️⃣  Checking Dependencies")

    required = [
        ('streamlit', 'Streamlit'),
        ('torch', 'PyTorch'),
        ('open_clip', 'OpenCLIP'),
        ('faiss', 'FAISS'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
    ]

    all_good = True
    for module, name in required:
        try:
            __import__(module)
            print(f"✓ {name:<15} installed")
        except ImportError:
            print(f"✗ {name:<15} NOT FOUND - run: pip install -r requirements.txt")
            all_good = False

    return all_good


def check_file_structure():
    """Check if all required files exist"""
    print_header("2️⃣  Checking File Structure")

    required_files = [
        'app.py',
        'download_dataset.py',
        'requirements.txt',
        'utils/embedder.py',
        'utils/search.py',
        '.streamlit/config.toml',
    ]

    all_good = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✓ {file:<30} exists")
        else:
            print(f"✗ {file:<30} MISSING")
            all_good = False

    return all_good


def check_directories():
    """Check if required directories exist"""
    print_header("3️⃣  Checking Directories")

    required_dirs = [
        'embeddings',
        'images_catalog',
        'sample_images',
        'utils',
    ]

    all_good = True
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"✓ {dir_name:<20} exists")
        else:
            print(f"⚠ {dir_name:<20} not found (will be created)")

    return True  # Directories can be created


def check_models():
    """Check if models can be loaded"""
    print_header("4️⃣  Testing Model Loading")

    try:
        print("Loading CLIP model (this may take 1-2 minutes first time)...")
        from utils.embedder import FashionEmbedder

        embedder = FashionEmbedder()
        print(f"✓ CLIP model loaded successfully")
        print(f"  - Device: {embedder.device}")
        print(f"  - Embedding dim: {embedder.embedding_dim}")

        # Quick test
        import numpy as np
        from PIL import Image
        test_img = Image.new('RGB', (224, 224), color='red')
        embedding = embedder.embed_image(test_img)
        print(f"✓ Test embedding generated: shape {embedding.shape}")

        return True
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        return False


def check_dataset():
    """Check if dataset and index exist"""
    print_header("5️⃣  Checking Dataset & Index")

    index_path = Path("embeddings/fashion.index")
    metadata_path = Path("embeddings/metadata.pkl")

    if index_path.exists() and metadata_path.exists():
        print(f"✓ FAISS index exists")
        print(f"✓ Metadata exists")

        # Try loading
        try:
            from utils.search import FashionSearchEngine
            engine = FashionSearchEngine()
            engine.load()
            stats = engine.get_stats()
            print(f"✓ Index loaded successfully")
            print(f"  - Total items: {stats['total_items']:,}")
            print(f"  - Embedding dim: {stats['embedding_dim']}")
            print(f"  - Index type: {stats['index_type']}")
            return True
        except Exception as e:
            print(f"✗ Index loading failed: {e}")
            return False
    else:
        print(f"⚠ Index not found")
        print(f"  Run: python download_dataset.py")
        return False


def check_samples():
    """Check if sample images exist"""
    print_header("6️⃣  Checking Sample Images")

    sample_dir = Path("sample_images")
    if sample_dir.exists():
        samples = list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.png"))
        if len(samples) > 0:
            print(f"✓ Found {len(samples)} sample images")
            return True
        else:
            print(f"⚠ No sample images found")
            print(f"  Run: python create_samples.py")
            return False
    else:
        print(f"⚠ sample_images/ directory not found")
        print(f"  Run: python create_samples.py")
        return False


def print_summary(results):
    """Print final summary"""
    print_header("📊 Test Summary")

    total = len(results)
    passed = sum(results.values())

    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:<10} {test}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 Everything looks good! You can now run:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        if not results.get("Dataset & Index"):
            print("\n💡 Quick fix: Run these commands:")
            print("   python create_samples.py")
            print("   python download_dataset.py")


def main():
    """Run all tests"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║                  LookGPT Installation Test                      ║
    ║                                                                  ║
    ║     This script verifies your LookGPT setup is complete         ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

    results = {
        "Dependencies": check_dependencies(),
        "File Structure": check_file_structure(),
        "Directories": check_directories(),
        "Model Loading": check_models(),
        "Dataset & Index": check_dataset(),
        "Sample Images": check_samples(),
    }

    print_summary(results)

    # Exit code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
