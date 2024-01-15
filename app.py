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

    # OpenAI API key input
    api_key_set = st.session_state.get("api_key_set", False)
    if not api_key_set:
        api_key = st.text_input("Enter your OpenAI API key", type="password")
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            st.session_state.api_key_set = True  # Mark as set
            st.success("API key saved successfully")
    else:
        st.info("OpenAI API key set")

    # Analyze button
    if st.button("Analyze"):
        try:
            # Load the uploaded PDF using loader
            loader = UnstructuredFileLoader(uploaded_file.name)
            documents = loader.load()

            # Create embeddings and query the AI model
            embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
            doc_search = Chroma.from_documents(documents, embeddings)
            chain = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type='stuff', vectorstore=doc_search)
            query = "Act like a very precise and intelligent legal professional and attorney, and..."  # Your query here
            output = chain.run(query)

            st.write(output)  # Display the output
        except Exception as e:
            st.error("Error analyzing the warrant:", e)

    # User input features (unchanged)

