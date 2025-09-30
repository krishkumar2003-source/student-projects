import os
import zipfile
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("🚀 Creating Complete Lulu Sales Dashboard Package...")
print("=" * 70)

# Create project directory
project_name = "lulu_sales_dashboard"
if not os.path.exists(project_name):
    os.makedirs(project_name)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# 1. GENERATE SYNTHETIC DATA
# ============================================================================
print("\n📊 Step 1: Generating synthetic sales data (100 rows)...")

cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Ras Al Khaimah', 'Fujairah', 'Umm Al Quwain']
nationalities = ['UAE National', 'Indian', 'Pakistani', 'Filipino', 'Egyptian', 'Jordanian', 'British', 'American']
age_groups = ['18-25', '26-35', '36-45', '46-55', '56+']
genders = ['Male', 'Female']
income_brackets = ['Low (< 5000 AED)', 'Medium (5000-15000 AED)', 'High (15000-30000 AED)', 'Very High (> 30000 AED)']
product_categories = ['Groceries', 'Electronics', 'Clothing', 'Home & Kitchen', 'Personal Care', 'Toys & Games', 'Sports', 'Books & Stationery']
loyalty_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']

data = []

for i in range(100):
    transaction_id = f'TXN{str(i+1).zfill(5)}'
    customer_id = f'CUST{str(random.randint(1, 50)).zfill(4)}'
    days_ago = random.randint(0, 180)
    transaction_date = datetime.now() - timedelta(days=days_ago)
    city = random.choice(cities)
    nationality = random.choice(nationalities)
    age_group = random.choice(age_groups)
    gender = random.choice(genders)
    income = random.choice(income_brackets)
    category = random.choice(product_categories)
    quantity = random.randint(1, 10)
    unit_price = round(random.uniform(10, 500), 2)
    total_amount = round(quantity * unit_price, 2)
    discount = round(random.uniform(0, 0.3) * total_amount, 2)
    final_amount = round(total_amount - discount, 2)
    is_loyalty_member = random.choice([True, False])
    loyalty_tier = random.choice(loyalty_tiers) if is_loyalty_member else 'None'
    loyalty_points_earned = int(final_amount * 0.1) if is_loyalty_member else 0
    loyalty_points_redeemed = random.randint(0, 100) if is_loyalty_member and random.random() > 0.7 else 0
    
    ad_budget_map = {
        'Groceries': 50000, 'Electronics': 80000, 'Clothing': 60000,
        'Home & Kitchen': 45000, 'Personal Care': 40000, 'Toys & Games': 35000,
        'Sports': 30000, 'Books & Stationery': 25000
    }
    ad_budget = ad_budget_map[category]
    store = f'Lulu {city}'
    
    data.append({
        'Transaction_ID': transaction_id, 'Customer_ID': customer_id,
        'Transaction_Date': transaction_date.strftime('%Y-%m-%d'),
        'Store_Location': store, 'City': city, 'Nationality': nationality,
        'Age_Group': age_group, 'Gender': gender, 'Income_Bracket': income,
        'Product_Category': category, 'Quantity': quantity, 'Unit_Price': unit_price,
        'Total_Amount': total_amount, 'Discount': discount, 'Final_Amount': final_amount,
        'Is_Loyalty_Member': is_loyalty_member, 'Loyalty_Tier': loyalty_tier,
        'Loyalty_Points_Earned': loyalty_points_earned,
        'Loyalty_Points_Redeemed': loyalty_points_redeemed,
        'Monthly_Ad_Budget': ad_budget
    })

df = pd.DataFrame(data)
csv_path = os.path.join(project_name, 'lulu_sales_data.csv')
df.to_csv(csv_path, index=False)
print(f"   ✅ Generated {len(df)} transactions")
print(f"   💰 Total Revenue: AED {df['Final_Amount'].sum():,.2f}")

# ============================================================================
# 2. CREATE APP.PY (MAIN DASHBOARD)
# ============================================================================
print("\n📱 Step 2: Creating Streamlit dashboard (app.py)...")

app_code = '''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Lulu Stores UAE - Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #E31837;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #FFD700 0%, #E31837 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('lulu_sales_data.csv')
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
    return df

df = load_data()

# Header
st.markdown('<h1 class="main-header">🛒 LULU HYPERMARKET UAE - SALES ANALYTICS DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown("### 📊 Regional Sales Performance & Customer Insights")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Transaction_Date'].min(), df['Transaction_Date'].max()),
    min_value=df['Transaction_Date'].min().date(),
    max_value=df['Transaction_Date'].max().date()
)

cities = st.sidebar.multiselect(
    "Select City",
    options=df['City'].unique(),
    default=df['City'].unique()
)

categories = st.sidebar.multiselect(
    "Select Product Category",
    options=df['Product_Category'].unique(),
    default=df['Product_Category'].unique()
)

loyalty = st.sidebar.multiselect(
    "Loyalty Tier",
    options=df['Loyalty_Tier'].unique(),
    default=df['Loyalty_Tier'].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Apply filters
filtered_df = df[
    (df['Transaction_Date'].dt.date >= date_range[0]) &
    (df['Transaction_Date'].dt.date <= date_range[1]) &
    (df['City'].isin(cities)) &
    (df['Product_Category'].isin(categories)) &
    (df['Loyalty_Tier'].isin(loyalty)) &
    (df['Gender'].isin(gender))
]

# KPI Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_revenue = filtered_df['Final_Amount'].sum()
    st.metric("💰 Total Revenue", f"AED {total_revenue:,.0f}")

with col2:
    total_transactions = len(filtered_df)
    st.metric("🛍️ Transactions", f"{total_transactions:,}")

with col3:
    avg_transaction = filtered_df['Final_Amount'].mean()
    st.metric("📊 Avg Transaction", f"AED {avg_transaction:,.0f}")

with col4:
    loyalty_members = filtered_df[filtered_df['Is_Loyalty_Member'] == True].shape[0]
    loyalty_pct = (loyalty_members / total_transactions * 100) if total_transactions > 0 else 0
    st.metric("⭐ Loyalty Members", f"{loyalty_pct:.1f}%")

with col5:
    total_discount = filtered_df['Discount'].sum()
    st.metric("🎁 Total Discounts", f"AED {total_discount:,.0f}")

st.markdown("---")

# Row 1: Sales by Category (Bar Chart) and City Distribution (Pie Chart)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sales by Product Category")
    category_sales = filtered_df.groupby('Product_Category')['Final_Amount'].sum().reset_index()
    category_sales = category_sales.sort_values('Final_Amount', ascending=True)
    
    fig_bar = px.bar(
        category_sales,
        x='Final_Amount',
        y='Product_Category',
        orientation='h',
        color='Final_Amount',
        color_continuous_scale='Reds',
        labels={'Final_Amount': 'Revenue (AED)', 'Product_Category': 'Category'}
    )
    fig_bar.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🌍 Sales Distribution by City")
    city_sales = filtered_df.groupby('City')['Final_Amount'].sum().reset_index()
    
    fig_pie = px.pie(
        city_sales,
        values='Final_Amount',
        names='City',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# Row 2: Customer Demographics and Loyalty Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Customer Demographics - Age Groups")
    
    fig_age = px.histogram(
        filtered_df,
        x='Age_Group',
        y='Final_Amount',
        color='Gender',
        barmode='group',
        labels={'Final_Amount': 'Revenue (AED)', 'Age_Group': 'Age Group'},
        color_discrete_map={'Male': '#1f77b4', 'Female': '#e377c2'}
    )
    fig_age.update_layout(height=400)
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.subheader("⭐ Loyalty Program Performance")
    loyalty_sales = filtered_df[filtered_df['Loyalty_Tier'] != 'None'].groupby('Loyalty_Tier')['Final_Amount'].sum().reset_index()
    
    fig_loyalty = px.pie(
        loyalty_sales,
        values='Final_Amount',
        names='Loyalty_Tier',
        color='Loyalty_Tier',
        color_discrete_map={'Bronze': '#CD7F32', 'Silver': '#C0C0C0', 'Gold': '#FFD700', 'Platinum': '#E5E4E2'}
    )
    fig_loyalty.update_traces(textposition='inside', textinfo='percent+label')
    fig_loyalty.update_layout(height=400)
    st.plotly_chart(fig_loyalty, use_container_width=True)

# Row 3: Ad Budget vs Sales and Nationality Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("💵 Advertisement Budget vs Sales")
    ad_sales = filtered_df.groupby('Product_Category').agg({
        'Final_Amount': 'sum',
        'Monthly_Ad_Budget': 'first'
    }).reset_index()
    
    fig_ad = go.Figure()
    fig_ad.add_trace(go.Bar(
        x=ad_sales['Product_Category'],
        y=ad_sales['Final_Amount'],
        name='Sales Revenue',
        marker_color='#E31837'
    ))
    fig_ad.add_trace(go.Bar(
        x=ad_sales['Product_Category'],
        y=ad_sales['Monthly_Ad_Budget'],
        name='Ad Budget',
        marker_color='#FFD700'
    ))
    fig_ad.update_layout(
        barmode='group',
        height=400,
        xaxis_title='Category',
        yaxis_title='Amount (AED)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    st.plotly_chart(fig_ad, use_container_width=True)

with col2:
    st.subheader("🌐 Customer Nationality Distribution")
    nationality_count = filtered_df['Nationality'].value_counts().reset_index()
    nationality_count.columns = ['Nationality', 'Count']
    
    fig_nat = px.bar(
        nationality_count.head(8),
        x='Count',
        y='Nationality',
        orientation='h',
        color='Count',
        color_continuous_scale='Viridis'
    )
    fig_nat.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_nat, use_container_width=True)

# Row 4: Income Distribution and Transaction Trends
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Sales by Income Bracket")
    
    fig_income = px.histogram(
        filtered_df,
        x='Income_Bracket',
        y='Final_Amount',
        color='Income_Bracket',
        labels={'Final_Amount': 'Revenue (AED)', 'Income_Bracket': 'Income Bracket'},
        color_discrete_sequence=px.colors.sequential.Greens
    )
    fig_income.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_income, use_container_width=True)

with col2:
    st.subheader("📈 Daily Transaction Trends")
    daily_sales = filtered_df.groupby('Transaction_Date')['Final_Amount'].sum().reset_index()
    
    fig_trend = px.line(
        daily_sales,
        x='Transaction_Date',
        y='Final_Amount',
        labels={'Final_Amount': 'Revenue (AED)', 'Transaction_Date': 'Date'},
        markers=True
    )
    fig_trend.update_traces(line_color='#E31837', line_width=3)
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>Lulu Hypermarket UAE - Regional Sales Dashboard</strong></p>
        <p>Data-driven insights for strategic decision making | © 2025 Lulu Group International</p>
    </div>
    """, unsafe_allow_html=True)
'''

with open(os.path.join(project_name, 'app.py'), 'w', encoding='utf-8') as f:
    f.write(app_code)
print("   ✅ Created app.py")

# ============================================================================
# 3. CREATE REQUIREMENTS.TXT
# ============================================================================
print("\n📦 Step 3: Creating requirements.txt...")

requirements_content = """streamlit==1.31.0
pandas==2.1.4
numpy==1.26.3
plotly==5.18.0"""

with open(os.path.join(project_name, 'requirements.txt'), 'w') as f:
    f.write(requirements_content)
print("   ✅ Created requirements.txt")

# ============================================================================
# 4. CREATE README.MD
# ============================================================================
print("\n📄 Step 4: Creating README.md...")

readme_content = """# 🛒 Lulu Hypermarket UAE - Sales Analytics Dashboard

A comprehensive, interactive sales dashboard for Lulu Stores in UAE, built with Streamlit.

## 📊 Dashboard Features

### Data Components
1. **Transactional Sales Data** - 100 transactions with complete details
2. **Demographic Analysis** - Customer segmentation by age, gender, nationality, income
3. **Loyalty Program Metrics** - Bronze, Silver, Gold, Platinum tier tracking
4. **Advertisement Budget Analysis** - ROI tracking for all product categories

### Visualizations
- **Bar Charts**: Sales by category, nationality distribution, ad budget comparison
- **Pie Charts**: City-wise sales, loyalty tier performance
- **Histograms**: Age groups, income brackets
- **Line Charts**: Daily transaction trends

### Interactive Filters
- Date range selection
- City filtering (Dubai, Abu Dhabi, Sharjah, etc.)
- Product categories
- Loyalty tiers
- Gender-based analysis

## 🚀 Quick Start

### Local Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

3. **Open browser**
   Navigate to http://localhost:8501

### Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

## 📦 Project Structure

```
lulu_sales_dashboard/
├── app.py                    # Main dashboard application
├── lulu_sales_data.csv      # Synthetic sales data (100 rows)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 📈 Key Performance Indicators

- **Total Revenue** in AED
- **Total Transactions**
- **Average Transaction Value**
- **Loyalty Member Percentage**
- **Total Discounts Given**

## 📊 Data Schema

- **Transaction Data**: ID, Date, Amount, Discount
- **Customer Data**: ID, Nationality, Age, Gender, Income
- **Store Data**: Location, City
- **Product Data**: Category, Quantity, Price
- **Loyalty Data**: Membership, Tier, Points
- **Marketing Data**: Monthly ad budget by category

## 🎨 Customization

Modify in `app.py`:
- Colors (Lulu brand: Red #E31837, Gold #FFD700)
- Filter options
- Chart configurations
- KPI metrics

## 🛠️ Technologies

- **Streamlit** - Dashboard framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Data generation

## 📝 Note

This dashboard uses synthetic data for demonstration. Replace with actual sales data for production use.

---

**Created for**: Lulu Stores UAE Regional Sales Team  
**Purpose**: Stakeholder presentations and data-driven decision making
"""

with open(os.path.join(project_name, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme_content)
print("   ✅ Created README.md")

# ============================================================================
# 5. CREATE .GITIGNORE
# ============================================================================
print("\n🚫 Step 5: Creating .gitignore...")

gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Streamlit
.streamlit/

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env"""

with open(os.path.join(project_name, '.gitignore'), 'w') as f:
    f.write(gitignore_content)
print("   ✅ Created .gitignore")

# ============================================================================
# 6. CREATE ZIP FILE
# ============================================================================
print("\n📦 Step 6: Creating ZIP file...")

zip_filename = f"{project_name}.zip"

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_name):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, os.path.dirname(project_name))
            zipf.write(file_path, arcname)
            print(f"   📄 Added: {arcname}")

print(f"\n   ✅ Created: {zip_filename}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("✨ PROJECT CREATION COMPLETE!")
print("=" * 70)
print(f"\n📁 Project Folder: {project_name}/")
print(f"📦 ZIP File: {zip_filename}")
print(f"\n📊 Data Summary:")
print(f"   - Total Transactions: {len(df)}")
print(f"   - Total Revenue: AED {df['Final_Amount'].sum():,.2f}")
print(f"   - Date Range: {df['Transaction_Date'].min()} to {df['Transaction_Date'].max()}")
print(f"   - Cities: {len(df['City'].unique())}")
print(f"   - Product Categories: {len(df['Product_Category'].unique())}")

print(f"\n📦 Package Contents:")
print(f"   ✅ app.py (Streamlit Dashboard)")
print(f"   ✅ lulu_sales_data.csv (100 rows)")
print(f"   ✅ requirements.txt")
print(f"   ✅ README.md")
print(f"   ✅ .gitignore")

print(f"\n🚀 Next Steps:")
print(f"   1. Extract {zip_filename}")
print(f"   2. cd {project_name}")
print(f"   3. pip install -r requirements.txt")
print(f"   4. streamlit run app.py")
print(f"\n   OR deploy to Streamlit Cloud (see README.md)")

print("\n" + "=" * 70)
print("🎉 Ready to impress your stakeholders!")
print("=" * 70)