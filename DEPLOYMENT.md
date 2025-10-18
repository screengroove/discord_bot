# Railway Deployment Guide

This guide will help you deploy your Discord bot to Railway.app in under 5 minutes.

## Prerequisites

- GitHub account
- Discord bot token (from Discord Developer Portal)
- OpenRouter API key (from OpenRouter.ai)

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

Your code should already be on GitHub. If not:

```bash
git remote add origin https://github.com/YOUR_USERNAME/discord_bot.git
git branch -M main
git push -u origin main
```

**IMPORTANT**: Never commit your `.env` file! (it's already in `.gitignore` ✅)

### 2. Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" and sign in with your GitHub account
3. Authorize Railway to access your GitHub repositories

### 3. Create a New Project

1. Click "New Project" button
2. Select "Deploy from GitHub repo"
3. Choose your `discord_bot` repository
4. Railway will automatically detect your Python project

### 4. Add Environment Variables

**CRITICAL STEP**: Copy values from your local `.env` file:

1. In Railway dashboard, click on your service
2. Go to the "Variables" tab
3. Click "RAW Editor"
4. **Open your local `.env` file** and copy ALL the contents
5. Paste into Railway's RAW Editor

Your variables should look like this (with YOUR actual values):
```
DISCORD_TOKEN=your_actual_token_here
DISCORD_CLIENT_ID=your_actual_client_id
OPENROUTER_API_KEY=your_actual_api_key
BOT_PREFIX=!
LOG_LEVEL=INFO
```

### 5. Deploy!

Railway will automatically:
- ✅ Install dependencies from `requirements.txt`
- ✅ Run your bot using `Procfile`
- ✅ Keep your bot running 24/7
- ✅ Auto-restart on crashes

### 6. Verify Deployment

Check the logs in Railway dashboard. You should see:
```
INFO - Using OpenRouter API
INFO - Fetching available models...
INFO - YourBot#1234 has connected to Discord!
```

## Troubleshooting

### Bot not responding
- Verify environment variables are set correctly in Railway
- Check that Message Content Intent is enabled in Discord Developer Portal

### "No valid API key found"
- Ensure `OPENROUTER_API_KEY` is set in Railway variables
- No extra spaces or quotes around values

### Bot keeps restarting
- Check Railway logs for errors
- Invalid Discord token? Regenerate in Discord Developer Portal

## Security Best Practices

- ✅ Never commit `.env` to git (already in `.gitignore`)
- ✅ Never share tokens publicly
- ✅ If tokens are exposed, regenerate immediately
- ✅ Use Railway's encrypted variables for secrets

## Cost

Railway provides $5/month free credit (usually sufficient for small Discord bots).

## Updating Your Bot

```bash
git add .
git commit -m "Update features"
git push
```

Railway auto-deploys on push! 🚀

## Need Help?

- Railway Docs: https://docs.railway.app
- Discord.py Docs: https://discordpy.readthedocs.io/
- OpenRouter Docs: https://openrouter.ai/docs
