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
st.title("📊 Effectiveness of the 9-Box Grid in HR Decision-Making")
st.markdown("""
    This survey aims to evaluate the effectiveness of the 9-box grid in HR decision-making processes. Your responses will help improve talent assessment methodologies.
""")

# Email input
email = st.text_input("**Enter your email (optional):**")

def is_valid_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Section 1: Demographic Information
st.header("👤 Demographic Information")
job_role = st.selectbox("**What is your job role?**", ["HR", "People’s Manager", "Individual Contributor", "Other"])
years_experience = st.radio("**How many years of experience do you have?**", ["0-5", "6-10", "11-15", "15+"])
org_size = st.radio("**What is the size of your organization?**", ["<100", "100-500", "501-1000", "1001+"])
uses_9box = st.radio("**Has your organization implemented the 9-box grid for talent assessment?**", ["Yes", "No", "Not Sure"])

# Conditional Questions Based on 9-Box Implementation
if uses_9box == "Yes":
    st.header("📌 Usage of the 9-Box Grid")
    usage_frequency = st.radio("**How frequently do you use the 9-box grid?**", ["Quarterly", "Yearly", "Bi-Yearly", "Other"])
    primary_purpose = st.selectbox("**What is the primary purpose of using the 9-box grid?**", ["Talent Review", "Succession Planning", "Employee Development", "Performance Evaluation", "Other"])
    ease_of_use = st.radio("**How do you rate the ease of using the 9-box grid?**", ["Very Difficult", "Difficult", "Neutral", "Easy", "Very Easy"])
    stakeholders = st.multiselect("**Who are the stakeholders involved in the 9-box grid assessment?**", ["HR", "Managers", "Senior Management", "Other"])
    
    st.header("📈 Effectiveness of the 9-Box Grid")
    talent_retention = st.radio("**Have you noticed improvements in talent retention or development?**", ["Not Effective", "Somewhat Effective", "Neutral", "Effective", "Very Effective"])
    succession_usefulness = st.radio("**How useful is the 9-box grid in making succession planning decisions?**", ["Not Useful", "Somewhat Useful", "Neutral", "Useful", "Very Useful"])
    fairness = st.radio("**Does the 9-box grid provide a fair and unbiased assessment?**", ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"])
    
    st.header("⚠️ Challenges and Improvements")
    challenges = st.multiselect("**What are the main challenges in using the 9-box grid?**", ["Subjectivity", "Lack of Managerial Buy-in", "Difficulty in Implementation", "Lack of Training", "Other"])
    recommend_9box = st.radio("**Would you recommend the use of the 9-box grid?**", ["Yes", "No", "Maybe"])
    additional_comments = st.text_area("**Any additional comments or suggestions?**")
else:
    st.header("🛠 Talent Assessment Approaches")
    assessment_methods = st.multiselect("**What methods does your organization use for talent assessment?**", ["Performance Reviews", "Competency-Based Evaluation", "9-Box Grid", "Peer Feedback", "Other"])
    reason_not_using = st.multiselect("**If your organization does not use the 9-box grid, what are the reasons?**", ["Unfamiliarity", "Preference for Other Methods", "Complexity", "Lack of Resources", "Other"])
    structured_effectiveness = st.radio("**How effective are structured talent assessment tools?**", ["Not Effective", "Somewhat Effective", "Neutral", "Effective", "Very Effective"])
    adopt_future = st.radio("**Would you be open to adopting the 9-box grid in the future?**", ["Yes", "No", "Maybe"])
    additional_comments = st.text_area("**Any additional comments or suggestions?**")

# Submission logic
if st.button("Submit ✅"):
    if not is_valid_email(email):
        st.error("📧 Please enter a valid email address.")
    else:
        new_row = pd.DataFrame([[job_role, years_experience, org_size, uses_9box, usage_frequency if uses_9box == "Yes" else "N/A", primary_purpose if uses_9box == "Yes" else "N/A", ease_of_use if uses_9box == "Yes" else "N/A", stakeholders if uses_9box == "Yes" else "N/A", talent_retention if uses_9box == "Yes" else "N/A", succession_usefulness if uses_9box == "Yes" else "N/A", fairness if uses_9box == "Yes" else "N/A", challenges if uses_9box == "Yes" else "N/A", recommend_9box if uses_9box == "Yes" else "N/A", assessment_methods if uses_9box != "Yes" else "N/A", reason_not_using if uses_9box != "Yes" else "N/A", structured_effectiveness if uses_9box != "Yes" else "N/A", adopt_future if uses_9box != "Yes" else "N/A", additional_comments, email]], columns=["Job Role", "Years of Experience", "Organization Size", "Uses 9-Box Grid", "Usage Frequency", "Primary Purpose", "Ease of Use", "Stakeholders", "Talent Retention", "Succession Usefulness", "Fairness", "Challenges", "Recommend 9-Box", "Assessment Methods", "Reason Not Using", "Structured Effectiveness", "Adopt Future", "Additional Comments", "Email"])
        sheet_data = conn.read()
        updated_data = pd.concat([sheet_data, new_row], ignore_index=True)
        conn.update(data=updated_data)
        updated_data.to_csv("survey_results.csv", index=False)
        st.cache_data.clear()
        st.success("🎉 Thank you for completing the survey! Your feedback is invaluable.")
        st.balloons()
