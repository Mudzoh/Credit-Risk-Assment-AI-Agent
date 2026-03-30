# Credit Risk Assessment AI Agent - Specification

## 1. Project Overview

**Project Name:** CreditRisk AI Agent  
**Project Type:** Web Application (Streamlit)  
**Core Functionality:** An AI-powered credit risk assessment tool that evaluates borrower creditworthiness, predicts default probability, and streamlines loan approval decisions through an interactive chatbot interface.  
**Target Users:** Loan officers, credit analysts, financial institutions, and risk management teams.

---

## 2. UI/UX Specification

### Layout Structure

**Multi-page Application:**
1. **Home/Dashboard** - Overview and quick assessment
2. **Credit Assessment** - Manual data input for individual assessment
3. **Batch Processing** - Upload CSV for bulk analysis
4. **Chatbot Assistant** - Interactive AI chatbot for credit queries
5. **Analytics** - Visual reports and risk distribution charts

**Navigation:** Sidebar with page icons and labels

### Visual Design

**Color Palette:**
- Primary: `#1E3A5F` (Deep Navy Blue)
- Secondary: `#2E7D32` (Forest Green - for positive indicators)
- Accent: `#D32F2F` (Crimson Red - for risk indicators)
- Warning: `#F57C00` (Orange)
- Background: `#F5F7FA` (Light Gray)
- Card Background: `#FFFFFF` (White)
- Text Primary: `#212121`
- Text Secondary: `#757575`

**Typography:**
- Headings: Inter Bold, sizes 24px/20px/16px
- Body: Inter Regular, 14px
- Code/Data: JetBrains Mono, 13px

**Spacing System:**
- Container padding: 24px
- Card padding: 20px
- Element gap: 16px
- Border radius: 12px

**Visual Effects:**
- Cards: `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`
- Buttons: Subtle hover elevation
- Risk meters: Animated gradient fills

### Components

**1. Risk Score Card**
- Circular gauge display (0-100)
- Color-coded: Green (Low), Orange (Medium), Red (High)
- Animated fill on score change

**2. Input Form Fields**
- Text inputs with floating labels
- Number inputs with validation
- Dropdown selects for categorical data
- Date pickers for temporal data

**3. Chat Interface**
- Chat bubble layout (user right, bot left)
- Typing indicator animation
- Quick action buttons
- Message timestamps

**4. Data Tables**
- Sortable columns
- Risk color highlighting
- Pagination for large datasets

**5. Charts**
- Pie chart for risk distribution
- Bar chart for factor analysis
- Line chart for trend analysis

---

## 3. Functionality Specification

### Core Features

**A. Credit Assessment Engine**
- Input borrower data (income, employment, debt-to-income ratio, credit history, collateral)
- Calculate credit score based on weighted factors
- Generate risk rating (A/B/C/D/E classification)
- Provide approval/rejection recommendation with reasoning

**B. Default Probability Prediction**
- Logistic regression model for probability estimation
- Percentage-based output (0-100%)
- Confidence interval display
- Key risk factors identification

**C. Chatbot Assistant**
- Natural language queries about credit policies
- Explain risk assessments in plain language
- Recommend next steps for applicants
- Answer FAQs about loan criteria
- Powered by rule-based + keyword matching (simulated AI)

**D. Batch Processing**
- CSV upload with template download
- Bulk risk assessment
- Export results to CSV/Excel
- Summary statistics

**E. Analytics Dashboard**
- Risk distribution pie chart
- Approval rate metrics
- Average risk scores by category
- Historical trend analysis

### Data Model

**Borrower Information:**
- `age` - Integer (18-100)
- `annual_income` - Float
- `employment_status` - Enum (employed/self-employed/unemployed/retired)
- `employment_years` - Integer
- `debt_amount` - Float
- `monthly_expenses` - Float
- `credit_history_length` - Integer (years)
- `previous_defaults` - Integer
- `loan_amount` - Float
- `loan_term` - Integer (months)
- `interest_rate` - Float
- `collateral_value` - Float
- `collateral_type` - Enum (none/real_estate/vehicle/other)

### Scoring Algorithm

**Risk Score Formula:**
```
Base Score = 100
Adjustments:
- Income < 30k: -15
- Debt-to-Income > 40%: -20
- Employment < 1 year: -10
- Previous defaults: -25 each
- Credit history < 2 years: -10
- No collateral: -15
- Age < 25: -5
```

**Risk Classification:**
- Score 80-100: Grade A (Excellent, Auto-Approve)
- Score 65-79: Grade B (Good, Approve with conditions)
- Score 50-64: Grade C (Fair, Manual review)
- Score 35-49: Grade D (Poor, High scrutiny)
- Score 0-34: Grade E (Very Poor, Decline)

### Edge Cases

- Missing data fields: Use median/mode imputation with warning
- Extreme outliers: Cap at reasonable limits
- Zero income: Flag as high risk
- Negative values: Validation error

---

## 4. Technical Specification

**Framework:** Streamlit (Python)

**Required Libraries:**
- `streamlit` - Web UI
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `plotly` - Interactive charts
- `scikit-learn` - ML model (logistic regression)
- `joblib` - Model persistence
- `requests` - API calls (if needed)

**Project Structure:**
```
credit-risk-agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies
├── SPEC.md               # This specification
├── README.md             # Deployment guide
├── models/
│   └── risk_model.pkl    # Trained model
├── data/
│   └── sample_data.csv   # Sample dataset
├── utils/
│   ├── scoring.py        # Risk scoring logic
│   ├── chatbot.py        # Chatbot engine
│   └── model_trainer.py  # ML model training
└── .streamlit/
    └── config.toml       # Streamlit config
```

---

## 5. Acceptance Criteria

1. ✅ User can input individual borrower data via form
2. ✅ System displays risk score with visual gauge
3. ✅ Default probability percentage is shown
4. ✅ Loan approval recommendation is provided
5. ✅ Chatbot responds to credit-related queries
6. ✅ User can upload CSV for batch processing
7. ✅ Analytics charts display risk distribution
8. ✅ Application is deployable to Streamlit Cloud via GitHub
9. ✅ All interactive elements are functional
10. ✅ Responsive design works on desktop/tablet
