# RAG-Based PDF Search System

This project is an AI-powered document search system that enables users to upload PDF files, extract text, chunk documents, generate embeddings using a pre-trained Sentence Transformer, and perform similarity searches using Pinecone. The system is implemented using Python, Streamlit, and Pinecone vector database for storing and querying document embeddings.

## Project Structure

```bash
.
├── Dockerfile               # Docker configuration for containerizing the application
├── README.md                # Project documentation
├── ak-hk.pem                # Private key for server connection (Ensure this is kept secure)
├── backend.py               # Backend logic for processing documents and performing search
├── main.py                  # Main application file (runs the Streamlit app)
├── requirements.txt         # Python dependencies
```

## Prerequisites

- **Python 3.8+**
- **Docker** (Optional, for containerized deployment)
- **Pinecone API Key** (for vector search database)
- **Streamlit** (for the frontend application)
- **AWS EC2 Instance** (for cloud deployment)

### Install Dependencies

To install the required Python packages, run:

```bash
pip install -r requirements.txt
```

### Requirements.txt

The `requirements.txt` file includes the following necessary dependencies:

- `pinecone-client`
- `langchain`
- `streamlit`
- `torch`
- `sentence-transformers`

## How to Run the Application

### 1. Local Development

To run the app locally, follow these steps:

1. Clone the repository:

```bash
git clone <repository_url>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the backend logic to extract text, chunk documents, and store embeddings in Pinecone:

```bash
python backend.py
```

4. Run the main application with Streamlit:

```bash
streamlit run main.py
```

### 2. Docker Deployment

You can deploy this application using Docker. The `Dockerfile` is already provided for containerizing the application.

1. Build the Docker image:

```bash
docker build -t ai-document-search .
```

2. Run the Docker container:

```bash
docker run -p 8501:8501 ai-document-search
```

Now, the application should be accessible at `http://localhost:8501`.

### 3. AWS EC2 Deployment using Docker

You can deploy this system on an AWS EC2 instance using Docker. The following steps outline how to set up your EC2 instance and deploy the Dockerized application.

#### Step 1: Set Up an EC2 Instance

1. **Launch an EC2 Instance**:
   - Go to the AWS EC2 dashboard.
   - Launch a new instance (choose **Ubuntu 20.04 LTS** or a similar Linux-based AMI).
   - Select an appropriate instance type (e.g., t2.micro for testing).
   - Configure security group rules to allow access to port 8501 (for Streamlit) and port 22 (for SSH).
   - Download the **private key** (`.pem` file) when setting up the instance, as it will be needed for SSH access.

2. **Connect to the EC2 Instance**:
   - Open your terminal and use the following command to SSH into your EC2 instance:
   
   ```bash
   ssh -i /path/to/your-key.pem ubuntu@<your-ec2-public-ip>
   ```

#### Step 2: Install Docker on EC2

1. **Update the package repository**:

   ```bash
   sudo apt-get update
   ```

2. **Install Docker**:

   ```bash
   sudo apt-get install docker.io
   ```

3. **Start and enable Docker**:

   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. **Check Docker installation**:

   ```bash
   docker --version
   ```

#### Step 3: Set Up the Application on EC2

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Build the Docker image**:

   ```bash
   sudo docker build -t ai-document-search .
   ```

3. **Run the Docker container**:

   ```bash
   sudo docker run -p 8501:8501 ai-document-search
   ```

4. **Access the Application**:

   - Go to your browser and open the URL: `http://<your-ec2-public-ip>:8501`.
   - You should now be able to access the application through the EC2 public IP.

#### Step 4: Configure Pinecone on EC2

Make sure you have your **Pinecone API Key** ready and follow these steps to configure it:

1. Open the `backend.py` file and replace the placeholder `api_key` with your actual Pinecone API key.

2. Ensure that your Pinecone index is created and that the index name in the code (`langchain-chatbot`) matches the one in Pinecone.

3. Make sure the EC2 instance can access Pinecone by verifying the networking configuration.

#### Step 5: (Optional) Run the Docker Container in Detached Mode

If you want the Docker container to run in the background, use the `-d` flag:

```bash
sudo docker run -d -p 8501:8501 ai-document-search
```

This will allow the application to continue running even after you disconnect from the SSH session.

## How it Works

### 1. Upload Documents

- Users can upload PDF files through the frontend interface (Streamlit).

### 2. Text Extraction

- Uploaded PDF files are processed, and the text is extracted for further use.

### 3. Chunking Documents

- The text is split into manageable chunks (500 characters with a 20-character overlap) to ensure contextual understanding.

### 4. Embedding Generation

- Document chunks are converted into vector embeddings using **SentenceTransformer**.

### 5. Pinecone Vector Store

- Embeddings are inserted into the Pinecone vector store for later querying.

### 6. Similarity Search

- Users can input a query, and the system will retrieve the most similar document chunks based on vector similarity.

### Example Search

Users can input a query like:

```bash
whats the future of AI
```

The system will return the most relevant document chunks based on the embeddings stored in Pinecone.

## Key Components

### Backend (`backend.py`)

- Contains the logic for:
  - Uploading and processing PDF files
  - Chunking the documents into smaller pieces
  - Generating and upserting embeddings into Pinecone

### Frontend (`main.py`)

- A Streamlit-based frontend that allows users to interact with the application by:
  - Uploading documents
  - Searching for relevant information using queries

## Pinecone Setup

To use Pinecone for vector search:

1. Sign up for Pinecone at [pinecone.io](https://pinecone.io).
2. Create an index and replace the `api_key` in the `backend.py` file with your actual Pinecone API key.
3. Ensure the index name matches the one in the code (`langchain-chatbot`).

## Contact

For any questions or issues, feel free to raise an issue on this repository or contact the project maintainer.

---

This `README.md` now includes detailed instructions for deploying the RAG-based PDF search system on an AWS EC2 instance using Docker.
