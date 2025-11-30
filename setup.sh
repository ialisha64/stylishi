#!/bin/bash

# Setup script for Streamlit Cloud deployment
echo "🚀 Setting up LookGPT..."

# Create necessary directories
mkdir -p embeddings
mkdir -p images_catalog
mkdir -p sample_images

# Download and build dataset (if not already present)
if [ ! -f "embeddings/fashion.index" ]; then
    echo "📦 Building fashion index..."
    python download_dataset.py
else
    echo "✓ Index already exists, skipping download"
fi

echo "✅ Setup complete!"
