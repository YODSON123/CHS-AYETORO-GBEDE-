import streamlit as st
import pandas as pd
import os

DB_FILE = "chs_records.csv"

if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["ID", "Name", "Punctuality", "Neatness", "Behavior", "Principal_Comment"])

st.title("🏫 COMMUNITY HIGH SCHOOL, AYETORO GBEDE")

# Admin Sidebar
pw = st.sidebar.text_input("Staff Password", type="password")
if pw == "chs123":
    st.header("Admin Entry")
    with st.form("entry"):
        id_no = st.text_input("Student ID")
        name = st.text_input("Name")
        comment = st.text_area("Principal's Comment")
        if st.form_submit_button("Save"):
            new_row = pd.DataFrame([[id_no, name, "Good", "Good", "Good", comment]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Saved!")

# Student View
st.header("Check Result")
search = st.text_input("Enter ID")
if st.button("Search"):
    res = df[df["ID"].astype(str) == search]
    if not res.empty:
        st.write(f"**Name:** {res.iloc[0]['Name']}")
        st.write(f"**Principal's Comment:** {res.iloc[0]['Principal_Comment']}")
    else:
        st.error("Not found")
