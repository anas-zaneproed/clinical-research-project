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

# Streamlit app setup
st.set_page_config(page_title="eTMF Training App", layout="wide")

# App title
st.title("eTMF Training App for Clinical Research")

# Introduction
st.write("""
Welcome to the eTMF training platform! Follow these steps:
1. Read the provided trial scenario.
2. Fill out the required eTMF forms.
3. Download the forms as a ZIP file.
4. Submit the ZIP file for assessment.
""")

# Step 1: Trial Scenario
st.header("Trial Scenario")
trial_scenario = "This is a placeholder for the trial scenario. Replace this text with the actual scenario content."
st.text_area("Scenario Details", trial_scenario, height=200, disabled=True)

# Step 2: Fill Forms
st.header("Fill eTMF Forms")
form_files = {}
for i in range(1, 11):
    form_name = f"Form_{i}.txt"
    form_content = st.text_area(f"{form_name}", placeholder=f"Enter details for {form_name}")
    form_files[form_name] = form_content

# Step 3: Download ZIP
st.header("Download Completed Forms")
if st.button("Generate ZIP"):
    if all(content.strip() for content in form_files.values()):
        zip_file = create_zip_file(form_files)
        st.download_button(
            label="Download ZIP",
            data=zip_file,
            file_name="eTMF_forms.zip",
            mime="application/zip"
        )
    else:
        st.error("Please fill out all forms before generating the ZIP.")

# Step 4: Submit ZIP
st.header("Submit Your ZIP File")
uploaded_file = st.file_uploader("Upload your ZIP file for assessment", type="zip")
if uploaded_file is not None:
    st.success("Your file has been uploaded successfully!")
