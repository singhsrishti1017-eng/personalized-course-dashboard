Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import streamlit as st
... import pandas as pd
... import plotly.express as px
... 
... st.set_page_config(page_title="EduPro Dashboard", layout="wide")
... 
... st.title("🎓 Personalized Course Recommendation Dashboard")
... 
... # Load data
... users = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Users")
... courses = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Courses")
... transactions = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Transactions")
... 
... # Merge data
... df = transactions.merge(users, on="UserID")
... df = df.merge(courses, on="CourseID")
... 
... # KPIs
... total_revenue = df["Amount"].sum()
... total_users = df["UserID"].nunique()
... total_courses = df["CourseID"].nunique()
... 
... col1, col2, col3 = st.columns(3)
... col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
... col2.metric("Total Learners", total_users)
... col3.metric("Total Courses", total_courses)
... 
... # Revenue by Category
... st.subheader("Revenue by Category")
... rev_cat = df.groupby("CourseCategory")["Amount"].sum().reset_index()
... fig1 = px.bar(rev_cat, x="CourseCategory", y="Amount")
... st.plotly_chart(fig1, use_container_width=True)
... 
... # Payment Methods
... st.subheader("Payment Method Distribution")
... pay = df["PaymentMethod"].value_counts().reset_index()
pay.columns = ["PaymentMethod", "Count"]
fig2 = px.pie(pay, names="PaymentMethod", values="Count")
st.plotly_chart(fig2, use_container_width=True)

# Top Courses
st.subheader("Top Courses")
top_courses = df.groupby("CourseName").size().reset_index(name="Enrollments")
top_courses = top_courses.sort_values("Enrollments", ascending=False).head(10)
fig3 = px.bar(top_courses, x="CourseName", y="Enrollments")
st.plotly_chart(fig3, use_container_width=True)
SyntaxError: multiple statements found while compiling a single statement
