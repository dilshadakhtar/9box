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
    It consists of a 3x3 matrix with different categories that help in succession planning, identifying high performers,
    and understanding development needs. The grid is often used in HR discussions to strategize talent management effectively.
    """)
    st.link_button("Go to Video Explaination", "https://youtu.be/B6SZJcydsYc")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 1

# Page 1: Demographics
if st.session_state.page == 1:
    st.header("👤 Demographic Information")
    email = st.text_input("**Enter your email (optional):**")
    job_role = st.selectbox("**What is your job role?**", ["HR", "People’s Manager", "Individual Contributor", "Other"], index=None)
    years_experience = st.radio("**How many years of experience do you have?**", ["0-5", "6-10", "11-15", "15+"], index=None)
    org_size = st.radio("**What is the size of your organization?**", ["<100", "100-500", "501-1000", "1001+"], index=None)
    uses_9box = st.radio("**Has your organization implemented the 9-box grid for talent assessment?**", ["Yes", "No", "Not Sure"], index=None)

    if st.button("Next ▶️"):
        st.session_state.uses_9box = uses_9box
        st.session_state.job_role = job_role
        st.session_state.email = email
        st.session_state.years_experience = years_experience
        st.session_state.org_size = org_size
        st.session_state.page = 2
        st.rerun()

# Page 2: Conditional Questions
elif st.session_state.page == 2:
    if st.session_state.uses_9box == "Yes":
        st.header("📌 Usage of the 9-Box Grid")
        usage_frequency = st.radio("**How frequently do you use the 9-box grid?**", ["Quarterly", "Yearly", "Bi-Yearly", "Other"], index=None)
        primary_purpose = st.selectbox("**What is the primary purpose of using the 9-box grid?**", ["Talent Review", "Succession Planning", "Employee Development", "Performance Evaluation", "Other"], index=None)
        ease_of_use = st.radio("**How do you rate the ease of using the 9-box grid?**", ["Very Difficult", "Difficult", "Neutral", "Easy", "Very Easy"], index=None)
        stakeholders = st.multiselect("**Who are the stakeholders involved?**", ["HR", "Managers", "Senior Management", "Other"], default=None)

        st.header("📈 Effectiveness & Challenges")
        talent_retention = st.radio("**Has it improved talent retention?**", ["Not Effective", "Somewhat Effective", "Neutral", "Effective", "Very Effective"], index=None)
        succession_usefulness = st.radio("**How useful is it for succession planning?**", ["Not Useful", "Somewhat Useful", "Neutral", "Useful", "Very Useful"], index=None)
        fairness = st.radio("**Is the assessment fair?**", ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], index=None)
        challenges = st.multiselect("**Challenges faced?**", ["Subjectivity", "Lack of Managerial Buy-in", "Difficulty in Implementation", "Lack of Training", "Other"], default=None)
        recommend_9box = st.radio("**Would you recommend it?**", ["Yes", "No", "Maybe"],index=None)
    
    else:
        st.header("🛠 Talent Assessment Approaches")
        assessment_methods = st.multiselect("**What methods does your organization use?**", ["Performance Reviews", "Competency-Based Evaluation", "9-Box Grid", "Peer Feedback", "Other"], default=None)
        reason_not_using = st.multiselect("**Reasons for not using 9-box?**", ["Unfamiliarity", "Preference for Other Methods", "Complexity", "Lack of Resources", "Other"], default=None)
        structured_effectiveness = st.radio("**Are structured tools effective?**", ["Not Effective", "Somewhat Effective", "Neutral", "Effective", "Very Effective"], index=None)
        adopt_future = st.radio("**Would you adopt it in future?**", ["Yes", "No", "Maybe"], index=None)
    
    additional_comments = st.text_area("**Any additional comments?**")
    
    if st.button("Submit ✅"):
        new_row = pd.DataFrame([[st.session_state.job_role, st.session_state.years_experience, st.session_state.org_size, st.session_state.uses_9box, usage_frequency if st.session_state.uses_9box == "Yes" else "N/A", primary_purpose if st.session_state.uses_9box == "Yes" else "N/A", ease_of_use if st.session_state.uses_9box == "Yes" else "N/A", stakeholders if st.session_state.uses_9box == "Yes" else "N/A", talent_retention if st.session_state.uses_9box == "Yes" else "N/A", succession_usefulness if st.session_state.uses_9box == "Yes" else "N/A", fairness if st.session_state.uses_9box == "Yes" else "N/A", challenges if st.session_state.uses_9box == "Yes" else "N/A", recommend_9box if st.session_state.uses_9box == "Yes" else "N/A", assessment_methods if st.session_state.uses_9box != "Yes" else "N/A", reason_not_using if st.session_state.uses_9box != "Yes" else "N/A", structured_effectiveness if st.session_state.uses_9box != "Yes" else "N/A", adopt_future if st.session_state.uses_9box != "Yes" else "N/A", additional_comments, st.session_state.email]], columns=["Job Role", "Years of Experience", "Organization Size", "Uses 9-Box Grid", "Usage Frequency", "Primary Purpose", "Ease of Use", "Stakeholders", "Talent Retention", "Succession Usefulness", "Fairness", "Challenges", "Recommend 9-Box", "Assessment Methods", "Reason Not Using", "Structured Effectiveness", "Adopt Future", "Additional Comments", "Email"])
        sheet_data = conn.read()
        updated_data = pd.concat([sheet_data, new_row], ignore_index=True)
        conn.update(data=updated_data)
        st.cache_data.clear()
        st.success("🎉 Thank you for completing the survey!")
        st.balloons()
