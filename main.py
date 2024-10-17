import streamlit as st
from backend import initialize_pinecone, extract_text_from_pdf, split_docs, generate_embeddings, \
    store_embeddings_in_pinecone, search_similar_docs
from langchain.embeddings import SentenceTransformerEmbeddings
import time

# Initialize Streamlit App
st.set_page_config(page_title="ASK PDF", page_icon="📄", layout="centered")
st.title("📄 **ASK PDF: Your AI-Powered Document Search**")

# App description
st.markdown("""
Welcome to **ASK PDF**! Upload your PDF file (limit: **1000KB**) and ask any questions related to its content.
Our AI system will analyze and find the most relevant sections for you and provide real-time answers.
""", unsafe_allow_html=True)

# Step 1: Pinecone API Key Input (Hardcoded in backend)
index_name = "langchain-chatbot"
pinecone_api_key = "d79317b9-680b-4166-8bb4-4cb913892719"

# Initialize Pinecone if API key is provided
if pinecone_api_key:
    index = initialize_pinecone(pinecone_api_key, index_name)

    # Step 3: Upload PDF File
    st.markdown("### 📤 Upload your PDF file (max 1000KB):")
    uploaded_file = st.file_uploader("", type="pdf")

    if uploaded_file:
        file_size = uploaded_file.size / 1024  # Convert to KB
        if file_size > 1000:  # 1000 KB limit
            st.warning("⚠️ The file is too large. Please upload a file less than 1000KB.")
        else:
            # Show progress bar during file processing
            progress_bar = st.progress(0)
            with st.spinner('🔄 Processing your PDF...'):
                for i in range(100):  # Simulate progress
                    time.sleep(0.05)
                    progress_bar.progress(i + 1)

            # File successfully uploaded
            st.success("✅ **success!**")

            # Step 4: Extract text from PDF
            with st.spinner('🔍 Extracting text from PDF...'):
                documents = extract_text_from_pdf(uploaded_file)

            # Split the document into chunks
            with st.spinner('please wait.'):
                docs = split_docs(documents)

            # Generate embeddings
            with st.spinner('we are working..'):
                embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                doc_embeddings = generate_embeddings(docs)

            # Store embeddings in Pinecone
            with st.spinner('You are one step away....'):
                num_vectors = store_embeddings_in_pinecone(index, doc_embeddings, docs)

            st.success(f"🎉 **Successfully processed!**")

            # Step 5: Allow user to search for documents and ask queries
            st.markdown("### 🔍 **Ask a question about your PDF content**:")
            query = st.text_input("Type your query here")

            if query:
                # Real-time query processing
                with st.spinner('🤖 Generating your answer, please wait...'):
                    query_embedding = embeddings.embed_query(query)
                    results = search_similar_docs(index, query_embedding)

                # Display the answer along with relevant document segments
                st.markdown("### 💡 **Generated Answer and Relevant Document Segments**:")
                st.write(f"**Query**: {query}")

                # Display top document segments that are relevant to the query
                for idx, match in enumerate(results['matches']):
                    match_text = match.get('metadata', {}).get('text', 'No Text')
                    st.write(f"{match_text[:500]}...")  # Display first 500 characters

                st.success("✅ **Answer generated and relevant document segments retrieved!**")

                # Option for multiple queries after first one
                st.markdown("Feel free to ask another question based on the same PDF!")