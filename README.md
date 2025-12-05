# Vietnamese Sentiment Analysis Assistant 🎭

A powerful hybrid sentiment analysis system for Vietnamese text using PhoBERT + Rule-based approach, achieving **95.80% accuracy** on diverse test cases.

## ✨ Features

- **Hybrid Model**: Combines deep learning (PhoBERT) with rule-based analysis for optimal accuracy
- **Advanced Preprocessing**: Noise removal, teencode normalization, word segmentation
- **Streamlit Web App**: Beautiful, user-friendly interface
- **History Management**: SQLite-based storage with export/import capabilities
- **Multi-format Export**: CSV, JSON, HTML, ICS calendar format
- **Comprehensive Testing**: 1000+ diverse prompts validation

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/d0ngle8k/Extract-Prompt-To-Emotion.git
cd Extract-Prompt-To-Emotion

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### 🌐 Deploy to Streamlit Cloud

1. **Fork this repository** on GitHub
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Connect your GitHub account**
4. **Select this repository**
5. **Deploy!** (Streamlit will automatically detect `app.py` as the entry point)

#### ⚠️ Streamlit Cloud Notes:
- **Free tier limitations**: Model loading may take time on first run
- **Data persistence**: History data doesn't persist between sessions (cloud limitation)
- **Memory usage**: PhoBERT model requires ~2GB RAM, ensure adequate resources

## 📊 Performance

- **Overall Accuracy**: 95.80%
- **Positive**: 85.71%
- **Negative**: 98.72%
- **Neutral**: 98.70%

Tested on 1000 diverse Vietnamese prompts including standard text, toxic language, slang, and edge cases.

## 🏗️ Architecture

```
app.py              # Streamlit web interface
├── preprocessing.py # Text cleaning & segmentation
├── phobert_module.py # Hugging Face PhoBERT integration
├── rule_based.py    # Lexicon-based sentiment analysis
├── fusion.py        # Conditional model fusion
└── db_connector.py  # SQLite database operations
```

## 📁 Project Structure

```
Extract-Prompt-To-Emotion/
├── app.py                 # Main Streamlit application
├── preprocessing.py       # Vietnamese text preprocessing
├── phobert_module.py      # PhoBERT sentiment analysis
├── rule_based.py          # Rule-based sentiment analysis
├── fusion.py              # Model fusion logic
├── db_connector.py        # Database operations
├── requirements.txt       # Python dependencies
├── .streamlit/config.toml # Streamlit configuration
├── test/                  # Test suite
│   ├── test_1000_prompts.py
│   └── test_1000_prompts_refined.txt
├── phobert_finetuned/     # Pre-trained model files
└── README.md
```

## 🔧 Dependencies

- `streamlit`: Web app framework
- `transformers`: Hugging Face models
- `torch`: PyTorch for deep learning
- `underthesea`: Vietnamese NLP toolkit
- `pandas`: Data manipulation
- `numpy`: Numerical operations

## 🎯 Usage

1. **Classification Tab**: Input Vietnamese text and get instant sentiment analysis
2. **History Tab**: View past classifications with export options
3. **Export Data**: Download history in CSV, JSON, HTML, or ICS format
4. **Import Data**: Upload CSV/JSON files to add historical data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify.    


## 🙏 Acknowledgments

- [PhoBERT](https://github.com/VinAIResearch/PhoBERT) by VinAI Research
- [Underthesea](https://github.com/undertheseanlp/underthesea) Vietnamese NLP toolkit
- [Streamlit](https://streamlit.io/) for the amazing web app framework
