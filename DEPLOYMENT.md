# Streamlit Deployment Guide

## 🚀 Deploy to Streamlit Community Cloud

### Prerequisites
- GitHub account
- This repository pushed to GitHub
- OpenAI API key

### Step-by-Step Deployment

#### 1. Prepare Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Add Streamlit app with rate limiting"
git push origin main
```

#### 2. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository: `dmatekenya/chichewa-RAG-based-chatbot`
   - Branch: `main`
   - Main file path: `app.py`

3. **Add Secrets**
   - In app settings, go to "Secrets" section
   - Add your environment variables in TOML format:
   
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   LANGSMITH_TRACING = "true"
   LANGSMITH_API_KEY = "your-langsmith-key-here"
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-5 minutes)
   - Your app will be live at: `https://your-app-name.streamlit.app`

#### 3. Monitor Usage

**Important:** You're paying for all OpenAI API calls!

**Built-in Protection:**
- ✅ 20 queries per session limit
- ✅ 10 queries per hour per user
- ✅ Usage stats in sidebar

**Monitor Costs:**
- Check OpenAI dashboard: https://platform.openai.com/usage
- Set up billing alerts
- Consider adding daily spending limits

---

## 🏠 Run Locally (for testing)

### 1. Create Local Secrets File
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 2. Edit `.streamlit/secrets.toml`
Add your actual API keys (this file is in .gitignore):
```toml
OPENAI_API_KEY = "sk-your-actual-key"
LANGSMITH_TRACING = "true"
LANGSMITH_API_KEY = "your-langsmith-key"
```

### 3. Run Streamlit
```bash
source venv/bin/activate
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🔒 Security Best Practices

### Secrets Management
- ✅ Never commit `.streamlit/secrets.toml` to git (already in .gitignore)
- ✅ Never commit `.env` with real keys to git (already in .gitignore)
- ✅ Use Streamlit Cloud secrets for deployment
- ✅ Rotate API keys if accidentally exposed

### Rate Limiting
Current limits (configurable in `app.py`):
- **Session limit**: 20 queries per session
- **Hourly limit**: 10 queries per hour per user

To adjust limits, edit these variables in `app.py`:
```python
MAX_QUERIES_PER_SESSION = 20  # Adjust as needed
MAX_QUERIES_PER_HOUR = 10     # Adjust as needed
```

### Cost Control
1. **Set OpenAI spending limits**
   - Go to: https://platform.openai.com/account/limits
   - Set monthly budget

2. **Monitor usage**
   - Check dashboard daily initially
   - Set up email alerts for unusual usage

3. **Consider alternatives if costs are high**
   - Require users to enter their own API keys
   - Use cheaper models (gpt-3.5-turbo instead of gpt-4)
   - Add stricter rate limits

---

## 📊 Usage Monitoring

### In-App Stats
Users can see their usage in the sidebar:
- Queries used in current session
- Queries used in last hour
- Session duration

### OpenAI Dashboard
Monitor actual costs:
- Visit: https://platform.openai.com/usage
- Check daily/monthly usage
- Review cost by model

### LangSmith (Optional)
If enabled, view detailed traces:
- Visit: https://smith.langchain.com
- See all queries, translations, and responses
- Debug issues

---

## 🔧 Troubleshooting

### App Won't Start
- Check if vector store exists: `data/vectorstore/`
- Run: `python src/document_processor.py` to create it
- Make sure all documents are in `data/docs/`

### Rate Limit Not Working
- Check browser cookies/cache
- Each browser/device gets separate limits
- Consider IP-based tracking for stricter limits

### High API Costs
- Review logs in OpenAI dashboard
- Check if rate limits need to be stricter
- Consider switching to gpt-3.5-turbo (cheaper)

### Deployment Fails
- Ensure `requirements.txt` is up to date
- Check Streamlit Cloud logs
- Verify secrets are properly set

---

## 📝 Updating the Deployed App

```bash
# Make changes to your code
git add .
git commit -m "Update app"
git push origin main

# Streamlit Cloud will auto-redeploy within ~1 minute
```

---

## 💰 Cost Estimates

**Rough estimates per query:**
- Translation (2x GPT-4 calls): ~$0.002
- Embeddings (retrieval): ~$0.0001
- Answer generation (GPT-4): ~$0.01
- **Total per query: ~$0.012**

**With rate limits:**
- 10 queries/hour/user
- 100 unique users/day
- = 1,000 queries/day
- = **~$12/day** or **~$360/month**

**To reduce costs:**
- Use gpt-3.5-turbo instead of gpt-4
- Stricter rate limits
- Cache common translations

---

## 🎉 Share Your App

Once deployed, share your app URL:
```
https://your-app-name.streamlit.app
```

Users can:
- Ask questions in Chichewa
- Get answers about your news articles
- No API key required from them
- Subject to rate limits you set
