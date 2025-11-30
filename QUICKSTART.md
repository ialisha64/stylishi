# 🚀 StyliShi Quick Start Guide

Get your fashion recommender running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected time: ~2-3 minutes

## Step 2: Create Sample Images (Optional)

```bash
python create_samples.py
```

This creates 10 sample fashion images for testing. Expected time: ~10 seconds

## Step 3: Download Dataset & Build Index

```bash
python download_dataset.py
```

This will:
- Download 100+ demo fashion images (~2 minutes)
- Compute CLIP embeddings (~3-5 minutes)
- Build FAISS search index (~30 seconds)

**Total time: ~10 minutes**

## Step 4: Launch the App

```bash
streamlit run app.py --server.maxUploadSize=10
```

Open http://localhost:8501 in your browser! 🎉

---

## 📱 Using on Phone

1. On your computer, note your local IP (e.g., 192.168.1.100)
2. Run: `streamlit run app.py --server.address=0.0.0.0`
3. On your phone, open: `http://YOUR_IP:8501`
4. Use phone camera to search for fashion items!

---

## 🐛 Troubleshooting

### Error: "Index not found"
**Solution:** Run `python download_dataset.py` first

### Error: "No module named 'open_clip'"
**Solution:** Run `pip install -r requirements.txt`

### Camera not working
**Solution:**
- Allow camera permissions in browser
- Try different browser (Chrome/Firefox work best)
- Check browser console for errors

### Slow performance
**Solution:**
- Close other applications
- Use smaller batch size in download_dataset.py
- Consider using GPU (install faiss-gpu)

---

## 💡 Pro Tips

1. **Test with samples first**: Use the "🎨 Sample Images" tab before trying camera
2. **Good lighting**: Better lighting = better results
3. **Clear background**: Plain backgrounds work best
4. **Close-up shots**: Get close to the clothing item
5. **Multiple angles**: Try different angles for best matches

---

## 🎯 Next Steps

- [ ] Try all 3 search modes (Camera, Upload, Samples)
- [ ] Add your own fashion images to `images_catalog/`
- [ ] Rebuild index with `python download_dataset.py --build-index-only`
- [ ] Deploy to Streamlit Cloud (see README.md)
- [ ] Share your portfolio project with EDISS committee! 🎓

---

## 📞 Need Help?

Check the main [README.md](README.md) for:
- Detailed architecture explanation
- Advanced configuration options
- Deployment guides
- Contributing guidelines
