# Extract-Prompt-To-Emotion

Vietnamese Sentiment Analysis Assistant using Hybrid Model (PhoBERT + Rule-based).

## Features
- Preprocessing: Noise removal, teencode normalization, word segmentation.
- Hybrid sentiment analysis: Combines PhoBERT (DL) and rule-based for high accuracy.
- Streamlit UI: Easy-to-use interface for classification and history.
- SQLite storage: Local history of classifications.

## Installation
1. Install Python 3.8+.
2. Clone repo and cd into it.
3. Create venv: `python -m venv .venv`
4. Activate: `.venv\Scripts\activate` (Windows)
5. Install deps: `pip install -r requirements.txt`

## Usage
Run the app: `streamlit run app.py`

Input Vietnamese text, get sentiment label with confidence.

## Accuracy
Achieved ~94% on test cases. Targets >=95% with fusion.

## Files
- `app.py`: Streamlit UI
- `preprocessing.py`: Text preprocessing
- `phobert_module.py`: PhoBERT sentiment
- `rule_based.py`: Rule-based sentiment
- `fusion.py`: Conditional fusion
- `db_connector.py`: SQLite DB
- `test.py`: Evaluation