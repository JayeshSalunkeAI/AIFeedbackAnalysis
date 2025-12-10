# 🎯 AI Feedback System

A production-ready two-dashboard AI-powered feedback system deployed on Render using Perplexity API.

## 📊 Features

### User Dashboard (Public)
- ⭐ Star rating (1-5)
- 📝 Feedback submission form
- 🤖 AI-generated response
- 😊 Sentiment detection
- ✅ Form validation

### Admin Dashboard (Internal)
- 📈 Real-time analytics
- 📊 Charts & visualizations
- 🔍 Advanced filtering
- 📥 Export data (CSV/JSON)
- 💡 AI-suggested recommendations

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **AI API**: Perplexity (sonar-pro)
- **Deployment**: Render


## 🎯 Key Endpoints

- **User Dashboard**: Select "⭐ User Dashboard" from sidebar
- **Admin Dashboard**: Select "📊 Admin Dashboard" from sidebar

## 🔐 Environment Variables

```bash
PERPLEXITY_API_KEY=sk-xxxxx...  # Required
PYTHON_VERSION=3.10.14          # Optional
```

## 📊 Database Schema

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    email TEXT,
    category TEXT NOT NULL,
    rating INTEGER (1-5),
    message TEXT NOT NULL,
    sentiment TEXT (positive|negative|neutral),
    summary TEXT,
    ai_response TEXT,
    recommendations TEXT,
    created_at TIMESTAMP
)
```

## 🎨 UI Components

### User Dashboard
- Name input
- Email input (optional)
- Category dropdown
- Star rating slider
- Textarea for feedback
- Submit button
- Success confirmation with AI response

### Admin Dashboard
- Key metrics (total, avg rating, satisfaction %)
- Charts (rating, sentiment, category)
- Filters (category, sentiment, rating range)
- Detailed feedback list with actions
- Export buttons (CSV, JSON)

## 🤖 AI Features

1. **Sentiment Analysis**: Detects positive/negative/neutral
2. **AI Response**: Generates professional customer service response
3. **Summary**: Creates one-sentence review summary
4. **Recommendations**: Suggests actionable items for team

## 📈 Analytics

- Rating distribution
- Sentiment breakdown
- Category performance
- Satisfaction rate (4-5 stars)
- Time-based trends
- Top categories

## 🐛 Troubleshooting

### API Key Error
```
Export PERPLEXITY_API_KEY in environment
Or add to Render environment variables
```

### Module Not Found
```
Check utils/__init__.py exists
Ensure correct Python path in app.py
```

### Port Already in Use
```
Render uses port 10000
Verify Start Command includes: --server.port 10000 --server.address 0.0.0.0
```

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application with both dashboards |
| `database.py` | SQLite CRUD operations |
| `perplexity_client.py` | Perplexity API integration |
| `analytics.py` | Data analysis and visualization helpers |
| `requirements.txt` | Python package dependencies |
| `runtime.txt` | Python version specification |

## 🚀 Deployment Checklist

- [x] Perplexity API key obtained
- [x] GitHub repository created
- [x] All files structured correctly
- [x] Environment variables configured
- [x] Render deployment configured
- [x] Both dashboards tested
- [x] AI features working
- [x] Database persisting data

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Perplexity API**: https://docs.perplexity.ai
- **GitHub Issues**: Check repository issues

## 📄 License

This project is open source and available under the MIT License.


---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: December 2025

