import streamlit as st
import pandas as pd
import re
from streamlit_star_rating import st_star_rating
from streamlit_gsheets import GSheetsConnection

# Set up Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Custom styling
st.markdown("""
    <style>
        .main {background-color: #f4f4f8;}
        h1 {color: #4CAF50; text-align: center;}
        h2 {color: #333366;}
        .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; font-size: 16px; padding: 10px 24px;}
        .stRadio > div, .stSelectbox > div, .stTextInput > div {background-color: #ffffff; padding: 10px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🚀 Career Growth Survey")

st.markdown("""
    Thank you for participating in our career growth survey! Your insights will help us better understand professional development within the company.
    Please answer the following questions honestly.
""")

# Email input
email = st.text_input("**Enter your email (optional):**")

def is_valid_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Job Information
st.header("💼 Job Information")

job_title = st.text_input("**What is your current job title?**")

years_in_role = st.radio("**How many years have you worked in your current role?**", [
    "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "10+ years"
])

years_in_company = st.radio("**How long have you been with this company?**", [
    "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "10+ years"
])

promotion = st.radio("**Have you received a promotion in the last 2 years?**", [
    "Yes", "No", "Currently being considered for one"
])

# Performance Rating
st.header("📊 Performance Rating")

performance_questions = [
    "I consistently meet or exceed the goals and targets set for my role.",
    "I receive positive feedback from my managers and colleagues about my work.",
    "I handle my core job responsibilities with accuracy and efficiency.",
    "I take initiative beyond my job description when needed.",
    "My work has a measurable impact on team or company outcomes."
]

performance_ratings = {q: st_star_rating(label=q, maxValue=5, defaultValue=0) for q in performance_questions}

# Potential Rating
st.header("🌟 Potential Rating")

potential_questions = [
    "I am eager to learn new skills and take on more challenging tasks.",
    "I adapt quickly to changes and problem-solve effectively.",
    "I am open to leadership roles or greater responsibilities in the future.",
    "I consistently seek feedback to improve myself.",
    "I have a clear vision for my career growth within the company."
]

potential_ratings = {q: st_star_rating(label=q, maxValue=5, defaultValue=0) for q in potential_questions}

# 9-Box Grid Placement
st.header("📈 9-Box Grid Placement")

grid_placement = st.radio("**Where do you think you currently stand on the 9-box grid?**", [
    "High Performance, High Potential", "High Performance, Medium Potential", "High Performance, Low Potential",
    "Medium Performance, High Potential", "Medium Performance, Medium Potential", "Medium Performance, Low Potential",
    "Low Performance, High Potential", "Low Performance, Medium Potential", "Low Performance, Low Potential",
    "I’m not sure"
])

# Career Support Feedback
career_feedback = st.text_area("**If you could change one thing about how your company supports your career growth, what would it be?**")

@st.dialog("🌟 Prompt Engineering Tip 🌟 ")
def tip():
    st.write("**Struggling to get the right answer from GPT?**")
    st.write("Try adding this simple instruction at the start of your question:")
    st.markdown("### *Take a deep breath, solve the problem step by step:*")
    st.info("This helps GPT slow down and think through each part of the problem carefully, just like a person would. As it encourages the model to break down the problem into manageable steps—mimicking the detailed reasoning often found in its training data—which can lead to more accurate and comprehensive answers.")
    st.write("**See the difference:**")
    st.write(" *Before using the prompt:* GPT gave the wrong answer.")
    st.image("image/Before.png", "Before Adding the Prompt")
    st.write("✅ *After using the prompt:* GPT provided the correct answer.")
    st.image("image/After1.png")
    st.image("image/After2.png", "After Adding the Prompt")
    st.link_button("Read More", "https://arxiv.org/pdf/2309.03409")

# Submission logic
if st.button("Submit ✅"):
    if not is_valid_email(email):
        st.error("📧 Please enter a valid email address.")
    else:
        new_row = pd.DataFrame([[
            job_title, years_in_role, years_in_company, promotion, grid_placement, career_feedback, email,
            *performance_ratings.values(), *potential_ratings.values()
        ]], columns=[
            "Job Title", "Years in Role", "Years in Company", "Promotion", "Grid Placement", "Career Feedback", "Email",
            *[f"Performance: {q}" for q in performance_questions],
            *[f"Potential: {q}" for q in potential_questions]
        ])
        sheet_data = conn.read()
        updated_data = pd.concat([sheet_data, new_row], ignore_index=True)
        conn.update(data=updated_data)
        st.cache_data.clear()
        st.success("🎉 Thank you for completing the survey! Your feedback is invaluable.")
        st.balloons()
        tip()
