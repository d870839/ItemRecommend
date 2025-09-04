# LLM Integration Setup Guide

## Overview
The app now supports dynamic AI-generated recommendations using Claude (Anthropic) API. When configured, it will generate completely new, wild food combinations on the fly instead of using hardcoded recommendations.

## Setup Instructions

### 1. Get Anthropic API Key
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

### 2. Configure Environment Variable

#### For Local Development:
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Windows Command Prompt
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

#### For Render Deployment:
1. Go to your Render dashboard
2. Select your service
3. Go to Environment tab
4. Add new environment variable:
   - Key: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-your-key-here`

### 3. Test the Integration
1. Start the Flask app: `python app.py`
2. Open http://localhost:5000
3. Click "Get New Recommendation"
4. You should see "🤖 Using AI to create wild new combinations..." during loading
5. The stats section should show "🤖 AI-Powered Recommendations Active"

## How It Works

### With LLM Enabled:
- Claude generates completely new, wild food combinations
- Each recommendation is unique and never repeated
- Uses advanced prompting to ensure maximum creativity
- Falls back to hardcoded recommendations if API fails

### Without LLM (Fallback Mode):
- Uses the curated list of 65+ hardcoded recommendations
- Still provides wild and innovative suggestions
- No API key required
- More reliable for basic usage

## API Costs
- Claude API charges per token used
- Each recommendation costs approximately $0.01-0.03
- Very cost-effective for the level of creativity provided

## Troubleshooting

### "Using Curated Recommendations" shows instead of AI
- Check that ANTHROPIC_API_KEY is set correctly
- Verify the API key is valid and has credits
- Check the console for error messages

### API errors
- Ensure you have sufficient credits in your Anthropic account
- Check your internet connection
- Verify the API key format (should start with `sk-ant-`)

### Slow responses
- LLM calls take 2-5 seconds vs instant hardcoded
- This is normal for AI generation
- Consider the trade-off between speed and creativity

## Customization

You can modify the AI prompt in `app.py` in the `generate_llm_recommendation()` function to:
- Change the level of wildness
- Focus on specific categories
- Adjust the creativity level
- Add specific requirements

## Security Notes
- Never commit your API key to version control
- Use environment variables for all sensitive data
- Consider using a secrets management service for production
