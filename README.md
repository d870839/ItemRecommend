# Private Selection Item Recommender

A Flask web application that provides AI-powered recommendations for new Private Selection products based on current food trends and market analysis.

## Features

- 🎯 **Random Recommendations**: Get a new product recommendation with each click
- 🤖 **AI-Powered**: Optional Claude integration for dynamic, wild recommendations
- 🎆 **Fireworks Animation**: Celebratory animations when recommendations appear
- 📊 **No Repeat Logic**: Ensures you never get the same recommendation twice in a row
- 🚀 **Ready for Render**: Optimized for deployment on Render.com
- 💾 **No Database Required**: All data stored in memory for simplicity
- 🔄 **Fallback Mode**: Works with or without LLM integration

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser to `http://localhost:5000`

## Deployment on Render

1. Push your code to a GitHub repository
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` configuration
4. Your app will be deployed and available at a public URL

## Product Categories

The recommender includes 35+ product recommendations across 6 categories:

- **Plant-Based** (High Priority): Plant-based alternatives to meat and dairy
- **Functional Foods** (High Priority): Health-focused products with added benefits
- **Global Fusion** (Medium Priority): International flavors and ethnic cuisine
- **Sustainable** (Medium Priority): Zero-waste and eco-friendly products
- **Premium Snacks** (Medium Priority): Artisan and gourmet snack options
- **Frozen Meals** (Low-Medium Priority): Convenience meal solutions

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Integration**: Claude (Anthropic) API
- **Animations**: CSS animations and JavaScript
- **Deployment**: Render.com
- **Data Storage**: In-memory (no database required)

## AI Integration

The app supports optional AI-powered recommendations using Claude:

- **Dynamic Generation**: Creates completely new, wild food combinations
- **No Hardcoding**: Each recommendation is unique and generated on-demand
- **Fallback Mode**: Works without API key using curated recommendations
- **Cost Effective**: ~$0.01-0.03 per recommendation

See [LLM_SETUP.md](LLM_SETUP.md) for detailed setup instructions.

## API Endpoints

- `GET /` - Main application interface
- `POST /recommend` - Get a random product recommendation
- `GET /stats` - Get statistics about available recommendations
