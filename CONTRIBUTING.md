# 🤝 Contributing to StyliShi

Thank you for your interest in contributing to StyliShi! This document provides guidelines for contributing.

## 🎯 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/YOUR_USERNAME/stylishi/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, etc.)

### Suggesting Features

1. Open an issue with tag `enhancement`
2. Describe the feature and its benefits
3. Provide examples of how it would work

### Pull Requests

1. **Fork** the repository
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**:
   ```bash
   python download_dataset.py
   streamlit run app.py
   ```
5. **Commit** with clear messages:
   ```bash
   git commit -m "Add: amazing feature that does X"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** with:
   - Description of changes
   - Why the change is needed
   - Screenshots/GIFs if applicable

## 📝 Code Style

- **Python**: Follow PEP 8
- **Docstrings**: Use Google style
- **Type hints**: Add where appropriate
- **Comments**: Explain *why*, not *what*

Example:
```python
def embed_image(self, image: Union[Image.Image, np.ndarray]) -> np.ndarray:
    """
    Generate 512-dim embedding from image

    Args:
        image: PIL Image or numpy array (RGB)

    Returns:
        L2-normalized embedding vector (512,)
    """
    # Convert numpy to PIL if needed (CLIP requires PIL)
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    ...
```

## 🧪 Testing

Before submitting PR:

1. Test all 3 search modes (Camera, Upload, Samples)
2. Check mobile responsiveness
3. Verify no console errors
4. Test with different image sizes
5. Ensure dataset build works

## 🌟 Areas for Contribution

### High Priority
- [ ] Text-based search ("red dress", "leather jacket")
- [ ] Multi-language support
- [ ] Better sample dataset
- [ ] Performance optimizations
- [ ] Mobile app (React Native)

### Medium Priority
- [ ] Price filtering
- [ ] Category filtering
- [ ] Color extraction
- [ ] Similar color matching
- [ ] Export results

### Nice to Have
- [ ] User accounts
- [ ] Save favorites
- [ ] Share results
- [ ] Social media integration
- [ ] Browser extension

## 📚 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/stylishi.git
cd stylishi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup dataset
python download_dataset.py

# Run app
streamlit run app.py
```

## 🎓 Learning Resources

- **Streamlit**: https://docs.streamlit.io
- **CLIP**: https://github.com/openai/CLIP
- **FAISS**: https://github.com/facebookresearch/faiss
- **Computer Vision**: https://pytorch.org/vision/stable/index.html

## 📧 Questions?

- Open a [Discussion](https://github.com/YOUR_USERNAME/stylishi/discussions)
- Tag maintainers in issues
- Email: your.email@example.com

## 🙏 Thank You!

Every contribution, no matter how small, is valued and appreciated!

**Happy coding! 🚀**
