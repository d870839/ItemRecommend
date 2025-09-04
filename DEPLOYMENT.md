# Deployment Guide for Render.com

## Quick Deploy to Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/private-selection-recommender.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the configuration from `render.yaml`
   - Click "Create Web Service"

3. **Your app will be live!**
   - Render will provide a public URL like `https://your-app-name.onrender.com`
   - The app will automatically restart when you push changes to GitHub

## Manual Configuration (if needed)

If auto-detection doesn't work, use these settings:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment**: `Python 3`
- **Plan**: `Free` (or upgrade as needed)

## Environment Variables

No environment variables are required for this app to run.

## Monitoring

- Check the Render dashboard for logs and metrics
- The app will automatically restart if it crashes
- Free tier includes 750 hours/month

## Troubleshooting

- **App won't start**: Check the logs in Render dashboard
- **Static files not loading**: Ensure `templates/` folder is in the root directory
- **Port issues**: The app uses port 5000, which Render handles automatically
