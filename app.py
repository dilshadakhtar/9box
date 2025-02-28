import streamlit as st
import pandas as pd
import pymysql

# Database connection setup
db_secrets = st.secrets["database"]

conn = pymysql.connect(
    host=db_secrets["host"],
    user=db_secrets["user"],
    password=db_secrets["password"],
    database=db_secrets["database"],
    port=int(db_secrets["port"])
)
cursor = conn.cursor()

# Create table if not exists
create_table_query = '''
CREATE TABLE IF NOT EXISTS survey_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255),
    role_tenure VARCHAR(50),
    company_tenure VARCHAR(50),
    promotion VARCHAR(50),
    performance_scores TEXT,
    potential_scores TEXT,
    familiarity VARCHAR(255),
    self_placement VARCHAR(255),
    manager_communication VARCHAR(255),
    model_accuracy TEXT,
    support_needed TEXT
);
'''
cursor.execute(create_table_query)
conn.commit()

# Page title and intro
st.title('📊 HR Project: Evaluating the 9-Box Talent Management Model')

st.markdown('''
### Purpose of this survey:
Hi there! I'm a student working on a Human Resource Management project focused on understanding how effectively the 9-box talent management model identifies and develops talent within organizations.

Your input will help me assess how this tool works in real-world settings — so thank you for sharing your honest thoughts! It’ll take less than 5 minutes.
''')

# Collect user inputs
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

# Collect performance scores
st.header('Section 2: Self-Assessment – Performance')

performance_qs = [
    "I consistently meet or exceed the goals and targets set for my role.",
    "I receive constructive feedback from my managers and colleagues about my work.",
    "I manage my core job responsibilities with accuracy and efficiency.",
    "I proactively take on tasks outside my job description.",
    "My work directly contributes to team or company success."
]

performance_scores = [st.slider(q, 1, 5) for q in performance_qs]

# Collect potential scores
st.header('Section 3: Self-Assessment – Potential')

potential_qs = [
    "I actively seek opportunities to learn new skills and grow.",
    "I quickly adapt to changes and solve problems under pressure.",
    "I am open to taking on leadership roles or additional responsibilities.",
    "I regularly ask for feedback to improve my performance.",
    "I have a clear plan for advancing my career within this company."
]

potential_scores = [st.slider(q, 1, 5) for q in potential_qs]

# Understanding the 9-box model
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

# Feedback section
st.header('Section 5: Feedback on Career Development')

manager_communication = st.radio("17. How clearly has your manager communicated your position on the 9-box grid?", [
    "Very clearly — I know exactly where I stand", "Somewhat clearly — I have a general idea",
    "Not clearly — I’m unsure of my placement", "Not at all — I’ve never been told about it"
])

model_accuracy = st.text_area("18. Do you feel the 9-box model accurately reflects your performance and potential? Why or why not?")

support_needed = st.text_area("19. What additional support would help you move to a higher box in the 9-box grid?")

# Store data in database
if st.button('Submit Survey'):
    insert_query = '''
    INSERT INTO survey_responses (
        job_title, role_tenure, company_tenure, promotion,
        performance_scores, potential_scores, familiarity, self_placement,
        manager_communication, model_accuracy, support_needed
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        job_title, role_tenure, company_tenure, promotion,
        str(performance_scores), str(potential_scores), familiarity, self_placement,
        manager_communication, model_accuracy, support_needed
    ))
    conn.commit()
    st.success("✅ Thank you for your support! Your feedback has been recorded.")

conn.close()

st.markdown('''
If you have any additional thoughts or ideas, please feel free to share them!
''')
