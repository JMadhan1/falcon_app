# 🚀 Deployment Guide - ISS SafetyNet Webapp

## Step-by-Step Deployment to Render

### Step 1: Prepare the Webapp Folder

The `webapp` folder is now ready with all necessary files:
- ✅ `app.py` - Flask application
- ✅ `best.pt` - Trained YOLOv8 model
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Process configuration
- ✅ `render.yaml` - Render configuration
- ✅ `static/` - CSS and JavaScript files
- ✅ `templates/` - HTML templates

### Step 2: Create a New GitHub Repository

1. **Go to GitHub** and create a new repository:
   - Name: `iss-safetynet-webapp` (or any name you prefer)
   - Description: "AI-powered safety equipment detection for ISS"
   - Visibility: Public
   - **DO NOT** initialize with README, .gitignore, or license

2. **Copy the repository URL** (e.g., `https://github.com/YOUR_USERNAME/iss-safetynet-webapp.git`)

### Step 3: Initialize Git in Webapp Folder

Open terminal/command prompt in the `webapp` folder:

```bash
cd c:\Users\jmadh\falconhack\webapp

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: ISS SafetyNet webapp for Render deployment"

# Set main branch
git branch -M main

# Add remote (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/iss-safetynet-webapp.git

# Push to GitHub
git push -u origin main
```

### Step 4: Deploy on Render

#### Option A: Automatic Detection (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** (if not already connected)
4. Find and select your `iss-safetynet-webapp` repository
5. Render will auto-detect `render.yaml` and configure everything
6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)

#### Option B: Manual Configuration

If auto-detection doesn't work:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Configure manually:

**Settings:**
```
Name: iss-safetynet
Environment: Python 3
Region: Choose closest to you
Branch: main
Root Directory: (leave empty)
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --keep-alive 5
```

**Advanced Settings:**
```
Python Version: 3.10.0
Auto-Deploy: Yes
Health Check Path: /
```

5. Click **"Create Web Service"**

### Step 5: Monitor Deployment

1. **Watch the build logs** in Render dashboard
2. You should see:
   ```
   ==> Downloading buildpack...
   ==> Installing dependencies...
   ==> Collecting flask
   ==> Collecting gunicorn
   ==> Collecting ultralytics
   ==> Installing collected packages...
   ==> Build successful!
   ==> Starting service...
   ==> Your service is live!
   ```

3. **Common build issues:**
   - ❌ "best.pt not found" → Make sure model file is committed
   - ❌ "Module not found" → Check requirements.txt
   - ❌ "Timeout" → Increase timeout in start command

### Step 6: Test Your Deployment

1. **Get your app URL** from Render (e.g., `https://iss-safetynet.onrender.com`)
2. **Open in browser**
3. **Test features:**
   - Upload an image
   - Try live camera (if on HTTPS)
   - Check detection results
   - Submit feedback

### Step 7: Verify Functionality

✅ **Checklist:**
- [ ] Homepage loads correctly
- [ ] Upload tab works
- [ ] Camera tab appears (may need HTTPS for camera access)
- [ ] Image detection works
- [ ] Results display properly
- [ ] Feedback submission works
- [ ] No console errors

## 🔧 Troubleshooting

### Issue 1: "Application Error" or "Bad Gateway"

**Possible causes:**
- Gunicorn not binding to correct port
- Model file missing
- Dependencies not installed

**Solution:**
1. Check Render logs for specific error
2. Verify `render.yaml` has correct startCommand
3. Ensure `best.pt` is in repository (check file size)
4. Try manual redeploy

### Issue 2: Slow First Load

**Cause:** Free tier instances sleep after inactivity

**Solution:**
- First request may take 30-60 seconds (cold start)
- Subsequent requests will be fast
- Consider upgrading to paid tier for always-on

### Issue 3: Model Loading Timeout

**Cause:** YOLOv8 model takes time to load

**Solution:**
- Already configured with `--timeout 120` in startCommand
- If still timing out, increase to `--timeout 180`

### Issue 4: Camera Not Working

**Cause:** Camera requires HTTPS

**Solution:**
- Render provides HTTPS by default
- If using custom domain, ensure SSL is configured
- On mobile, grant camera permissions when prompted

### Issue 5: Large File Size Warning

**Cause:** `best.pt` model file is large

**Solution:**
- Git LFS (Large File Storage) if file > 100MB
- Or use model download script in build command
- Current model should be < 100MB (YOLOv8n)

## 📊 Expected Performance

**Deployment Time:** 5-10 minutes
**Cold Start:** 30-60 seconds (first request)
**Inference Time:** <1 second
**Memory Usage:** ~500MB
**Instance Type:** Free tier is sufficient

## 🎯 Post-Deployment

### Update Your Presentation

Add the live demo URL to your:
- PPT slides
- README.md
- GitHub repository description
- Hackathon submission

### Monitor Usage

Check Render dashboard for:
- Request count
- Error rate
- Response time
- Build history

### Continuous Deployment

Any push to `main` branch will auto-deploy:
```bash
# Make changes
git add .
git commit -m "Update: description"
git push
```

## 🔐 Security Notes

- No API keys required
- Model weights are public (for hackathon)
- No user authentication needed
- Feedback data stored locally (not sensitive)

## 💡 Tips

1. **Test locally first** before deploying
2. **Use descriptive commit messages**
3. **Monitor Render logs** during deployment
4. **Keep model file optimized** (use YOLOv8n, not larger variants)
5. **Document your deployment URL** for submission

## 📞 Support

If deployment fails:
1. Check Render logs (most informative)
2. Verify all files are committed
3. Test locally with same Python version
4. Review this guide step-by-step

## ✅ Success Criteria

Your deployment is successful when:
- ✅ URL is accessible
- ✅ Homepage loads with UI
- ✅ Image upload works
- ✅ Detection returns results
- ✅ No errors in browser console
- ✅ Render shows "Live" status

---

**Good luck with your deployment! 🚀**

Your live demo URL will be: `https://YOUR-APP-NAME.onrender.com`
