# E-Commerce Data Pipeline 🚀

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-brightgreen.svg)

## 📊 Project Overview

End-to-end data engineering pipeline for e-commerce analytics, demonstrating the full lifecycle from raw event generation to analytics-ready data warehouse. This project showcases dimensional modeling, ETL development, and business intelligence capabilities.

---

## 🎯 Current Status: Phase 1 Complete ✅

### What's Working:
- ✅ Event generator producing realistic e-commerce data
- ✅ Python ETL pipeline (JSON → MySQL)
- ✅ Star schema data warehouse (Kimball methodology)
- ✅ Business analytics queries delivering insights
- ✅ 165 events processed through complete pipeline

---

## 🏗️ Architecture
```
Event Generator → JSON Files → Python Loader → Staging DB → Transformations → Data Warehouse → Analytics
     (Faker)      (165 events)   (PyMySQL)    (Raw data)   (SQL ETL)      (Star Schema)    (Insights)
```

---

## 📁 Project Structure
```
ecommerce-data-pipeline/
├── src/
│   ├── event_generator.py       # Generates synthetic e-commerce events
│   ├── loader.py                 # Loads JSON data into MySQL staging
│   └── utils/
│       └── db_connector.py       # Database connection utilities
├── sql/
│   ├── schema/
│   │   ├── create_staging.sql    # Staging table schemas
│   │   └── create_warehouse.sql  # Data warehouse schemas
│   └── transformations/
│       ├── 01_populate_dim_date.sql
│       ├── 02_populate_dim_customers.sql
│       ├── 03_populate_dim_products.sql
│       ├── 04_populate_dim_devices.sql
│       ├── 05_populate_fact_orders.sql
│       └── 06_populate_fact_page_views.sql
├── data/
│   └── events/                   # Generated JSON event files (gitignored)
├── dags/                         # Airflow DAGs (Phase 2)
├── tests/                        # Data quality tests
├── docs/                         # Documentation
├── .env.example                  # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

**Languages & Core:**
- Python 3.10+
- SQL (MySQL 8.0)

**Libraries:**
- `faker` - Realistic test data generation
- `pymysql` - MySQL database connector
- `python-dotenv` - Environment variable management
- `sqlalchemy` - Database ORM (optional)

**Database:**
- MySQL 8.0 - Staging and warehouse databases

**Data Modeling:**
- Star Schema (Kimball methodology)
- Dimensional modeling best practices

**Version Control:**
- Git & GitHub

---

## 📊 Data Warehouse Schema

### Star Schema Design

**Dimension Tables:**
- **`dim_customers`** (163 rows) - Customer profiles with segmentation
  - customer_key, customer_id, first_seen_date, total_orders, total_spent, customer_segment
- **`dim_products`** (45 rows) - Product catalog with ratings
  - product_key, product_id, product_name, category, avg_rating, total_reviews
- **`dim_date`** (1 row) - Date/time dimension
  - date_key, full_date, year, quarter, month, week, day, is_weekend
- **`dim_devices`** (12 rows) - Device and browser combinations
  - device_key, device_type, browser

**Fact Tables:**
- **`fact_orders`** (20 rows) - Purchase transactions
  - order_key, order_id, customer_key, date_key, total_amount, items_count, payment_method
- **`fact_page_views`** (100 rows) - User browsing behavior
  - pageview_key, event_id, customer_key, device_key, date_key, page_url, session_id

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- MySQL 8.0
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/eekukole/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database connection**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your MySQL credentials
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME_STAGING=ecommerce_staging
# DB_NAME_WAREHOUSE=ecommerce_warehouse
```

5. **Create databases**
```sql
-- In MySQL Workbench or CLI
CREATE DATABASE ecommerce_staging;
CREATE DATABASE ecommerce_warehouse;
```

6. **Generate sample data**
```bash
python src/event_generator.py
```

7. **Load data into staging**
```bash
python src/loader.py
```

8. **Build data warehouse**
```sql
-- Run SQL scripts in order:
-- 1. sql/schema/create_warehouse.sql
-- 2. sql/transformations/*.sql (in order 01-06)
```

---

## 📈 Sample Analytics Queries

### Customer Segmentation Analysis
```sql
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_key) AS num_customers,
    COUNT(f.order_key) AS total_orders,
    COALESCE(SUM(f.total_amount), 0) AS total_revenue,
    COALESCE(AVG(f.total_amount), 0) AS avg_order_value
FROM dim_customers c
LEFT JOIN fact_orders f ON c.customer_key = f.customer_key
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;
```

### Conversion Rate Analysis
```sql
SELECT 
    COUNT(DISTINCT pv.customer_key) AS total_visitors,
    COUNT(DISTINCT o.customer_key) AS buyers,
    ROUND(COUNT(DISTINCT o.customer_key) * 100.0 / 
          COUNT(DISTINCT pv.customer_key), 2) AS conversion_rate_percent
FROM fact_page_views pv
LEFT JOIN fact_orders o ON pv.customer_key = o.customer_key;
```

### Device Usage Breakdown
```sql
SELECT 
    d.device_type,
    d.browser,
    COUNT(*) AS page_views,
    ROUND(COUNT(*) * 100.0 / 
          (SELECT COUNT(*) FROM fact_page_views), 2) AS percentage
FROM fact_page_views f
JOIN dim_devices d ON f.device_key = d.device_key
GROUP BY d.device_type, d.browser
ORDER BY page_views DESC;
```

### Revenue by Payment Method
```sql
SELECT 
    payment_method,
    COUNT(*) AS num_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM fact_orders
GROUP BY payment_method
ORDER BY total_revenue DESC;
```

---

## 💡 Key Features

### Event Generator
- Produces 4 types of realistic e-commerce events:
  - **Page Views:** User browsing behavior
  - **Add to Cart:** Product interest signals
  - **Purchases:** Complete transactions with payment info
  - **Product Reviews:** Customer feedback with ratings
- Uses Faker library for realistic fake data
- Configurable event volumes and distributions
- JSON output format for flexibility

### Data Loader
- Idempotent loading (safe to re-run)
- Error handling and logging
- Supports incremental loads
- Data validation on insert
- Connection pooling for performance

### Data Warehouse
- Star schema optimized for analytics
- Pre-aggregated customer metrics
- Slowly Changing Dimensions (SCD Type 1)
- Foreign key relationships for data integrity
- Indexed for query performance

---

## 📚 What I Learned

### Technical Skills
✅ **Dimensional Modeling** - Star schema design following Kimball methodology  
✅ **ETL Development** - Extract, Transform, Load pipeline from scratch  
✅ **Python-SQL Integration** - Database connectivity, query execution, error handling  
✅ **Data Quality** - Validation, deduplication, referential integrity  
✅ **Business Analytics** - KPI calculation, customer segmentation, conversion metrics  

### Best Practices
✅ Environment variable management for credentials  
✅ Git workflow and version control  
✅ Code documentation and README maintenance  
✅ Project structure and organization  
✅ SQL query optimization with indexes  

### Problem-Solving
✅ Debugging foreign key constraints  
✅ Handling duplicate data scenarios  
✅ Troubleshooting JOIN conditions  
✅ Data type conversions and casting  

---

## 🎯 Roadmap

### Phase 1: Fundamentals ✅ COMPLETE
- [x] Event generator
- [x] Python data loader
- [x] Star schema design
- [x] ETL transformations
- [x] Business analytics queries

### Phase 2: Orchestration (In Progress)
- [ ] Docker containerization
- [ ] Apache Airflow setup
- [ ] DAG creation for automation
- [ ] Scheduled pipeline runs
- [ ] Data quality monitoring

### Phase 3: Cloud Deployment
- [ ] AWS infrastructure setup (S3, RDS, EC2)
- [ ] Migrate pipeline to cloud
- [ ] Infrastructure as Code (Terraform)
- [ ] Cost optimization
- [ ] Cloud monitoring and alerts

### Phase 4: Advanced Features
- [ ] Real-time streaming with Kafka
- [ ] Data lakehouse architecture (Delta Lake)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Data observability tools
- [ ] API for analytics access

---

## 🧪 Testing
```bash
# Test database connection
python -c "from src.utils.db_connector import get_db_connection; get_db_connection()"

# Generate small test dataset
python src/event_generator.py --events=50

# Validate data quality
# (Data quality tests coming in Phase 2)
```

---

## 📖 Documentation

Additional documentation available in `/docs`:
- **Architecture Diagram** - Visual representation of pipeline
- **Data Dictionary** - Complete field descriptions
- **Setup Guide** - Detailed installation instructions
- **Troubleshooting** - Common issues and solutions

---

## 🤝 Contributing

This is a personal learning project, but feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📫 Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/emmanuel-ekukole88)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/eekukole)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:emmanuelekukole@gmail.com)

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **Faker** library for realistic test data generation
- **Kimball Group** for dimensional modeling methodology
- **MySQL** documentation and community
- Data engineering community for best practices and inspiration

---

## 📊 Project Stats

![GitHub last commit](https://img.shields.io/github/last-commit/eekukole/ecommerce-data-pipeline)
![GitHub repo size](https://img.shields.io/github/repo-size/eekukole/ecommerce-data-pipeline)
![Lines of code](https://img.shields.io/tokei/lines/github/eekukole/ecommerce-data-pipeline)

---

⭐ **Star this repo if you find it helpful!**

*Built with ❤️ by [Emmanuel Ekukole] | Building in public, learning every day*