# Groq Setup Guide (FREE LLM API)

Groq provides a **completely free** API with generous rate limits for AI inference. It's OpenAI-compatible and much faster than most alternatives.

## Why Groq?

✅ **100% Free** - No credit card required
✅ **Fast** - Up to 750 tokens/second
✅ **Generous Limits** - 30 requests/minute on free tier
✅ **OpenAI Compatible** - Works with existing OpenAI code
✅ **High Quality** - Access to Llama 3.1 and other great models

## Getting Your Free API Key

1. **Sign up at**: https://console.groq.com/
   - No credit card required
   - Free tier is permanent

2. **Get your API key**:
   - Go to https://console.groq.com/keys
   - Click "Create API Key"
   - Give it a name (e.g., "job-miner")
   - Copy the key immediately

3. **Add to GitHub Secrets** (for automated runs):
   - Go to your repository settings
   - Navigate to: Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `GROQ_API_KEY`
   - Value: paste your API key
   - Click "Add secret"

4. **Add to local .env file** (for local runs):
   ```bash
   echo "GROQ_API_KEY=your-api-key-here" >> .env
   ```

## Available Models

The default model is `llama-3.1-8b-instant` (fast and accurate), but you can change it:

- `llama-3.1-70b-versatile` - Larger, more capable
- `llama-3.1-8b-instant` - Fast and efficient (default)
- `mixtral-8x7b-32768` - Good for long contexts
- `gemma2-9b-it` - Google's Gemma model

To change the model, set in your `.env`:
```bash
GROQ_MODEL=llama-3.1-70b-versatile
```

## Rate Limits (Free Tier)

- 30 requests per minute
- 14,400 tokens per minute
- No monthly cap!

This is more than enough for the job scraper running daily.

## Testing Your Setup

```bash
# Make sure you have the API key set
export GROQ_API_KEY="your-key-here"

# Run the scraper
python -m jobminer.main
```

You should see: `Initialized Groq filter with model: llama-3.1-8b-instant (FREE)`

## Troubleshooting

**Error: "Groq API key not configured"**
- Make sure your `.env` file has `GROQ_API_KEY=...`
- Or set environment variable: `export GROQ_API_KEY=...`

**Error: "Rate limit exceeded"**
- Free tier: 30 requests/minute
- Wait a minute and try again
- The scraper automatically handles rate limits

**Want to use Ollama locally instead?**
- Install Ollama: https://ollama.ai
- Pull a model: `ollama pull llama2`
- Remove/comment out `GROQ_API_KEY` from `.env`
- The scraper will automatically use Ollama

## Links

- Groq Console: https://console.groq.com/
- Groq Documentation: https://console.groq.com/docs
- Supported Models: https://console.groq.com/docs/models
