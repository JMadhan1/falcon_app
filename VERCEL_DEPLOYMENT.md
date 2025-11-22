# Vercel Deployment Guide

## 🚀 Deploy Flask Object Detection App to Vercel

This guide will help you deploy your Flask application with YOLOv8 object detection to Vercel.

---

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional): Install with `npm i -g vercel`
3. **GitHub Repository**: Your code should be pushed to GitHub

---

## 🔧 Configuration Files

The following files have been created for Vercel deployment:

### 1. `vercel.json`
Configures Vercel to use Python runtime and route all requests to the Flask app.

### 2. `api/index.py`
Entry point for Vercel serverless functions. Imports and exposes the Flask app.

### 3. `.vercelignore`
Excludes unnecessary files from deployment (similar to `.gitignore`).

---

## 📦 Important Notes About Vercel

### ⚠️ Limitations to Consider:

1. **File Size Limits**:
   - Your `best.pt` model file is ~6MB, which is within Vercel's limits
   - Serverless function size limit: 50MB (uncompressed)
   - If deployment fails due to size, consider using Vercel Blob Storage

2. **Execution Time**:
   - Vercel serverless functions have a 10-second timeout on Hobby plan
   - 60-second timeout on Pro plan
   - YOLO inference should complete within these limits for most images

3. **File System**:
   - Vercel uses a read-only file system
   - Uploads and feedback data won't persist between requests
   - Consider using Vercel Blob Storage or external storage (S3, etc.)

---

## 🌐 Deployment Methods

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**:
   - Visit [vercel.com/new](https://vercel.com/new)

2. **Import Git Repository**:
   - Click "Import Project"
   - Select your GitHub repository: `JMadhan1/falcon_app`
   - Click "Import"

3. **Configure Project**:
   - **Framework Preset**: Select "Other"
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete (~2-3 minutes)

5. **Access Your App**:
   - Vercel will provide a URL like: `https://falcon-app-xxx.vercel.app`

---

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```
   - Follow the prompts
   - Confirm project settings
   - Wait for deployment

4. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

## 🔄 Handling File Uploads & Persistence

Since Vercel's file system is read-only, you'll need to modify the app for production:

### Option 1: Use Vercel Blob Storage

1. Install Vercel Blob SDK:
   ```bash
   pip install vercel-blob
   ```

2. Update `app.py` to use Blob storage instead of local file system

### Option 2: Use External Storage (S3, Cloudinary, etc.)

Modify the upload handling in `app.py` to upload to external storage.

### Option 3: Return Images Without Saving

For a simple deployment, you can skip saving files and just return detection results.

---

## 🛠️ Recommended Changes for Production

### 1. Update `app.py` for Vercel

Add this at the top of `app.py`:

```python
# Vercel-specific configuration
if os.environ.get('VERCEL'):
    # Use /tmp directory for temporary files (writable on Vercel)
    UPLOAD_FOLDER = '/tmp/uploads'
    FEEDBACK_FOLDER = '/tmp/feedback_data'
```

### 2. Disable Debug Mode

Change the last line in `app.py`:

```python
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False
```

---

## 🧪 Testing Locally Before Deployment

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Run Local Development Server**:
   ```bash
   vercel dev
   ```

3. **Test the App**:
   - Open `http://localhost:3000`
   - Upload an image and test detection

---

## 📊 Monitoring & Logs

1. **View Logs**:
   - Go to Vercel Dashboard → Your Project → Deployments
   - Click on a deployment → "Functions" tab → View logs

2. **Real-time Logs** (CLI):
   ```bash
   vercel logs
   ```

---

## 🔐 Environment Variables

If you need to add environment variables:

1. **Via Dashboard**:
   - Go to Project Settings → Environment Variables
   - Add variables like `MODEL_PATH`, `API_KEY`, etc.

2. **Via CLI**:
   ```bash
   vercel env add MODEL_PATH
   ```

---

## 🚨 Troubleshooting

### Issue: "Module not found" error

**Solution**: Ensure all dependencies are in `requirements.txt`

### Issue: "Function timeout"

**Solution**: 
- Optimize YOLO inference
- Reduce image size before processing
- Upgrade to Vercel Pro for 60s timeout

### Issue: "File system is read-only"

**Solution**: Use `/tmp` directory or external storage

### Issue: Model file too large

**Solution**: 
- Use Vercel Blob Storage
- Host model file externally (S3, Google Cloud Storage)
- Load model from URL

---

## 📝 Next Steps After Deployment

1. **Custom Domain**: Add a custom domain in Vercel Dashboard
2. **Analytics**: Enable Vercel Analytics for traffic insights
3. **Monitoring**: Set up error tracking (Sentry, etc.)
4. **Scaling**: Monitor usage and upgrade plan if needed

---

## 🎯 Quick Deployment Checklist

- [ ] Push all code to GitHub
- [ ] Verify `vercel.json` is present
- [ ] Verify `api/index.py` is present
- [ ] Check `requirements.txt` has all dependencies
- [ ] Go to [vercel.com/new](https://vercel.com/new)
- [ ] Import GitHub repository
- [ ] Click Deploy
- [ ] Test the deployed app
- [ ] Share the Vercel URL!

---

## 🔗 Useful Links

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel Blob Storage](https://vercel.com/docs/storage/vercel-blob)
- [Vercel CLI Reference](https://vercel.com/docs/cli)

---

## 💡 Alternative: If Vercel Doesn't Work

If you encounter issues with Vercel (model size, timeout, etc.), consider:

1. **Render** - Better for ML apps, longer timeouts
2. **Railway** - Good for Python apps with large dependencies
3. **Hugging Face Spaces** - Optimized for ML models
4. **Google Cloud Run** - Scalable container deployment

---

**Happy Deploying! 🚀**
