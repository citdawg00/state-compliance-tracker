import streamlit as st
import pandas as pd
 
st.set_page_config(layout="wide")
 
st.title("State Compliance Tracker")
 
# ========================
# GLOBAL COMPANY INPUTS
# ========================
st.sidebar.header("Company Compliance Inputs")
 
nde = st.sidebar.selectbox(
    "Did you complete an NDE?", ["Yes", "No"], key="nde"
)
 
sec503 = st.sidebar.selectbox(
    "Did you complete a Section 503 AAP?", ["Yes", "No"], key="sec503"
)
 
vevraa = st.sidebar.selectbox(
    "Did you complete a VEVRAA AAP?", ["Yes", "No"], key="vevraa"
)
 
pay_equity = st.sidebar.selectbox(
    "Did you complete Annual Pay Equity Reporting?", ["Yes", "No"], key="pay_equity"
)
 
# ========================
# FILE UPLOAD
# ========================
uploaded_file = st.file_uploader("Upload State/Employee File (Excel)", type=["xlsx"])
 
# ========================
# PROCESS FILE
# ========================
if uploaded_file is not None:
 
    df = pd.read_excel(uploaded_file)
 
    st.write("### Uploaded Data")
    st.dataframe(df)
 
    results = []
 
    for index, row in df.iterrows():
        state = str(row["State"]).strip().upper()
        employees = int(row["Employees"])
 
        if employees == 0:
            continue
 
        # ===== DEFAULT VALUES =====
        status = "YES"
        requirement = "Nondiscriminatory"
        notes = ""
        comp = ""
 
        # ==========================
        # BASELINE (NDE)
        # ==========================
        if nde == "Yes":
            notes = "Current reporting fulfills request"
        else:
            status = "CONDITIONAL"
            notes = "Nondiscriminatory reporting not confirmed"
 
        # ==========================
        # SAFE HARBOR STATES (Pay Equity)
        # ==========================
        if state in ["CO", "MA", "OR", "WA", "MD"]:
            requirement = "Safe Harbor Pay Equity"
 
            if pay_equity == "Yes":
                status = "YES"
                notes = "Fulfilled with Annual Pay Reporting"
                comp = "Ensure pay transparency in job posting"
            else:
                status = "CONDITIONAL"
                notes = "Pay equity reporting not confirmed"
 
        # ==========================
        # TRUE REPORTING STATES (PROMPTS REQUIRED)
        # ==========================
        if state in ["CA", "IL"]:
 
            requirement = "State Reporting Required"
 
            filed = st.selectbox(
                f"{state}: Did you file required report?",
                ["Select", "Yes", "No"],
                key=f"file_{state}_{index}"
            )
 
            if filed == "Yes":
                date = st.text_input(
                    f"{state}: Enter filing date",
                    key=f"date_{state}_{index}"
                )
 
                if date:
                    status = "YES"
                    notes = f"Current reporting fulfills request + {state} reporting filed"
                    comp = f"{state} filing completed on {date}"
                else:
                    status = "CONDITIONAL"
                    notes = "Filing indicated but documentation not confirmed"
                    comp = "Missing filing date"
 
            elif filed == "No":
                status = "CONDITIONAL"
                notes = "State-specific reporting may be required; confirmation needed"
                comp = "No filing confirmed"
 
            else:
                status = "CONDITIONAL"
                notes = "State-specific reporting may be required; confirmation needed"
                comp = ""
 
        # ==========================
        # CONTRACT-BASED STATES (NO PROMPTS)
        # ==========================
        if state in ["WI", "NJ", "MN", "VA", "CT", "NY", "DC", "KY", "ME"]:
            requirement = "AAP Required (Contract-Based)"
            status = "CONDITIONAL"
            notes = "Additional requirements apply only if covered state or public agency contracts exist"
            comp = ""
 
        # ==========================
        # THRESHOLD STATES (Example IL logic)
        # ==========================
        if state == "IL" and employees < 100:
            status = "CONDITIONAL"
            notes = "Do not meet employee threshold; current reporting fulfills nondiscriminatory requirements"
            comp = "Ensure pay transparency in job posting"
 
        if state == "MN" and employees < 40:
            status = "CONDITIONAL"
            notes = "Do not meet employee threshold for certificate; current reporting fulfills requirements"
            comp = "Ensure pay transparency in job posting"
         
 ============================
# GLOBAL NDE OVERRIDE
# ============================
if nde != "Yes" and status == "YES":
    status = "CONDITIONAL"
    notes = "Underlying nondiscriminatory compliance not satisfied (NDE not completed)"
        # ==========================
        # FINAL OUTPUT ROW
        # ==========================
        results.append({
            "State": state,
            "COMPLIANT?": status,
            "State Requirements": requirement,
            "State Requirements - Notes": notes,
            "Compensation": comp
        })
 
    results_df = pd.DataFrame(results)
 
    st.write("### Final Compliance Output")
    st.dataframe(results_df)
