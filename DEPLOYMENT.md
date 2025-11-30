# 🌐 StyliShi Deployment Guide

Complete guide to deploying StyliShi on free cloud platforms

---

## 🎯 Deployment Options

| Platform | Cost | Difficulty | Features |
|----------|------|------------|----------|
| **Streamlit Cloud** | Free | ⭐ Easy | Auto-deploy from GitHub, 1GB RAM |
| **HuggingFace Spaces** | Free | ⭐⭐ Medium | 16GB disk, persistent storage |
| **Render** | Free tier | ⭐⭐ Medium | 512MB RAM, auto-sleep |
| **Railway** | Free $5 credit | ⭐⭐ Medium | Better performance |

**Recommended: Streamlit Cloud** (easiest and best for this app)

---

## 1️⃣ Streamlit Community Cloud (Recommended)

### Prerequisites
- GitHub account
- Your code pushed to a public repo

### Step-by-Step Deployment

#### A. Prepare Your Repository

1. **Create GitHub repo**
   ```bash
   cd StyliShi
   git init
   git add .
   git commit -m "Add StyliShi fashion recommender"
   ```

2. **Push to GitHub**
   ```bash
   # Create repo on github.com, then:
   git remote add origin https://github.com/YOUR_USERNAME/stylishi.git
   git branch -M main
   git push -u origin main
   ```

#### B. Optimize for Cloud Deployment

**Important:** Streamlit Cloud has resource limits:
- 1GB RAM
- 800MB storage

For demo, use a smaller dataset:

```python
# In download_dataset.py, change:
sample_images_info = [...] for i in range(100)  # Change to 50 or 30
```

Rebuild index:
```bash
python download_dataset.py
```

Commit the embeddings:
```bash
git add embeddings/
git commit -m "Add pre-built index for deployment"
git push
```

#### C. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Click **"New app"**

3. Fill in:
   - **Repository**: `YOUR_USERNAME/stylishi`
   - **Branch**: `main`
   - **Main file path**: `app.py`

4. Click **"Deploy"** and wait ~5 minutes

5. Your app is live! 🎉

**Your URL**: `https://YOUR_USERNAME-stylishi.streamlit.app`

#### D. Update Deployment

Any new commit to `main` branch auto-deploys!

```bash
git add .
git commit -m "Update feature"
git push
# Auto-deploys in ~2 minutes
```

---

## 2️⃣ HuggingFace Spaces

### Advantages
- 16GB storage (can use larger datasets)
- Persistent storage
- GPU option (paid)

### Deployment Steps

1. **Create Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Name: `stylishi`
   - SDK: **Streamlit**
   - Hardware: **CPU basic (free)**

2. **Upload Files**

   Option A - Git:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/stylishi
   git push hf main
   ```

   Option B - Web UI:
   - Click "Files" → "Upload files"
   - Upload all project files

3. **Configure**

   Create `README.md` in Space (HuggingFace uses it):
   ```yaml
   ---
   title: StyliShi Fashion Recommender
   emoji: 👗
   colorFrom: purple
   colorTo: pink
   sdk: streamlit
   sdk_version: 1.32.0
   app_file: app.py
   pinned: false
   ---
   ```

4. **Build Index on First Run**

   Add to top of `app.py`:
   ```python
   import subprocess
   import os

   # Auto-build index on first run
   if not os.path.exists("embeddings/fashion.index"):
       subprocess.run(["python", "download_dataset.py"])
   ```

5. **Access Your App**

   URL: `https://huggingface.co/spaces/YOUR_USERNAME/stylishi`

---

## 3️⃣ Render (Alternative)

### Deployment

1. Go to [render.com](https://render.com)

2. Click **"New +"** → **"Web Service"**

3. Connect GitHub repo

4. Configure:
   - **Name**: stylishi
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python download_dataset.py`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

5. Deploy! (free tier sleeps after 15 min inactivity)

---

## 4️⃣ Railway (Alternative)

### Deployment

1. Go to [railway.app](https://railway.app)

2. Click **"Start a New Project"** → **"Deploy from GitHub repo"**

3. Select your `stylishi` repo

4. Add these environment variables:
   - `PORT`: 8501

5. Add start command in `railway.json`:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

6. Deploy! (free $5 credit for new users)

---

## 🔧 Optimization for Cloud

### Reduce Memory Usage

1. **Use smaller CLIP model** (in `utils/embedder.py`):
   ```python
   model_name = "ViT-B-32"  # Current: 512D
   # OR
   model_name = "ViT-B-16"  # Smaller, faster
   ```

2. **Reduce dataset size**:
   - Use 30-50 images for demo
   - Or use smaller image resolution

3. **Enable caching** (already in `app.py`):
   ```python
   @st.cache_resource  # ✓ Already added
   def load_models():
       ...
   ```

### Speed Up Deployment

1. **Pre-commit embeddings** (recommended):
   ```bash
   python download_dataset.py
   git add embeddings/
   git commit -m "Add pre-built index"
   ```

2. **Use lightweight dependencies**:
   - Already using `faiss-cpu` (not full faiss)
   - Using `open-clip-torch` (not full CLIP)

---

## 📊 Monitoring Your App

### Streamlit Cloud
- **Logs**: App settings → "Manage app" → "Logs"
- **Metrics**: Analytics tab shows visitors
- **Reboot**: "Reboot app" button if issues

### HuggingFace
- **Logs**: "Logs" tab in Space
- **Rebuild**: "Factory reboot" to rebuild from scratch

---

## 🐛 Common Deployment Issues

### Issue: "Out of memory"
**Solution:**
- Reduce dataset to 30-50 images
- Use smaller CLIP model
- Upgrade to paid tier

### Issue: "Module not found"
**Solution:**
- Check `requirements.txt` is committed
- Ensure all dependencies listed

### Issue: "Index not found"
**Solution:**
- Commit `embeddings/` folder with index
- OR add setup script to build on first run

### Issue: "Camera not working"
**Solution:**
- HTTPS required for camera access
- All cloud platforms provide HTTPS by default
- Check browser permissions

---

## 🎯 Post-Deployment Checklist

- [ ] App loads without errors
- [ ] All 3 search modes work (Camera, Upload, Samples)
- [ ] Results display correctly
- [ ] Images load properly
- [ ] Mobile-responsive (test on phone)
- [ ] Add custom domain (optional, Streamlit Cloud supports this)
- [ ] Share link in EDISS application! 🎓

---

## 🌟 Pro Tips

1. **Custom domain**: Streamlit Cloud allows custom domains (yourname.com)
2. **Analytics**: Add Google Analytics to track visitors
3. **A/B testing**: Deploy multiple versions (dev/prod) on different branches
4. **Monitoring**: Use Streamlit's built-in analytics
5. **SEO**: Add meta tags in Streamlit config for better discovery

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **HuggingFace Docs**: https://huggingface.co/docs/hub/spaces
- **GitHub Issues**: Report issues in your repo

Happy deploying! 🚀
