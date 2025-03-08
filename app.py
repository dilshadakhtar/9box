# example/st_app_gsheets_using_service_account.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Read Google Sheet as DataFrame")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(
    worksheet="Sheet1",
    ttl="10m",
    usecols=[0, 1],
    nrows=3,
)

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")
