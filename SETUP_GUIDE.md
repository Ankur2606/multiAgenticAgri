# 🚀 Quick Setup Guide for Agricultural Multi-Agent API

## 🔧 Prerequisites

1. **Python 3.8+** installed
2. **Google AI API Key** (required for Gemini models)
3. **Virtual environment** activated

## 📋 Setup Steps

### 1. Create Environment File
```bash
# Copy the template
copy .env.template .env

# Edit .env file and add your Google AI API key
notepad .env
```

### 2. Get Google AI API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste it in your `.env` file:
   ```
   GOOGLE_AI_API_KEY=your_actual_api_key_here
   ```

### 3. Install Dependencies
```bash
pip install -r requirements_api.txt
```

### 4. Start the API Server
```bash
python api_server.py
```

### 5. Test the API
```bash
python test_api_client.py
```

## 🐛 Troubleshooting

### Issue: Agent Response is None
**Cause**: Missing or invalid Google AI API key
**Solution**: 
1. Check your `.env` file exists
2. Verify the API key is correct
3. Check server logs for authentication errors

### Issue: Import Errors
**Cause**: Missing dependencies or incorrect agent imports
**Solution**:
1. Reinstall dependencies: `pip install -r requirements_api.txt`
2. Check all sub-agent imports in `agent.py`

### Issue: Connection Refused
**Cause**: API server not running
**Solution**: Start the server with `python api_server.py`

## 📊 Testing

The test client will now show detailed error information:
- ✅ **Success**: Agent responds normally
- ❌ **Error**: Shows specific error message
- 🔍 **Debug**: Detailed response analysis

## 🌐 API Endpoints

- **Health Check**: http://localhost:8000/
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_AI_API_KEY` | ✅ Yes | Google AI API key for Gemini models |
| `GOOGLE_CLOUD_PROJECT` | ❌ Optional | Google Cloud project ID |
| `DEBUG` | ❌ Optional | Enable debug logging |

## 📝 Next Steps

1. Configure your Google AI API key
2. Start the server
3. Run the tests
4. Check the interactive documentation
5. Start building your agricultural applications!

Happy farming! 🌾
