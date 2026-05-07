# 💜 PhonePe Pulse — Transaction Insights

> An end-to-end Data Analytics and Machine Learning solution built on PhonePe's publicly available Pulse dataset.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://phonepeproject-3yvrqc92bkcjfqrkrlqe5f.streamlit.app/)

---

## 🔗 Quick Links

| Resource | Link |
|---|---|
| 🚀 Live Dashboard | https://phonepeproject-3yvrqc92bkcjfqrkrlqe5f.streamlit.app |
| 📊 EDA Notebook | [Phonepe_EDA.ipynb](./Phonepe_EDA.ipynb) |
| 🤖 ML Notebook | [Phonepe_ML.ipynb](./Phonepe_ML.ipynb) |
| 🗄️ Data Source | [PhonePe Pulse GitHub](https://github.com/PhonePe/pulse) |

---

## 📌 Project Overview

PhonePe is one of India's leading digital payment platforms built on the Unified Payments Interface (UPI) framework. This project analyzes over **1,16,203 records** covering transactions, user engagement, and insurance data from **2018 to 2024** across **36 Indian states and union territories**.

The project covers the complete data science lifecycle:

- ✅ Data Extraction from raw JSON files
- ✅ MySQL Database Design and ETL Pipeline
- ✅ SQL Business Case Analysis
- ✅ Exploratory Data Analysis (EDA) with 15 charts
- ✅ Machine Learning Regression Models
- ✅ Interactive Streamlit Dashboard deployed publicly

---

## 🏗️ System Architecture

```
PhonePe Pulse GitHub (JSON Files)
        ↓
data_loader.py (Python ETL Script)
        ↓
MySQL Database (9 Tables | 1,16,203 rows)
        ↓
Google Colab (EDA + ML Analysis)
        ↓
GitHub CSVs (Data for Dashboard)
        ↓
Streamlit App → Streamlit Cloud (Public URL)
```

---

## 🗄️ Database Structure

| Table | Domain | Type | Rows |
|---|---|---|---|
| aggregated_transaction | Transactions | State-level | 5,034 |
| aggregated_user | Users | State-level | 6,732 |
| aggregated_insurance | Insurance | State-level | 682 |
| map_transaction | Transactions | District-level | 20,604 |
| map_user | Users | District-level | 20,608 |
| map_insurance | Insurance | District-level | 13,876 |
| top_transaction | Transactions | Top Performers | 18,295 |
| top_user | Users | Top Performers | 18,296 |
| top_insurance | Insurance | Top Performers | 12,276 |
| **TOTAL** | | | **1,16,203** |

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming | Python 3.10 |
| Database | MySQL 8.0 |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn |
| Dashboard | Streamlit |
| Deployment | Streamlit Cloud |
| Version Control | Git & GitHub |
| Notebook | Google Colab |

---

## 📁 Repository Structure

```
phonepe_project/
│
├── data_loader.py               # ETL script to load JSON into MySQL
├── business_cases.sql           # SQL queries for 5 business case studies
├── app.py                       # Streamlit dashboard application
├── requirements.txt             # Python dependencies
│
├── Phonepe_EDA.ipynb            # EDA notebook — 15 charts + hypothesis tests
├── Phonepe_ML.ipynb             # ML notebook — 3 models + evaluation
│
├── data/                        # All 9 MySQL exported CSV files
│   ├── aggregated_transaction.csv
│   ├── aggregated_user.csv
│   ├── aggregated_insurance.csv
│   ├── map_transaction.csv
│   ├── map_user.csv
│   ├── map_insurance.csv
│   ├── top_transaction.csv
│   ├── top_user.csv
│   └── top_insurance.csv
│
└── screenshots_and_results/     # SQL result screenshots and exports
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- MySQL 8.0
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/Sabitha-23/phonepe_project.git
cd phonepe_project
```

### Step 2 — Install dependencies
```bash
pip install streamlit pandas plotly mysql-connector-python
```

### Step 3 — Set up MySQL database
- Open MySQL Workbench
- Create database: `CREATE DATABASE phonepe_pulse;`
- Run the table creation SQL from `business_cases.sql`

### Step 4 — Load data into MySQL
```bash
python data_loader.py
```

### Step 5 — Run the Streamlit dashboard
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📊 Dashboard Features

The live dashboard is organized into **4 tabs** with **13 interactive charts**:

### 📊 Transactions Tab
- KPI cards — Total transactions, Amount, Avg Amount, Active States
- Transaction type distribution pie chart
- Year-wise growth line chart
- Top 10 states horizontal bar chart
- India choropleth map by transaction amount

### 👥 Users Tab
- KPI cards — Registered Users, App Opens, Engagement Ratio
- Top states by registered users
- Device brand market share pie chart
- India engagement ratio choropleth map

### 🛡️ Insurance Tab
- KPI cards — Total Policies, Total Amount
- Top states by insurance amount
- Insurance growth by year line chart

### 🏆 Top Performers Tab
- Top 10 districts by transaction amount
- Top 10 districts by registered users
- Quarter-wise transaction performance

**All charts support:** Hover tooltips · Zoom & Pan · Legend filtering · PNG download

---

## 🤖 Machine Learning

**Task:** Regression — Predict transaction amount in crores

**Features used:** year, quarter, transaction_count, avg_txn_value, state_encoded, type_encoded, year_quarter

**Models compared:**

| Model | R² Score | Performance |
|---|---|---|
| Linear Regression | ~0.75 | Baseline |
| Random Forest (Tuned) | ~0.92 | Good |
| Gradient Boosting (Tuned) | ~0.94 | **Best** ✅ |

**Best Model:** Gradient Boosting Regressor with GridSearchCV tuning

**Evaluation:** 5-fold cross-validation · R² Score · MAE · RMSE

---

## 📈 Key Insights

- 📈 PhonePe transactions grew **exponentially post-COVID-19** (2020 onwards)
- 💳 **Peer-to-peer payments** dominate at 52% of total transactions
- 🏆 **Maharashtra, Karnataka, Telangana** are top performing states consistently
- 📱 **Xiaomi and Samsung** together account for 50%+ of the user base
- 🎉 **Q4 (Oct-Dec)** consistently shows highest transactions — festive season effect proven statistically (p-value = 0.0188)
- 🌍 **South India** generates significantly higher transactions than North India (p-value = 0.0004)
- 🛡️ **Insurance adoption** surged after 2020 with massive untapped potential in UP, Bihar

---

## 🧪 Hypothesis Testing

| Hypothesis | Test | P-Value | Result |
|---|---|---|---|
| South India vs North India transactions | T-Test | 0.0004 | Reject H0 ✅ |
| Q4 vs Q1 transaction amounts | T-Test | 0.0188 | Reject H0 ✅ |
| Transaction types differ significantly | ANOVA | 0.0000 | Reject H0 ✅ |

---

## 💡 Business Recommendations

1. **Merchant Acquisition** — Launch zero-fee onboarding in Tier 2/3 cities to grow merchant payments
2. **Re-engagement Campaigns** — Target low-engagement states with regional language support and cashback offers
3. **Q4 Preparedness** — Pre-plan server scaling and festive campaigns 8 weeks before October
4. **Insurance Expansion** — Focus on UP, Bihar, West Bengal for insurance marketing
5. **Device Optimization** — Prioritize app performance for Xiaomi and Samsung devices
6. **North India Push** — Increase marketing investment in Hindi-belt states
7. **Manipur Recovery** — Investigate 60.95% decline and implement recovery strategy

---

## 👩‍💻 Author

**Sabitha J**
Domain: Data Science with Gen AI

---

## 📄 License

This project uses publicly available data from the [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse).

---

*Built with 💜 using Python, MySQL, Streamlit, and Scikit-learn*