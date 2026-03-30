import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple

st.set_page_config(
    page_title="CreditRisk AI Agent",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .stApp { background-color: #F5F7FA; }
    .main-header { color: #1E3A5F; font-weight: 700; }
    .metric-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .stButton > button { background-color: #1E3A5F; color: white; border: none; border-radius: 8px; padding: 10px 24px; }
</style>
""",
    unsafe_allow_html=True,
)


class CreditRiskScorer:
    def __init__(self):
        self.weights = {
            "income": 0.20,
            "debt_to_income": 0.25,
            "employment": 0.15,
            "credit_history": 0.15,
            "defaults": 0.15,
            "collateral": 0.10,
        }

    def calculate_debt_to_income(
        self, annual_income: float, debt_amount: float
    ) -> float:
        if annual_income <= 0:
            return 100.0
        monthly_income = annual_income / 12
        monthly_debt = debt_amount / 12
        return (monthly_debt / monthly_income) * 100 if monthly_income > 0 else 100.0

    def calculate_risk_score(self, data: Dict) -> Tuple[int, str, List[str]]:
        score = 100
        risk_factors = []

        annual_income = data.get("annual_income", 0)
        if annual_income < 30000:
            score -= 15
            risk_factors.append(f"Low annual income (${annual_income:,.0f})")
        elif annual_income < 50000:
            score -= 8
            risk_factors.append("Below average income")

        debt_amount = data.get("debt_amount", 0)
        dti = self.calculate_debt_to_income(annual_income, debt_amount)
        if dti > 40:
            score -= 20
            risk_factors.append(f"High debt-to-income ratio ({dti:.1f}%)")
        elif dti > 30:
            score -= 10
            risk_factors.append(f"Moderate debt-to-income ratio ({dti:.1f}%)")

        employment_years = data.get("employment_years", 0)
        if employment_years < 1:
            score -= 10
            risk_factors.append("Employment less than 1 year")
        elif employment_years < 2:
            score -= 5
            risk_factors.append("Limited employment history")

        credit_history = data.get("credit_history_length", 0)
        if credit_history < 2:
            score -= 10
            risk_factors.append(f"Short credit history ({credit_history} years)")

        previous_defaults = data.get("previous_defaults", 0)
        if previous_defaults > 0:
            score -= 25 * previous_defaults
            risk_factors.append(f"Previous defaults: {previous_defaults}")

        collateral_value = data.get("collateral_value", 0)
        collateral_type = data.get("collateral_type", "none")
        loan_amount = data.get("loan_amount", 0)

        if collateral_type == "none" or collateral_value == 0:
            score -= 15
            risk_factors.append("No collateral provided")
        elif collateral_value < loan_amount * 0.5:
            score -= 8
            risk_factors.append("Insufficient collateral coverage")
        elif collateral_value >= loan_amount:
            score += 5
            risk_factors.append("Strong collateral coverage")

        age = data.get("age", 30)
        if age < 25:
            score -= 5
            risk_factors.append("Young borrower (under 25)")
        elif age > 70:
            score -= 3
            risk_factors.append("Senior borrower (over 70)")

        score = max(0, min(100, score))
        grade = self.get_grade(score)

        return score, grade, risk_factors

    def get_grade(self, score: int) -> str:
        if score >= 80:
            return "A"
        elif score >= 65:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 35:
            return "D"
        else:
            return "E"

    def get_recommendation(self, grade: str, score: int) -> Tuple[str, str]:
        recommendations = {
            "A": (
                "APPROVE",
                "Excellent credit profile. Auto-approve with standard terms.",
            ),
            "B": ("APPROVE", "Good credit profile. Approve with standard terms."),
            "C": (
                "CONDITIONAL APPROVAL",
                "Fair credit profile. Approve with higher interest rate or additional conditions.",
            ),
            "D": (
                "REVIEW REQUIRED",
                "Poor credit profile. Manual review by senior officer required.",
            ),
            "E": (
                "DECLINE",
                "Very poor credit profile. Recommend decline or significant restructuring required.",
            ),
        }
        return recommendations.get(grade, ("REVIEW", "Manual review required"))

    def predict_default_probability(self, data: Dict) -> Tuple[float, float]:
        score, grade, _ = self.calculate_risk_score(data)

        base_probability = {"A": 0.03, "B": 0.08, "C": 0.18, "D": 0.35, "E": 0.55}

        prob = base_probability.get(grade, 0.25)

        loan_amount = data.get("loan_amount", 0)
        annual_income = data.get("annual_income", 1)
        if annual_income > 0:
            loan_to_income = loan_amount / annual_income
            if loan_to_income > 3:
                prob += 0.10
            elif loan_to_income > 5:
                prob += 0.15

        prob = max(0.01, min(0.99, prob))
        confidence = 0.85 if grade in ["A", "E"] else 0.75

        return round(prob * 100, 1), confidence

    def assess_credit(self, borrower_data: Dict) -> Dict:
        score, grade, risk_factors = self.calculate_risk_score(borrower_data)
        recommendation, reason = self.get_recommendation(grade, score)
        probability, confidence = self.predict_default_probability(borrower_data)

        return {
            "risk_score": score,
            "risk_grade": grade,
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "reason": reason,
            "default_probability": probability,
            "confidence": confidence,
        }


class CreditChatbot:
    def __init__(self):
        self.conversation_history = []
        self.responses = {
            "greeting": [
                "Hello! I'm your Credit Risk Assessment Assistant. How can I help you today?",
                "Hi there! Ready to assist with credit risk evaluations.",
            ],
            "risk_assessment": [
                "I evaluate credit risk based on: Annual income, Debt-to-income ratio, Employment history, Credit history length, Previous defaults, and Collateral value."
            ],
            "approval_criteria": [
                "Loan approval depends on: Risk Score >= 65 for standard approval, Score 50-64: Conditional approval, Score < 50: Manual review required."
            ],
            "default_probability": [
                "Default probability by grade: A: ~3%, B: ~8%, C: ~18%, D: ~35%, E: ~55%"
            ],
            "grade_meaning": [
                "Grade A (80-100): Excellent - Auto-approve | B (65-79): Good - Approve | C (50-64): Fair - Higher rate | D (35-49): Poor - Review | E (0-34): Very Poor - Decline"
            ],
            "help": [
                "I can help with: Credit Assessment, Default Prediction, Approval Guidance, Factor Analysis, and General Inquiries."
            ],
            "collateral": [
                "Collateral improves risk score: Real estate +15pts, Vehicle +10pts, Other +5-10pts, None -15pts. Ideal coverage is 100%+ of loan."
            ],
            "debt_ratio": [
                "Debt-to-Income (DTI) = Monthly Debt / Monthly Income x 100. Below 36%: Excellent, 36-43%: Acceptable, Above 43%: Risky."
            ],
            "unclear": [
                "I'm not quite sure I understood. Try asking about: risk assessment, approval criteria, default probability, or risk grades."
            ],
        }

    def process_message(self, message: str) -> str:
        message_lower = message.lower().strip()

        if any(
            word in message_lower for word in ["hello", "hi", "hey", "good morning"]
        ):
            return self._get_random("greeting")
        elif any(
            phrase in message_lower
            for phrase in [
                "how you assess",
                "credit score",
                "risk factor",
                "what factor",
            ]
        ):
            return self._get_random("risk_assessment")
        elif any(
            word in message_lower
            for word in ["approval", "qualify", "eligible", "criteria", "requirement"]
        ):
            return self._get_random("approval_criteria")
        elif any(
            word in message_lower
            for word in ["default", "probability", "chance", "fail"]
        ):
            return self._get_random("default_probability")
        elif any(
            word in message_lower
            for word in ["grade", "tier", "classification", "mean"]
        ):
            return self._get_random("grade_meaning")
        elif any(
            word in message_lower for word in ["collateral", "security", "guarantee"]
        ):
            return self._get_random("collateral")
        elif any(
            phrase in message_lower for phrase in ["debt ratio", "dti", "income ratio"]
        ):
            return self._get_random("debt_ratio")
        elif any(
            word in message_lower
            for word in ["help", "what can", "feature", "capability"]
        ):
            return self._get_random("help")
        else:
            return self._get_random("unclear")

    def _get_random(self, key: str) -> str:
        import random

        return random.choice(self.responses.get(key, self.responses["unclear"]))

    def clear_history(self):
        self.conversation_history = []


def create_risk_gauge(score: int):
    if score >= 80:
        color = "#2E7D32"
        label = "LOW RISK"
    elif score >= 50:
        color = "#F57C00"
        label = "MEDIUM RISK"
    else:
        color = "#D32F2F"
        label = "HIGH RISK"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#757575"},
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "rgba(245, 247, 250, 0.9)",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0",
                "steps": [
                    {"range": [0, 35], "color": "rgba(211, 47, 47, 0.2)"},
                    {"range": [35, 50], "color": "rgba(245, 124, 0, 0.2)"},
                    {"range": [50, 65], "color": "rgba(245, 124, 0, 0.2)"},
                    {"range": [65, 80], "color": "rgba(46, 125, 50, 0.2)"},
                    {"range": [80, 100], "color": "rgba(46, 125, 50, 0.3)"},
                ],
                "threshold": {"line": {"color": color, "width": 4}, "value": score},
            },
            title={"text": label, "font": {"size": 16, "color": color}},
            number={"font": {"size": 48, "color": color}},
        )
    )
    fig.update_layout(
        height=250, margin=dict(l=20, r=20, t=60, b=20), paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def process_batch_assessment(df: pd.DataFrame) -> pd.DataFrame:
    scorer = CreditRiskScorer()
    results = []
    for _, row in df.iterrows():
        data = row.to_dict()
        result = scorer.assess_credit(data)
        results.append(
            {
                "risk_score": result["risk_score"],
                "risk_grade": result["risk_grade"],
                "default_probability": result["default_probability"],
                "recommendation": result["recommendation"],
                "risk_factors": ", ".join(result["risk_factors"]),
            }
        )
    return pd.DataFrame(results)


def init_session_state():
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = CreditChatbot()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "assessment_results" not in st.session_state:
        st.session_state.assessment_results = []
    if "uploaded_df" not in st.session_state:
        st.session_state.uploaded_df = None


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🏦 CreditRisk AI")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "📊 Credit Assessment",
                "📁 Batch Processing",
                "💬 Chat Assistant",
                "📈 Analytics",
            ],
            index=0,
        )
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.metric("Total Assessed", len(st.session_state.assessment_results))
        if st.session_state.assessment_results:
            approved = sum(
                1
                for r in st.session_state.assessment_results
                if "APPROVE" in r.get("recommendation", "")
            )
            st.metric(
                "Approval Rate",
                f"{(approved / len(st.session_state.assessment_results)) * 100:.1f}%",
            )
        return page


def dashboard_page():
    st.markdown(
        '<h1 class="main-header">🏠 Credit Risk Assessment Dashboard</h1>',
        unsafe_allow_html=True,
    )
    st.markdown("Welcome to the AI-powered credit risk assessment system.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Quick Assessment")
        st.markdown("Evaluate individual borrower creditworthiness")
        if st.button("Start Assessment", key="dash_assess"):
            st.session_state["page"] = "📊 Credit Assessment"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Assistant")
        st.markdown("Chat about credit policies and criteria")
        if st.button("Chat Now", key="dash_chat"):
            st.session_state["page"] = "💬 Chat Assistant"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Batch Process")
        st.markdown("Upload CSV files for bulk analysis")
        if st.button("Upload CSV", key="dash_batch"):
            st.session_state["page"] = "📁 Batch Processing"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def credit_assessment_page():
    st.markdown(
        '<h1 class="main-header">📊 Credit Assessment</h1>', unsafe_allow_html=True
    )
    st.markdown(
        "Enter borrower information to generate a comprehensive credit risk assessment."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.expander("👤 Personal Information", expanded=True):
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
            employment_status = st.selectbox(
                "Employment Status",
                ["employed", "self-employed", "unemployed", "retired"],
            )
            employment_years = st.number_input(
                "Years at Current Job", min_value=0, max_value=50, value=3
            )

        with st.expander("💰 Financial Information", expanded=True):
            annual_income = st.number_input(
                "Annual Income ($)", min_value=0, value=75000, step=1000
            )
            debt_amount = st.number_input(
                "Total Existing Debt ($)", min_value=0, value=15000, step=1000
            )
            monthly_expenses = st.number_input(
                "Monthly Expenses ($)", min_value=0, value=3000, step=100
            )

        with st.expander("📋 Credit History", expanded=True):
            credit_history_length = st.number_input(
                "Credit History (Years)", min_value=0, max_value=50, value=8
            )
            previous_defaults = st.number_input(
                "Previous Defaults", min_value=0, max_value=20, value=0
            )

    with col2:
        with st.expander("🏦 Loan Details", expanded=True):
            loan_amount = st.number_input(
                "Requested Loan Amount ($)", min_value=1000, value=50000, step=1000
            )
            loan_term = st.selectbox("Loan Term", [12, 24, 36, 48, 60, 72, 84])
            interest_rate = st.number_input(
                "Interest Rate (%)", min_value=0.0, max_value=30.0, value=7.5, step=0.1
            )

        with st.expander("🏠 Collateral", expanded=True):
            collateral_type = st.selectbox(
                "Collateral Type", ["none", "real_estate", "vehicle", "other"]
            )
            collateral_value = st.number_input(
                "Collateral Value ($)", min_value=0, value=0, step=1000
            )

    if st.button("🔍 Assess Credit Risk", use_container_width=True, type="primary"):
        borrower_data = {
            "age": age,
            "employment_status": employment_status,
            "employment_years": employment_years,
            "annual_income": annual_income,
            "debt_amount": debt_amount,
            "monthly_expenses": monthly_expenses,
            "credit_history_length": credit_history_length,
            "previous_defaults": previous_defaults,
            "loan_amount": loan_amount,
            "loan_term": loan_term,
            "interest_rate": interest_rate,
            "collateral_type": collateral_type,
            "collateral_value": collateral_value,
        }

        scorer = CreditRiskScorer()
        result = scorer.assess_credit(borrower_data)
        st.session_state.assessment_results.append(result)

        st.markdown("---")
        st.markdown("### Assessment Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            fig = create_risk_gauge(result["risk_score"])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            grade_colors = {
                "A": "#2E7D32",
                "B": "#1976D2",
                "C": "#F57C00",
                "D": "#E64A19",
                "E": "#D32F2F",
            }
            st.markdown(
                f"<div style='text-align: center; padding: 30px;'><div style='font-size: 18px; color: #757575;'>Risk Grade</div><div style='font-size: 72px; font-weight: bold; color: {grade_colors.get(result['risk_grade'], '#757575')}'>{result['risk_grade']}</div><div style='font-size: 14px; color: #757575;'>Score: {result['risk_score']}/100</div></div>",
                unsafe_allow_html=True,
            )

        with col3:
            prob = result["default_probability"]
            prob_color = (
                "#2E7D32" if prob < 15 else ("#F57C00" if prob < 35 else "#D32F2F")
            )
            st.markdown(
                f"<div style='text-align: center; padding: 30px;'><div style='font-size: 18px; color: #757575;'>Default Probability</div><div style='font-size: 48px; font-weight: bold; color: {prob_color};'>{prob}%</div><div style='font-size: 14px; color: #757575;'>Confidence: {result['confidence'] * 100:.0f}%</div></div>",
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns(2)
        with col1:
            rec = result["recommendation"]
            rec_color = (
                "#2E7D32"
                if "APPROVE" in rec and "CONDITIONAL" not in rec
                else ("#F57C00" if "CONDITIONAL" in rec else "#D32F2F")
            )
            st.markdown(
                f"<div class='metric-card'><h4 style='color: #757575;'>Recommendation</h4><div style='font-size: 28px; font-weight: bold; color: {rec_color};'>{rec}</div><p style='color: #757575;'>{result['reason']}</p></div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Risk Factors Identified")
            if result["risk_factors"]:
                for factor in result["risk_factors"]:
                    st.markdown(f"- {factor}")
            else:
                st.markdown("✓ No significant risk factors")
            st.markdown("</div>", unsafe_allow_html=True)


def batch_processing_page():
    st.markdown(
        '<h1 class="main-header">📁 Batch Processing</h1>', unsafe_allow_html=True
    )
    st.markdown("Upload a CSV file to process multiple credit assessments at once.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 📥 Upload CSV")
        uploaded_file = st.file_uploader(
            "Choose a CSV file", type="csv", key="csv_uploader"
        )
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.uploaded_df = df
                st.markdown(f"**File:** {uploaded_file.name}")
                st.markdown(f"**Records:** {len(df)}")
                st.dataframe(df.head(), use_container_width=True)
            except Exception as e:
                st.error(f"Error reading file: {e}")

    with col2:
        st.markdown("#### 📋 Required CSV Columns")
        cols = [
            "age",
            "annual_income",
            "debt_amount",
            "monthly_expenses",
            "employment_years",
            "credit_history_length",
            "previous_defaults",
            "loan_amount",
            "loan_term",
            "collateral_value",
            "collateral_type",
        ]
        for col in cols:
            st.markdown(f"- `{col}`")
        if st.button("📥 Download Template"):
            template_df = pd.DataFrame(columns=cols)
            template_df = template_df._append(
                {
                    "age": 35,
                    "annual_income": 75000,
                    "debt_amount": 15000,
                    "monthly_expenses": 3000,
                    "employment_years": 3,
                    "credit_history_length": 8,
                    "previous_defaults": 0,
                    "loan_amount": 50000,
                    "loan_term": 60,
                    "collateral_value": 25000,
                    "collateral_type": "vehicle",
                },
                ignore_index=True,
            )
            csv = template_df.to_csv(index=False)
            st.download_button(
                label="Download CSV Template",
                data=csv,
                file_name="credit_template.csv",
                mime="text/csv",
            )

    if st.session_state.uploaded_df is not None and st.button(
        "🚀 Process Assessments", type="primary"
    ):
        with st.spinner("Processing..."):
            try:
                df = st.session_state.uploaded_df
                if df.empty or df.shape[1] == 0:
                    st.error(
                        "The uploaded CSV file appears to be empty or invalid. Please check the file format."
                    )
                else:
                    results_df = process_batch_assessment(df)
                    st.session_state.assessment_results.extend(
                        results_df.to_dict("records")
                    )

                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Processed", len(results_df))
                    with col2:
                        approved = len(
                            results_df[
                                results_df["recommendation"].str.contains(
                                    "APPROVE", na=False
                                )
                            ]
                        )
                        st.metric("Approved", approved)
                    with col3:
                        declined = len(
                            results_df[results_df["recommendation"] == "DECLINE"]
                        )
                        st.metric("Declined", declined)
                    with col4:
                        avg_score = results_df["risk_score"].mean()
                        st.metric("Avg Risk Score", f"{avg_score:.1f}")

                    st.dataframe(results_df, use_container_width=True)
                    csv_result = results_df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results",
                        csv_result,
                        file_name="results.csv",
                        mime="text/csv",
                    )
            except Exception as e:
                st.error(f"Error processing: {e}")


def chat_assistant_page():
    st.markdown(
        '<h1 class="main-header">💬 Chat Assistant</h1>', unsafe_allow_html=True
    )
    st.markdown(
        "Ask questions about credit risk assessment, or use quick actions below."
    )

    col1, col2, col3, col4 = st.columns(4)
    quick_questions = [
        ("Assess risk?", "How do you assess risk?"),
        ("Approval criteria?", "What are approval criteria?"),
        ("Default prob?", "What is default probability?"),
        ("Grade meaning?", "What do grades mean?"),
    ]

    for i, (label, question) in enumerate(quick_questions):
        col = [col1, col2, col3, col4][i]
        if col.button(label, key=f"quick_{i}"):
            response = st.session_state.chatbot.process_message(question)
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.chat_history.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()

    st.markdown("---")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your question..."):
        response = st.session_state.chatbot.process_message(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    if st.button("🗑️ Clear"):
        st.session_state.chat_history = []
        st.rerun()
        st.rerun()


def analytics_page():
    st.markdown(
        '<h1 class="main-header">📈 Analytics Dashboard</h1>', unsafe_allow_html=True
    )

    if not st.session_state.assessment_results:
        st.info(
            "No assessment data available. Run some credit assessments to see analytics."
        )
        return

    results_df = pd.DataFrame(st.session_state.assessment_results)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Assessments", len(results_df))
    with col2:
        avg_score = results_df["risk_score"].mean() if "risk_score" in results_df else 0
        st.metric("Average Risk Score", f"{avg_score:.1f}")
    with col3:
        avg_default = (
            results_df["default_probability"].mean()
            if "default_probability" in results_df
            else 0
        )
        st.metric("Avg Default Probability", f"{avg_default:.1f}%")
    with col4:
        approved = (
            len(
                results_df[
                    results_df.get("recommendation", "").str.contains(
                        "APPROVE", na=False
                    )
                ]
            )
            if "recommendation" in results_df
            else 0
        )
        rate = (approved / len(results_df) * 100) if len(results_df) > 0 else 0
        st.metric("Approval Rate", f"{rate:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Risk Grade Distribution")
        if "risk_grade" in results_df:
            grade_counts = results_df["risk_grade"].value_counts().sort_index()
            fig_pie = px.pie(
                values=grade_counts.values,
                names=grade_counts.index,
                color=grade_counts.index,
                color_discrete_map={
                    "A": "#2E7D32",
                    "B": "#1976D2",
                    "C": "#F57C00",
                    "D": "#E64A19",
                    "E": "#D32F2F",
                },
            )
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.markdown("#### Recommendation Distribution")
        if "recommendation" in results_df:
            rec_counts = results_df["recommendation"].value_counts()
            fig_bar = px.bar(
                x=rec_counts.index,
                y=rec_counts.values,
                color=rec_counts.index,
                color_discrete_sequence=["#2E7D32", "#F57C00", "#D32F2F", "#1976D2"],
            )
            fig_bar.update_layout(
                height=350, showlegend=False, xaxis_title="", yaxis_title="Count"
            )
            st.plotly_chart(fig_bar, use_container_width=True)


def main():
    init_session_state()
    page = render_sidebar()

    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "📊 Credit Assessment":
        credit_assessment_page()
    elif page == "📁 Batch Processing":
        batch_processing_page()
    elif page == "💬 Chat Assistant":
        chat_assistant_page()
    elif page == "📈 Analytics":
        analytics_page()


if __name__ == "__main__":
    main()
