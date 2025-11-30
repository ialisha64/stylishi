# 🚀 START HERE - Your Complete StyliShi Setup Guide

**Welcome! You're 15 minutes away from a running AI fashion recommender.**

---

## 📋 What You're Building

**StyliShi** is a production-grade fashion recommender that:
- Uses your phone/laptop camera to search for similar clothing
- Searches 50,000+ items in under 1 second
- Works on any device (mobile-responsive)
- Costs $0 to run and deploy

Perfect for your **Erasmus Mundus EDISS portfolio**! 🎓

---

## ⚡ Quick Setup (3 Commands)

Open your terminal and run:

### Step 1: Install dependencies (~3 minutes)
```bash
pip install -r requirements.txt
```

### Step 2: Create sample images (~10 seconds)
```bash
python create_samples.py
```

### Step 3: Build search index (~10 minutes)
```bash
python download_dataset.py
```

### Step 4: Launch app (~5 seconds)
```bash
streamlit run app.py
```

**Open http://localhost:8501 and start searching!** 🎉

---

## 🧪 Test Your Setup

Run this to verify everything works:

```bash
python test_setup.py
```

You should see:
```
✓ PASS     Dependencies
✓ PASS     File Structure
✓ PASS     Directories
✓ PASS     Model Loading
✓ PASS     Dataset & Index
✓ PASS     Sample Images

🎉 Everything looks good!
```

---

## 📱 Using on Your Phone

1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4)
   - Mac/Linux: `ifconfig` or `ip addr`

2. Launch app with network access:
   ```bash
   streamlit run app.py --server.address=0.0.0.0
   ```

3. On your phone, open:
   ```
   http://YOUR_IP:8501
   ```
   Example: `http://192.168.1.100:8501`

4. Point camera at clothing and search! 📸

---

## 📚 Documentation Guide

The project includes comprehensive docs - here's when to read each:

| File | When to Read | What It Covers |
|------|-------------|----------------|
| **START_HERE.md** | 👈 You are here! | Quick setup |
| **QUICKSTART.md** | After setup | Detailed usage guide |
| **README.md** | Before deploying | Full documentation |
| **DEPLOYMENT.md** | When deploying to cloud | 4 platform guides |
| **EDISS_PORTFOLIO.md** | When applying to EDISS | Application tips |
| **PROJECT_SUMMARY.md** | For overview | Complete summary |
| **CONTRIBUTING.md** | If contributing | Dev guidelines |

**Recommended reading order:**
1. START_HERE.md (this file)
2. Run the app and test it
3. QUICKSTART.md for tips
4. README.md for full docs
5. DEPLOYMENT.md to deploy
6. EDISS_PORTFOLIO.md for application

---

## 🎯 What to Do First

### Option A: Quick Test (5 minutes)

Just want to see it work?

1. Install dependencies
2. Run test: `python test_setup.py`
3. If models need download, wait 2-3 minutes
4. Create samples: `python create_samples.py`
5. Launch: `streamlit run app.py`
6. Use "Sample Images" tab

**No dataset needed for quick test!**

### Option B: Full Setup (15 minutes)

Want the complete experience?

1. Follow "Quick Setup" above (all 4 steps)
2. Wait for dataset download (~10 min)
3. Launch app
4. Try all 3 modes: Camera, Upload, Samples

**Recommended for portfolio demo!**

---

## ❓ Troubleshooting

### "Command not found: python"
**Fix:** Try `python3` instead of `python`

### "No module named 'streamlit'"
**Fix:** Install dependencies: `pip install -r requirements.txt`

### "Index not found" error
**Fix:** Run dataset setup: `python download_dataset.py`

### Camera not working
**Fix:**
- Allow camera in browser permissions
- Try Chrome or Firefox (best support)
- Check if other apps are using camera

### Slow performance
**Fix:**
- Close other apps
- Use smaller dataset (edit `download_dataset.py` line 95: change 100 to 30)
- Restart and rebuild

### Port already in use
**Fix:** Use different port:
```bash
streamlit run app.py --server.port=8502
```

---

## 🎓 For EDISS Application

This project demonstrates:

✅ **Computer Vision**: CLIP vision transformer (SOTA 2024)
✅ **Scalable Systems**: FAISS vector search (50k+ items)
✅ **Production ML**: <100ms latency, real-time processing
✅ **Full-Stack**: End-to-end app development
✅ **Cloud Deployment**: Zero-cost scalable hosting

**See [EDISS_PORTFOLIO.md](EDISS_PORTFOLIO.md) for:**
- Motivation letter snippets (ready to copy)
- CV project descriptions
- Interview talking points
- Demo video script
- Email templates

---

## 📸 Create Your Demo

For your portfolio, you need:

### 1. Screenshots (4-5 images)
- Homepage with camera
- Search results page
- Mobile view
- Performance metrics

### 2. Demo GIF (25 seconds)
Tools: ScreenToGif (Windows), Kap (Mac), Peek (Linux)

Show:
1. Opening app
2. Pointing camera at clothing
3. Click search
4. Results appearing (<1 sec)

### 3. Demo Video (2 minutes)
Script in [EDISS_PORTFOLIO.md](EDISS_PORTFOLIO.md)

Record:
1. Introduction (15s)
2. Live demo (45s)
3. Technical explanation (45s)
4. Closing (15s)

---

## 🌐 Deploy to Cloud (FREE)

Once your app works locally:

**Easiest: Streamlit Cloud** (2 clicks)

1. Push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Add StyliShi"
   git remote add origin https://github.com/YOUR_USERNAME/stylishi.git
   git push -u origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your repo → Deploy!

**Done! Live URL in 5 minutes.**

Full guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📊 Expected Performance

After setup, you should see:

| Metric | Target | What It Means |
|--------|--------|---------------|
| **Embedding Time** | <50ms | CLIP model inference |
| **Search Time** | <50ms | FAISS similarity search |
| **Total Query** | <100ms | End-to-end search time |
| **Camera FPS** | 30 FPS | Smooth video feed |

**If you see these numbers, you're golden!** ✨

---

## 🎯 Next Steps Checklist

- [ ] Complete setup (4 commands above)
- [ ] Run test: `python test_setup.py`
- [ ] Launch app: `streamlit run app.py`
- [ ] Try all 3 search modes
- [ ] Test on mobile phone
- [ ] Take screenshots for portfolio
- [ ] Record demo video
- [ ] Deploy to Streamlit Cloud
- [ ] Update README with your info
- [ ] Share on LinkedIn
- [ ] Add to EDISS application

---

## 🆘 Need Help?

1. **Setup issues?** → Read [QUICKSTART.md](QUICKSTART.md)
2. **Deployment issues?** → Read [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Application tips?** → Read [EDISS_PORTFOLIO.md](EDISS_PORTFOLIO.md)
4. **Still stuck?** → Check GitHub Issues

---

## 🎉 You're Ready!

This project will:
- ✅ Impress the EDISS selection committee
- ✅ Demonstrate production ML skills
- ✅ Show full-stack capabilities
- ✅ Prove you can ship complete products
- ✅ Stand out in your application

**Now go build and deploy!** 🚀

---

## 📞 Quick Links

- **Main Docs**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Deploy Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Application Guide**: [EDISS_PORTFOLIO.md](EDISS_PORTFOLIO.md)
- **Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

<div align="center">

**Built for EDISS candidates**

Made with ❤️ and lots of ☕

*Good luck with your application!* 🎓

</div>
