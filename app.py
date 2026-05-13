    import streamlit as st
import pandas as pd
import os

DB_FILE = "chs_records.csv"

# Load or create database
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["ID", "Name", "Punctuality", "Neatness", "Principal_Comment"])

st.set_page_config(page_title="CHS Ayetoro Gbede", layout="centered")
st.title("🏫 COMMUNITY HIGH SCHOOL, AYETORO GBEDE")

menu = ["Student Result Portal", "Staff/Admin Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Staff/Admin Login":
    pw = st.sidebar.text_input("Access Password", type="password")
    if pw == "chs123":
        st.header("Upload Student Result")
        with st.form("result_form", clear_on_submit=True):
            id_no = st.text_input("Admission Number (ID)")
            name = st.text_input("Student Name")
            
            st.subheader("Psychomotor Assessment")
            punc = st.select_slider("Punctuality", options=["Poor", "Fair", "Good", "Very Good", "Excellent"])
            neat = st.select_slider("Neatness", options=["Poor", "Fair", "Good", "Very Good", "Excellent"])
            
            comment = st.text_area("Principal's Remark")
            
            if st.form_submit_button("Save to Result Booklet"):
                new_data = pd.DataFrame([[id_no, name, punc, neat, comment]], columns=df.columns)
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"Successfully saved result for {name}!")

else:
    st.header("Check Your Result")
    search_id = st.text_input("Enter your Admission Number")
    if st.button("Generate Result"):
        result = df[df["ID"].astype(str) == search_id]
        if not result.empty:
            res = result.iloc[-1] 
            st.markdown(f"### Result for {res['Name']}")
            st.write("---")
            st.write("**Psychomotor Domain**")
            st.table({
                "Trait": ["Punctuality", "Neatness"],
                "Rating": [res['Punctuality'], res['Neatness']]
            })
            st.info(f"**Principal's Comment:** {res['Principal_Comment']}")
        else:
            st.error("No record found. Please check the ID or contact the school admin.")
    
