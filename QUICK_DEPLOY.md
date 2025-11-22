# 🚀 QUICK DEPLOY COMMANDS

## Copy-Paste These Commands (in order):

### 1. Navigate to webapp folder
```bash
cd c:\Users\jmadh\falconhack\webapp
```

### 2. Initialize Git
```bash
git init
git add .
git commit -m "Initial commit: ISS SafetyNet webapp"
git branch -M main
```

### 3. Connect to GitHub
**First, create a new repository on GitHub:**
- Go to: https://github.com/new
- Repository name: `iss-safetynet-webapp`
- Keep it PUBLIC
- DO NOT initialize with README
- Click "Create repository"

**Then run (replace YOUR_USERNAME):**
```bash
git remote add origin https://github.com/YOUR_USERNAME/iss-safetynet-webapp.git
git push -u origin main
```

### 4. Deploy on Render
1. Go to: https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Click "Connect GitHub"
4. Select `iss-safetynet-webapp` repository
5. Click "Connect"
6. Render auto-detects config from `render.yaml`
7. Click "Create Web Service"
8. Wait 5-10 minutes ☕

### 5. Get Your Live URL
After deployment completes:
- URL will be: `https://YOUR-APP-NAME.onrender.com`
- Copy this URL for your presentation!

---

## ✅ Verification Checklist

After deployment, test:
- [ ] Homepage loads
- [ ] Upload image works
- [ ] Detection shows results
- [ ] Bounding boxes appear
- [ ] Confidence scores display
- [ ] No console errors

---

## 🐛 If Something Goes Wrong

**Check Render Logs:**
1. Go to Render dashboard
2. Click on your service
3. Click "Logs" tab
4. Look for errors

**Common fixes:**
- ❌ "best.pt not found" → Ensure file is committed
- ❌ "Module not found" → Check requirements.txt
- ❌ "Bad Gateway" → Wait for full deployment
- ❌ "Timeout" → Normal for first deploy, wait longer

---

## 📞 Support

- **Detailed Guide:** Read `DEPLOYMENT.md`
- **Project Info:** Read `README.md`
- **Render Docs:** https://render.com/docs
- **Render Logs:** Check for specific errors

---

**That's it! Your app will be live in ~10 minutes! 🎉**
