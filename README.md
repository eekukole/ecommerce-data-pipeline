# E-Commerce Data Pipeline 🚀

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)

## 📊 Project Overview
End-to-end data engineering pipeline for e-commerce analytics, evolving from local development to cloud-native architecture.

## 🎯 Current Status: Phase 1 Complete ✅

### What's Working:
- ✅ Event generator producing realistic e-commerce data
- ✅ Python data loader (JSON → MySQL)
- ✅ Star schema data warehouse
- ✅ Business analytics queries

### Tech Stack:
- **Language:** Python 3.10+
- **Database:** MySQL 8.0
- **Libraries:** Faker, PyMySQL, python-dotenv
- **Data Model:** Star Schema (Kimball methodology)

## 📁 Project Structure
```
ecommerce-data-pipeline/
├── src/
│   ├── event_generator.py    # Generates synthetic e-commerce events
│   └── loader.py              # Loads JSON data into MySQL
├── sql/
│   ├── schema/               # Database table definitions
│   └── transformations/      # ETL transformation scripts
├── data/
│   └── events/              # Generated JSON event files
└── dags/                    # Airflow DAGs (coming soon)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MySQL 8.0
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your MySQL credentials

# Generate sample data
python src/event_generator.py

# Load into MySQL
python src/loader.py
```

## 📈 Data Warehouse Schema

**Dimensions:**
- `dim_customers` - Customer profiles and segmentation
- `dim_products` - Product catalog
- `dim_date` - Time dimension
- `dim_devices` - Device and browser information

**Facts:**
- `fact_orders` - Purchase transactions
- `fact_page_views` - User browsing behavior

## 📊 Sample Analytics
```sql
-- Customer Segmentation
SELECT 
    customer_segment,
    COUNT(*) AS customers,
    AVG(total_spent) AS avg_ltv
FROM dim_customers
GROUP BY customer_segment;

-- Daily Revenue Trend
SELECT 
    d.full_date,
    SUM(f.total_amount) AS revenue
FROM fact_orders f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.full_date;
```

## 🎯 Roadmap

- [x] Phase 1: Local pipeline fundamentals
- [ ] Phase 2: Cloud migration (AWS)
- [ ] Phase 3: Airflow orchestration
- [ ] Phase 4: Real-time streaming (Kafka)

## 📚 What I Learned
- Data modeling with star schema design
- ETL pipeline development
- Python-MySQL integration
- Dimensional modeling best practices

## 🤝 Connect
Building in public! Follow my data engineering journey.

---

**Status:** 🚧 Active Development | **Next:** Docker + Airflow Setup