import streamlit as st
import cv2
import PyPDF2  # Added for PDF handling

# Initialize blob detector parameters (unchanged)
blob_params = cv2.SimpleBlobDetector_Params()
blob_params.filterByInertia = False
blob_params.filterByConvexity = False
blob_params.filterByColor = True
blob_params.blobColor = 0
blob_params.filterByCircularity = True
blob_params.filterByArea = False
blob_detector = cv2.SimpleBlobDetector_create(blob_params)


st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 4])
with col1:
    st.header("Uploaded Warrant")
    uploaded_file = st.file_uploader("Upload your warrant", type=["pdf"])
    if uploaded_file is not None:
        try:
            with open(uploaded_file.name, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                page = pdf_reader.pages[0]
                st.image(page._get_page_object().get_contents(), width=540)
        except Exception as e:
            st.error("Error displaying PDF:", e)

with col2:
    st.title("Legal Advisor")

    # Analyze button
    if st.button("Analyze"):
        # Call your analysis functions here
        st.write("Analyzing the warrant...")

    # User input features (unchanged)

