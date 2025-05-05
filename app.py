import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

# Configuration
st.set_page_config(page_title="ZAN-202 Protocol Deviation Log", layout="wide")

# App title
st.title("ZAN-202: Protocol Deviation Log Training")
st.subheader("A Phase IIb Study in Type 2 Diabetes")

# Scenario Section
st.header("📋 Study Scenario")
scenario = """
**Sponsor:** Zenith Pharmaceuticals  
**CRO:** Apex CRO  
**Site Number:** 105  
**Site Name:** Medistar Clinical Research Center, Chennai  
**Principal Investigator:** Dr. Kiran Deshmukh  
**Investigational Product:** ZAN-GLU IV Injection  

**Identified Deviations:**
1. **SUB-022:** Missed Screening labs (Protocol Section 6.1 violation)  
2. **SUB-025:** Month 3 visit 7 days late (±5 day window allowed, Section 5.2)  
3. **SUB-030:** Signed outdated ICF (v3.0 instead of v4.0)  
"""
st.markdown(scenario)

# Form Template
st.header("✍️ Protocol Deviation Log")

# Create editable dataframe
deviation_data = {
    "Deviation ID": ["DEV-001", "DEV-002", "DEV-003"],
    "Date Identified": ["2025-05-20", "2025-05-20", "2025-05-19"],
    "Subject ID": ["SUB-022", "SUB-025", "SUB-030"],
    "Protocol Section Violated": ["Section 6.1", "Section 5.2", "ICF Version"],
    "Description of Deviation": [
        "Missed Screening labs, proceeded to randomization",
        "Month 3 visit 7 days late (window ±5 days)",
        "Signed outdated ICF (v3.0 instead of v4.0)"
    ],
    "Action Taken": [
        "Enrollment halted, deviation report submitted",
        "Visit completed, staff retraining conducted",
        "Re-consented with correct version, CAPA implemented"
    ],
    "Reported to IRB? (Y/N)": ["Y", "Y", "Y"],
    "Date Reported to Sponsor/IRB": ["2025-05-21", "2025-05-22", "2025-05-21"]
}

df = pd.DataFrame(deviation_data)
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Date Identified": st.column_config.DateColumn("Date Identified"),
        "Date Reported to Sponsor/IRB": st.column_config.DateColumn("Report Date")
    }
)

# Header Information
st.divider()
st.subheader("Study Information")
col1, col2 = st.columns(2)
with col1:
    study_title = st.text_input("Study Title / Protocol Number", "ZAN-202: A Phase IIb Study in Type 2 Diabetes")
    site_number = st.text_input("Site Number", "105")
    principal_investigator = st.text_input("Principal Investigator", "Dr. Kiran Deshmukh")

with col2:
    sponsor = st.text_input("Sponsor", "Zenith Pharmaceuticals")
    cro = st.text_input("CRO (if applicable)", "Apex CRO")
    investigational_product = st.text_input("Investigational Product Name", "ZAN-GLU IV Injection")

# Download Section
st.header("💾 Download Completed Log")

def create_zip():
    zip_buffer = BytesIO()
    
    # Create CSV
    csv = edited_df.to_csv(index=False)
    
    # Create header info text
    header_info = f"""Study Title / Protocol Number: {study_title}
Site Number: {site_number}
Site Name: Medistar Clinical Research Center, Chennai
Principal Investigator: {principal_investigator}
Sponsor: {sponsor}
CRO (if applicable): {cro}
Investigational Product Name: {investigational_product}
Log Start Date: 2025-05-01
Log End Date: 2025-05-31\n\n"""
    
    # Combine header and CSV
    full_content = header_info + csv
    
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("Protocol_Deviation_Log.csv", full_content)
    
    zip_buffer.seek(0)
    return zip_buffer

if st.button("Generate Download Package"):
    zip_file = create_zip()
    st.download_button(
        label="Download ZIP",
        data=zip_file,
        file_name="ZAN-202_Deviation_Log.zip",
        mime="application/zip"
    )

# Submission Section
st.header("📤 Submit Completed Log")
uploaded_file = st.file_uploader("Upload your completed deviation log", type=["csv", "zip"])
if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")
    if st.button("Submit for Review"):
        st.balloons()
        st.success("Submission complete! Your trainer will review your entries.")
