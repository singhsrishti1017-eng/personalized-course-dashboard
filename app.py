import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="EduPro Analytics Dashboard", layout="wide")

# Title
st.title("🎓 EduPro Personalized Course Recommendation Dashboard")

st.markdown("### AI-Based Learner Analytics & Recommendation System")

# Load Data
users = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Users")
courses = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Courses")
transactions = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Transactions")

# Merge Data
df = transactions.merge(users, on="UserID")
df = df.merge(courses, on="CourseID")

# Sidebar
st.sidebar.header("Dashboard Filters")

category_filter = st.sidebar.multiselect(
    "Select Course Category",
    options=df["CourseCategory"].unique(),
    default=df["CourseCategory"].unique()
)

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["PaymentMethod"].unique(),
    default=df["PaymentMethod"].unique()
)

filtered_df = df[
    (df["CourseCategory"].isin(category_filter)) &
    (df["PaymentMethod"].isin(payment_filter))
]

# KPIs
total_revenue = filtered_df["Amount"].sum()
total_users = filtered_df["UserID"].nunique()
total_courses = filtered_df["CourseID"].nunique()
avg_rating = filtered_df["Rating"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("👨‍🎓 Total Learners", total_users)
col3.metric("📚 Total Courses", total_courses)
col4.metric("⭐ Average Rating", f"{avg_rating:.1f}")

st.markdown("---")

# Revenue by Category
st.subheader("📈 Revenue by Course Category")

rev_cat = filtered_df.groupby("CourseCategory")["Amount"].sum().reset_index()

fig1 = px.bar(
    rev_cat,
    x="CourseCategory",
    y="Amount",
    color="CourseCategory",
    title="Revenue by Category"
)

st.plotly_chart(fig1, use_container_width=True)

# Payment Method Distribution
st.subheader("💳 Payment Method Distribution")

pay = filtered_df["PaymentMethod"].value_counts().reset_index()
pay.columns = ["PaymentMethod", "Count"]

fig2 = px.pie(
    pay,
    names="PaymentMethod",
    values="Count",
    title="Payment Methods"
)

st.plotly_chart(fig2, use_container_width=True)

# Top Courses
st.subheader("🏆 Top Courses")

top_courses = (
    filtered_df.groupby("CourseName")
    .size()
    .reset_index(name="Enrollments")
    .sort_values(by="Enrollments", ascending=False)
    .head(10)
)

fig3 = px.bar(
    top_courses,
    x="CourseName",
    y="Enrollments",
    color="Enrollments",
    title="Top 10 Courses"
)

st.plotly_chart(fig3, use_container_width=True)

# Revenue Trend
st.subheader("📅 Revenue Trend")

filtered_df["TransactionDate"] = pd.to_datetime(filtered_df["TransactionDate"])

revenue_trend = (
    filtered_df.groupby("TransactionDate")["Amount"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    revenue_trend,
    x="TransactionDate",
    y="Amount",
    title="Revenue Over Time"
)

st.plotly_chart(fig4, use_container_width=True)

# Ratings Distribution
st.subheader("⭐ Course Rating Distribution")

fig5 = px.histogram(
    filtered_df,
    x="Rating",
    nbins=10,
    title="Ratings Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# Learner Age Distribution
st.subheader("👥 Learner Age Distribution")

fig6 = px.histogram(
    filtered_df,
    x="Age",
    nbins=15,
    title="Age Distribution"
)

st.plotly_chart(fig6, use_container_width=True)

# Recommendation Insights
st.subheader("🤖 Recommendation Insights")

recommended = (
    filtered_df.groupby("CourseName")["Rating"]
    .mean()
    .reset_index()
    .sort_values(by="Rating", ascending=False)
    .head(5)
)

st.table(recommended)

# Footer
st.markdown("---")
st.markdown("### ✅ Developed by Srishti Singh")
