import streamlit as st
import pandas as pd
import re
from streamlit_star_rating import st_star_rating
from streamlit_gsheets import GSheetsConnection

# Set up Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Custom Styling
st.markdown("""
    <style>
        .main {background-color: #f8f9fa;}
        h1 {color: #2C3E50; text-align: center;}
        h2 {color: #2980B9;}
        .stButton>button {background-color: #2980B9; color: white; border-radius: 8px; font-size: 16px; padding: 10px 24px;}
        .stRadio > div, .stSelectbox > div, .stTextInput > div, .stMultiselect > div {background-color: #ffffff; padding: 12px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("📊 Effectiveness of the 9-Box Grid in HR Decision-Making")
st.markdown("""
We are students from IIM Kozhikode conducting a survey for our Human Resource Management project.  
This study aims to assess the effectiveness of the 9-box grid in HR decision-making.
""")

# Explanation for 9-Box Grid
with st.expander("ℹ️ What is the 9-Box Grid?"):
    st.image("9Box.png")
    st.write("""
    The 9-box grid is a tool used in talent management to assess employees based on their performance and potential.
    It helps in succession planning, identifying high performers, and understanding development needs.
    """)
    st.link_button("Go to Video Explanation", "https://youtu.be/B6SZJcydsYc")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 1

# Page 1: Demographics
if st.session_state.page == 1:
    st.header("👤 Demographic Information")
    email = st.text_input("**Enter your email (optional):**")
    job_role = st.selectbox("**What is your job role?**", ["", "HR", "People’s Manager", "Individual Contributor", "Other"], index=0)
    years_experience = st.radio("**How many years of experience do you have?**", ["", "0-5", "6-10", "11-15", "15+"], index=0)
    org_size = st.radio("**What is the size of your organization?**", ["", "<100", "100-500", "501-1000", "1001+"], index=0)
    uses_9box = st.radio("**Has your organization implemented the 9-box grid for talent assessment?**", ["", "Yes", "No", "Not Sure"], index=0)

    if st.button("Next ▶️"):
        if not job_role or not years_experience or not org_size or not uses_9box:
            st.error("❗ Please fill all mandatory fields before proceeding.")
        else:
            st.session_state.update({
                "uses_9box": uses_9box,
                "job_role": job_role,
                "email": email,
                "years_experience": years_experience,
                "org_size": org_size,
                "page": 2
            })
            st.rerun()

# Page 2: Conditional Questions
elif st.session_state.page == 2:
    if st.session_state.uses_9box == "Yes":
        st.header("📌 Usage of the 9-Box Grid")
        usage_frequency = st.radio("**How frequently do you use the 9-box grid?**", ["", "Quarterly", "Yearly", "Bi-Yearly", "Other"], index=0)
        primary_purpose = st.selectbox("**Primary purpose of using 9-box?**", ["", "Talent Review", "Succession Planning", "Employee Development", "Performance Evaluation", "Other"], index=0)
        ease_of_use = st.radio("**Ease of use?**", ["", "Very Difficult", "Difficult", "Neutral", "Easy", "Very Easy"], index=0)
        stakeholders = st.multiselect("**Stakeholders involved?**", ["HR", "Managers", "Senior Management", "Other"], default=[])
        talent_retention = st.radio("**Improved talent retention?**", ["", "Not Effective", "Somewhat Effective", "Neutral", "Effective", "Very Effective"], index=0)
        succession_usefulness = st.radio("**Usefulness for succession planning?**", ["", "Not Useful", "Somewhat Useful", "Neutral", "Useful", "Very Useful"], index=0)
        fairness = st.radio("**Is the assessment fair?**", ["", "Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], index=0)
        challenges = st.multiselect("**Challenges faced?**", ["Subjectivity", "Lack of Managerial Buy-in", "Difficulty in Implementation", "Lack of Training", "Other"], default=[])
        recommend_9box = st.radio("**Would you recommend it?**", ["", "Yes", "No", "Maybe"], index=0)
    else:
        st.header("🛠 Talent Assessment Approaches")
        assessment_methods = st.multiselect("**Assessment methods used?**", ["Performance Reviews", "Competency-Based Evaluation", "9-Box Grid", "Peer Feedback", "Other"], default=[])
        reason_not_using = st.multiselect("**Reasons for not using 9-box?**", ["Unfamiliarity", "Preference for Other Methods", "Complexity", "Lack of Resources", "Other"], default=[])
        structured_effectiveness = st.radio("**Are structured tools effective?**", ["", "Not Effective", "Somewhat Effective", "Neutral", "Effective", "Very Effective"], index=0)
        adopt_future = st.radio("**Would you adopt it in future?**", ["", "Yes", "No", "Maybe"], index=0)
    
    additional_comments = st.text_area("**Any additional comments?**")
    
    if st.button("Submit ✅"):
        if st.session_state.uses_9box == "Yes" and (not usage_frequency or not primary_purpose or not ease_of_use or not talent_retention or not succession_usefulness or not fairness or not recommend_9box or not stakeholders or not challenges):
            st.error("❗ Please fill all mandatory fields before submitting.")
        elif st.session_state.uses_9box != "Yes" and (not structured_effectiveness or not adopt_future or not assessment_methods or not reason_not_using):
            st.error("❗ Please fill all mandatory fields before submitting.")
        else:
            st.success("🎉 Thank you for completing the survey!")
            st.balloons()
