# CreditRisk AI Agent

An AI-powered credit risk assessment application that helps evaluate borrower creditworthiness, predict default probability, and streamline loan approval decisions.

## Features

- **Credit Assessment** - Input borrower data and get instant risk scores
- **Risk Grading** - A/B/C/D/E classification system
- **Default Prediction** - ML-powered default probability estimation
- **Chat Assistant** - AI chatbot for credit policy questions
- **Batch Processing** - Upload CSV files for bulk analysis
- **Analytics Dashboard** - Visual reports and risk distribution charts

## Quick Start

### Local Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd credit-risk-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser at `http://localhost:8501`

## Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Repository pushed to GitHub

### Deployment Steps

1. **Push your code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/credit-risk-agent.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and main file path
   - Click "Deploy!"

Your app will be live at `https://YOUR-USERNAME-credit-risk-agent.streamlit.app`

## Project Structure

```
credit-risk-agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── SPEC.md               # Technical specification
├── utils/
│   ├── scoring.py        # Risk scoring algorithms
│   └── chatbot.py        # Chatbot engine
├── data/
│   └── sample_data.csv   # Sample dataset
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## Usage Guide

### Credit Assessment
1. Navigate to "Credit Assessment" page
2. Enter borrower information in the form fields
3. Click "Assess Credit Risk"
4. View the risk score, grade, and recommendation

### Batch Processing
1. Navigate to "Batch Processing" page
2. Download the CSV template
3. Fill in borrower data for multiple records
4. Upload your CSV file
5. Click "Process Assessments"
6. Download the results

### Chat Assistant
1. Navigate to "Chat Assistant" page
2. Ask questions about credit policies
3. Use quick action buttons for common queries

## Risk Scoring Algorithm

The system evaluates risk based on:
- Annual income level
- Debt-to-income ratio
- Employment history
- Credit history length
- Previous defaults
- Collateral value

### Grade Classification

| Grade | Score Range | Risk Level |
|-------|-------------|------------|
| A | 80-100 | Excellent |
| B | 65-79 | Good |
| C | 50-64 | Fair |
| D | 35-49 | Poor |
| E | 0-34 | Very Poor |

## License

MIT License
