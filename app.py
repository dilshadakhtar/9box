import streamlit as st
import pandas as pd
import os

# Define CSV file path
DATA_FILE = 'survey_responses.csv'

# # Initialize the CSV file if not present
# if not os.path.exists(DATA_FILE):
#     pd.DataFrame(columns=[
#         'Job Title', 'Role Tenure', 'Company Tenure', 'Promotion',
#         'Performance Scores', 'Potential Scores', 'Familiarity', 'Self Placement',
#         'Manager Communication', 'Model Accuracy', 'Support Needed'
#     ]).to_csv(DATA_FILE, index=False)

# Page title and intro
st.title('📊 HR Project: Evaluating the 9-Box Talent Management Model')

st.markdown('''
### Purpose of this survey:
Hi there! I'm a student working on a Human Resource Management project focused on understanding how effectively the 9-box talent management model identifies and develops talent within organizations.

Your input will help me assess how this tool works in real-world settings — so thank you for sharing your honest thoughts! It’ll take less than 5 minutes.
''')

# Section 1: Background Information
st.header('Section 1: Background Information')

job_title = st.text_input("1. What is your current job title?")

role_tenure = st.radio("2. How long have you been in your current role?", [
    "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "10+ years"
])

company_tenure = st.radio("3. How long have you been with this company?", [
    "Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "10+ years"
])

promotion = st.radio("4. Have you received a promotion in the last 2 years?", [
    "Yes", "No", "Currently being considered for one"
])

# Section 2: Self-Assessment – Performance
st.header('Section 2: Self-Assessment – Performance')

st.markdown("On a scale of 1-5, rate yourself on the following aspects of job performance:")

performance_qs = [
    "I consistently meet or exceed the goals and targets set for my role.",
    "I receive constructive feedback from my managers and colleagues about my work.",
    "I manage my core job responsibilities with accuracy and efficiency.",
    "I proactively take on tasks outside my job description.",
    "My work directly contributes to team or company success."
]

performance_scores = []
for q in performance_qs:
    performance_scores.append(st.slider(q, 1, 5))

# Section 3: Self-Assessment – Potential
st.header('Section 3: Self-Assessment – Potential')

st.markdown("On a scale of 1-5, rate yourself on the following indicators of future potential:")

potential_qs = [
    "I actively seek opportunities to learn new skills and grow.",
    "I quickly adapt to changes and solve problems under pressure.",
    "I am open to taking on leadership roles or additional responsibilities.",
    "I regularly ask for feedback to improve my performance.",
    "I have a clear plan for advancing my career within this company."
]

potential_scores = []
for q in potential_qs:
    potential_scores.append(st.slider(q, 1, 5))

# Section 4: Understanding the 9-Box Model
st.header('Section 4: Understanding the 9-Box Model')

familiarity = st.radio("15. Are you familiar with the 9-box talent management model used to assess performance and potential?", [
    "Yes, I understand it well", "Yes, but I only have a basic understanding",
    "No, I’ve heard of it but don’t know much about it", "No, I’ve never heard of it"
])

self_placement = st.radio("16. If you had to place yourself on the 9-box grid, where do you think you currently stand?", [
    "High Performance, High Potential", "High Performance, Medium Potential", "High Performance, Low Potential",
    "Medium Performance, High Potential", "Medium Performance, Medium Potential", "Medium Performance, Low Potential",
    "Low Performance, High Potential", "Low Performance, Medium Potential", "Low Performance, Low Potential",
    "I’m not sure"
])

# Section 5: Feedback on Career Development
st.header('Section 5: Feedback on Career Development')

manager_communication = st.radio("17. How clearly has your manager communicated your position on the 9-box grid?", [
    "Very clearly — I know exactly where I stand", "Somewhat clearly — I have a general idea",
    "Not clearly — I’m unsure of my placement", "Not at all — I’ve never been told about it"
])

model_accuracy = st.text_area("18. Do you feel the 9-box model accurately reflects your performance and potential? Why or why not?")

support_needed = st.text_area("19. What additional support would help you move to a higher box in the 9-box grid?")

# Submit button and save data
if st.button('Submit Survey'):
    new_data = pd.DataFrame({
        'Job Title': [job_title],
        'Role Tenure': [role_tenure],
        'Company Tenure': [company_tenure],
        'Promotion': [promotion],
        'Performance Scores': [performance_scores],
        'Potential Scores': [potential_scores],
        'Familiarity': [familiarity],
        'Self Placement': [self_placement],
        'Manager Communication': [manager_communication],
        'Model Accuracy': [model_accuracy],
        'Support Needed': [support_needed]
    })
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success("✅ Thank you for your support! Your feedback has been recorded.")

st.markdown('''
If you have any additional thoughts or ideas, please feel free to share them!
''')
