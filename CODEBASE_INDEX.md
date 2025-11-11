# Vietnamese Sentiment Analysis - Codebase Index

## 📁 Project Overview
A comprehensive Vietnamese sentiment analysis system using hybrid PhoBERT + rule-based approach, achieving 95.80% accuracy.

## 🏗️ Architecture

### Core Components
```
app.py                 # Main Streamlit application (242 lines)
├── preprocessing.py   # Text preprocessing utilities (89 lines)
├── phobert_module.py  # PhoBERT sentiment analysis (45 lines)
├── rule_based.py      # Rule-based sentiment analysis (129 lines)
├── fusion.py          # Model fusion logic (55 lines)
└── db_connector.py    # SQLite database operations (49 lines)
```

### Configuration & Assets
```
requirements.txt       # Python dependencies (6 lines)
.streamlit/config.toml # Streamlit configuration (18 lines)
.gitignore            # Git ignore patterns (25 lines)
README.md             # Project documentation (85 lines)
```

### Testing Suite
```
test/
├── test_1000_prompts.py          # Main evaluation script (68 lines)
└── test_1000_prompts_refined.txt # Test dataset (1000 prompts)
```

## 📊 Code Metrics

### Lines of Code (LOC)
- **Total**: ~700+ lines
- **Core Logic**: ~380 lines
- **UI/Interface**: ~242 lines
- **Tests**: ~68 lines
- **Documentation**: ~85 lines

### Complexity Breakdown
- **Preprocessing**: Text cleaning, normalization, segmentation
- **PhoBERT Module**: Hugging Face model integration
- **Rule-based**: Lexicon with 200+ sentiment words/phrases
- **Fusion**: Conditional logic for model combination
- **Database**: CRUD operations with SQLite
- **UI**: Streamlit tabs, export/import, history management

## 🔧 Key Functions & Classes

### app.py
```python
# Main functions:
- export_to_csv(df)      # CSV export
- export_to_json(df)     # JSON export
- export_to_html(df)     # HTML export
- export_to_ics(df)      # ICS calendar export
- import_from_csv(file)  # CSV import
- import_from_json(file) # JSON import

# UI Components:
- Classification tab with input validation
- History tab with CRUD operations
- Export/import functionality
```

### preprocessing.py
```python
class VietnamesePreprocessor:
    - remove_noise(text)          # Remove URLs, mentions, repeated chars
    - normalize_teencode(text)    # Convert slang to formal Vietnamese
    - word_segmentation(text)     # Tokenize Vietnamese text
    - tokenize(text)              # PhoBERT tokenization
    - preprocess(text)            # Full preprocessing pipeline
```

### phobert_module.py
```python
class PhoBERTModule:
    - __init__(model_name)        # Load PhoBERT model
    - analyze_sentiment(text)     # Return label and confidence
```

### rule_based.py
```python
class RuleBasedSentiment:
    - __init__()                  # Initialize lexicon (200+ entries)
    - is_neutral_context(text)    # Detect neutral/question patterns
    - analyze_sentiment(text)     # Score calculation with negation
    - get_label(score)            # Convert score to POSITIVE/NEGATIVE/NEUTRAL
```

### fusion.py
```python
class ConditionalFusion:
    - fuse(phobert_result, rule_result)  # Combine models with veto logic
```

### db_connector.py
```python
class DBConnector:
    - create_table()              # Initialize SQLite schema
    - insert_history(...)         # Add classification record
    - fetch_history(limit)        # Retrieve recent records
    - delete_by_id(id)            # Remove specific record
    - delete_all()                # Clear all records
```

## 🎯 Key Features

### Input Validation (NEW)
- **Spam Detection**: Detects random characters, keyboard mashing
- **Length Validation**: Minimum 2 characters, maximum reasonable length
- **Content Check**: Ensures meaningful Vietnamese text
- **Error Messages**: User-friendly pop-up warnings

### Sentiment Analysis Pipeline
1. **Input Validation** → Reject invalid/spam input
2. **Preprocessing** → Clean and normalize text
3. **Parallel Analysis** → PhoBERT + Rule-based scoring
4. **Fusion** → Conditional combination with veto logic
5. **Output** → Final label with confidence score
6. **Storage** → Save to SQLite database

### Export/Import System
- **Formats**: CSV, JSON, HTML, ICS calendar
- **Bulk Operations**: Import multiple records
- **Data Integrity**: Validation during import

## 🔍 Data Flow

```
User Input
    ↓
Input Validation (Spam/Length/Content Check)
    ↓
Preprocessing (Clean → Normalize → Segment)
    ↓
Parallel Processing:
├── PhoBERT Analysis (Deep Learning)
└── Rule-based Analysis (Lexicon Matching)
    ↓
Conditional Fusion (Veto + Neutral Priority)
    ↓
Final Result (Label + Confidence)
    ↓
Database Storage + UI Display
```

## 🧪 Test Coverage

### Test Dataset
- **1000 diverse prompts** covering:
  - Standard Vietnamese text
  - Toxic/profane language
  - Slang and teencode
  - Questions and neutral statements
  - Edge cases and mixed sentiments

### Performance Metrics
- **Overall Accuracy**: 95.80%
- **Category Breakdown**:
  - Positive: 85.71%
  - Negative: 98.72%
  - Neutral: 98.70%

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
- Repository: https://github.com/d0ngle8k/Extract-Prompt-To-Emotion
- Entry point: `app.py`
- Requirements: `requirements.txt`
- Configuration: `.streamlit/config.toml`

## 📋 Dependencies

```txt
streamlit>=1.28.0      # Web framework
transformers>=4.21.0   # Hugging Face models
torch>=1.12.0          # PyTorch backend
underthesea>=6.8.0     # Vietnamese NLP
pandas>=1.5.0          # Data manipulation
numpy>=1.21.0          # Numerical operations
```

## 🔐 Security & Privacy

- **No external API calls** during analysis
- **Local model inference** (PhoBERT runs locally)
- **SQLite storage** (no cloud database dependency)
- **Input sanitization** prevents malicious content

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop/mobile
- **Real-time Feedback**: Instant sentiment analysis
- **History Management**: View, export, delete records
- **Multi-format Export**: CSV, JSON, HTML, ICS
- **Import Capability**: Bulk data import
- **Error Handling**: User-friendly error messages

## 🔧 Maintenance

### Regular Updates Needed:
- **Model Updates**: PhoBERT fine-tuning for new data
- **Lexicon Expansion**: Add new slang/profane terms
- **Test Dataset**: Update with current language trends
- **Dependency Updates**: Keep packages current

### Monitoring:
- **Accuracy Tracking**: Regular test runs
- **Performance Metrics**: Response time, memory usage
- **User Feedback**: Error reports and feature requests

---

*Last updated: November 11, 2025*
*Total files: 12*
*Codebase health: Excellent ✅*