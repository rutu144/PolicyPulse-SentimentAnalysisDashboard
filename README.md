# PolicyPulse | Sentiment Analysis Dashboard

**PolicyPulse** is a web-based application designed to analyze public sentiment toward government policies using the TweetEval dataset. It uses a BERT-based model to classify tweets as Positive, Neutral, or Negative and offers interactive visualizations such as sentiment trends, word clouds, and topic modeling.

---

## Features

* **Policy Filtering**: GST, Digital India, Make in India, Swachh Bharat.
* **Sentiment Analysis**: Positive, Neutral, Negative sentiment metrics and categorized tweet tables.
* **Interactive Filters**: Search by keyword, sentiment, and date range.
* **Visualizations**: Sentiment trends and word clouds.
* **Topic Modeling**: LDA-based key topic extraction.
* **Data Export**: Download filtered tweets as CSV.
* **Modern UI**: Gradient headers, hover effects, tooltips, and loading spinners.

---

## Tech Stack

* **Backend**: Flask (Python)
* **Frontend**: HTML, Bootstrap 5, CSS, JS
* **Processing**: Pandas, NumPy, NLTK, spaCy
* **Model**: BERT (Hugging Face Transformers) - Accuracy: 0.6657
* **Visualization**: Matplotlib, WordCloud
* **Dataset**: TweetEval Sentiment Dataset (preprocessed)

---

## Prerequisites

* Python 3.8+ (Recommended: 3.10)
* pip
* virtualenv (recommended)
* Git
* Modern web browser
* Internet access

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PolicyPulse-SentimentAnalysisDashboard.git
cd PolicyPulse-SentimentAnalysisDashboard
```

### Step 2: Create a Virtual Environment

#### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Dataset Setup

### Step 4: Download TweetEval Dataset

```bash
python data/dummy/download_tweeteval.py
```

**Creates:**

* `data/dummy/tweeteval_train.csv`
* `data/dummy/tweeteval_val.csv`
* `data/dummy/tweeteval_test.csv`

### Step 5: Preprocess Dataset

```bash
python data/dummy/preprocess_dummy.py
```

**Generates:**

* `data/processed/filtered_tweeteval.csv`
* `data/processed/preprocessed_tweeteval.csv`

**Verify Output:**

```bash
python -c "import pandas as pd; df = pd.read_csv('data/processed/preprocessed_tweeteval.csv'); print('Columns:', df.columns); print('Label counts:', df['label'].value_counts()); print('Policy counts:', df['policy'].value_counts())"
```

---

## Train the BERT Model

### Step 6: Train

```bash
python src/train_bert.py
```

**Trains for 3 epochs and saves to:** `models/bert_sentiment/`

**Expected Output:**

```text
Validation Accuracy: 0.6657
```

---

## Theme Extraction

### Step 7: Extract Topics and Keywords

```bash
python src/theme_extraction.py
```

**Output Sample:**

```text
GST Themes:
Keywords: [('tax reform', 150), ('digital payment', 120), ...]
Topics: ['Topic 1: tax, reform, policy', 'Topic 2: digital, india, tech', ...]
```

---

## Running the Dashboard

### Step 1: Activate Environment

#### On Windows

```bash
venv\Scripts\activate
```

#### On macOS/Linux

```bash
source venv/bin/activate
```

### Step 2: Run Flask App

```bash
python src/app.py
```

Visit: http://127.0.0.1:5000

---

## Interacting with the Dashboard

* **Select Policy** (e.g., GST)
* **Search Tweets** by keyword
* **Filter by Sentiment**
* **Set Date Range**
* **Click Apply/Reset Filters**
* **Download CSV**

---

© 2025 Rutuja Vaidya, Viraj Gujar, Tejas Bagul | BERT + TweetEval + Flask = 📈 Insightful Policy Sentiment Analysis
