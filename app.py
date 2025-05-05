import streamlit as st
import zipfile
import os
from io import BytesIO

def create_zip_file(files):
    """Create a ZIP file from the provided files."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for file_name, file_content in files.items():
            zf.writestr(file_name, file_content)
    zip_buffer.seek(0)
    return zip_buffer

# Define your form templates here
FORM_TEMPLATES = {
    "Investigator_Brochure.docx": "This is a template for Investigator Brochure...",
    "Informed_Consent_Form.docx": "Template for Informed Consent Form...",
    "Protocol.docx": "Study Protocol Template...",
    "Case_Report_Form.docx": "CRF Template...",
    "Monitoring_Plan.docx": "Monitoring Plan Template...",
    "Site_Selection_Form.docx": "Site Selection Template...",
    "Ethics_Approval.docx": "Ethics Committee Approval Template...",
    "Investigator_Agreement.docx": "Investigator Agreement Template...",
    "Drug_Accountability_Form.docx": "Drug Accountability Template...",
    "Safety_Report.docx": "Safety Reporting Template..."
}

# Streamlit app setup
st.set_page_config(page_title="eTMF Training App", layout="wide")

# App title
st.title("eTMF Training App for Clinical Research")

# Introduction
st.write("""
Welcome to the eTMF training platform! Follow these steps:
1. Read the provided trial scenario.
2. Download and fill out the required eTMF forms.
3. Upload your completed forms.
4. Submit the forms for assessment.
""")

# Step 1: Trial Scenario
st.header("Trial Scenario")
trial_scenario = "This is a placeholder for the trial scenario. Replace this text with the actual scenario content."
st.text_area("Scenario Details", trial_scenario, height=200, disabled=True)

# Step 2: Download Templates Section
st.header("Download Form Templates")
st.write("Download the templates below, fill them out, and then upload them in the next section.")

# Create two columns for better organization
col1, col2 = st.columns(2)

# Display download buttons for each template
with col1:
    for i, (template_name, template_content) in enumerate(list(FORM_TEMPLATES.items())[:5]):
        st.download_button(
            label=f"Download {template_name}",
            data=template_content,
            file_name=template_name,
            mime="application/octet-stream"
        )

with col2:
    for i, (template_name, template_content) in enumerate(list(FORM_TEMPLATES.items())[5:]):
        st.download_button(
            label=f"Download {template_name}",
            data=template_content,
            file_name=template_name,
            mime="application/octet-stream"
        )

# Step 3: Upload Completed Forms
st.header("Upload Completed Forms")
uploaded_files = st.file_uploader(
    "Upload your completed forms (ZIP or individual files)", 
    type=["zip", "docx", "txt", "pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Successfully uploaded {len(uploaded_files)} file(s)!")
    
    # If user uploaded individual files, offer to zip them
    if len(uploaded_files) > 1 and not any(file.name.endswith('.zip') for file in uploaded_files):
        if st.button("Create ZIP from uploaded files"):
            files_to_zip = {}
            for uploaded_file in uploaded_files:
                files_to_zip[uploaded_file.name] = uploaded_file.getvalue()
            
            zip_file = create_zip_file(files_to_zip)
            st.download_button(
                label="Download as ZIP",
                data=zip_file,
                file_name="completed_forms.zip",
                mime="application/zip"
            )

# Step 4: Submit for Assessment
st.header("Submit for Assessment")
if st.button("Submit Documents for Assessment"):
    if uploaded_files:
        st.success("Your documents have been submitted for assessment!")
        # Here you would add your assessment logic
    else:
        st.error("Please upload your completed forms before submitting.")
