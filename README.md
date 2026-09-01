````markdown
# 🤖 AI Customer Service Chatbot

An AI-powered customer service chatbot that uses **Large Language Models (LLMs), Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG), and semantic search** to provide accurate and context-aware answers to customer queries.

The chatbot retrieves relevant information from a knowledge base and uses **Google Gemini** to generate natural-language responses.

---

## 📌 Project Overview

Customer service teams often need to answer repetitive questions related to courses, internships, services, tools, payments, and other frequently asked topics.

This project provides an AI-based solution where users can ask questions in natural language and receive helpful answers based on the information available in the chatbot's knowledge base.

The system uses **RAG (Retrieval-Augmented Generation)** so that responses are grounded in the available dataset instead of relying only on the language model's general knowledge.

---

## ✨ Features

- 🤖 AI-powered customer service chatbot
- 💬 Natural-language question answering
- 🔎 Semantic search using vector embeddings
- 📚 Knowledge-base based responses
- 🧠 Google Gemini LLM integration
- ⚡ Fast and interactive Streamlit interface
- 🛡️ Reduces hallucinated responses
- 📖 Displays source information used for answers
- 🔄 Ability to create/update the knowledge base
- 🧹 Clear chat functionality
- ❓ Handles questions outside the available knowledge base safely

---

## 🏗️ System Architecture

```text
                User
                  │
                  ▼
        ┌──────────────────┐
        │ Streamlit Web UI │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ User's Question  │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Semantic Search  │
        │     FAISS        │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Relevant Context │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Google Gemini    │
        │      LLM         │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Generated Answer │
        └────────┬─────────┘
                 │
                 ▼
                User
````

---

## 🧠 How the Chatbot Works

The chatbot follows a **Retrieval-Augmented Generation (RAG)** approach.

### Step 1 — User Question

The user enters a question through the Streamlit interface.

Example:

```text
Do you provide internships?
```

### Step 2 — Convert Knowledge into Embeddings

The dataset contains customer-service questions and answers.

The questions are converted into numerical vector representations using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

These embeddings capture the semantic meaning of the text.

### Step 3 — Semantic Search

The generated question embedding is compared with the stored embeddings using **FAISS**.

FAISS retrieves the most relevant pieces of information from the knowledge base.

### Step 4 — Context Retrieval

The most relevant documents are passed as context to the language model.

### Step 5 — Gemini Generates the Answer

Google Gemini receives:

* The user's question
* The retrieved context
* Instructions to answer only using the provided information

The model then generates a natural-language response.

### Step 6 — Display Response

The final answer is displayed in the Streamlit chatbot interface.

The application can also show the source information used to generate the answer.

---

## 🔍 What is RAG?

**RAG stands for Retrieval-Augmented Generation.**

Instead of asking the LLM to answer a question only from its existing knowledge, the system first retrieves relevant information from a knowledge base.

```text
Question
   ↓
Retrieve relevant information
   ↓
Add information as context
   ↓
Send context + question to LLM
   ↓
Generate grounded answer
```

This approach helps reduce incorrect or made-up answers.

---

## 🛠️ Technologies Used

| Technology              | Purpose                         |
| ----------------------- | ------------------------------- |
| Python                  | Core programming language       |
| Streamlit               | Web interface                   |
| Google Gemini           | Large Language Model            |
| LangChain               | LLM application framework       |
| Hugging Face Embeddings | Text embeddings                 |
| Sentence Transformers   | Semantic representation         |
| FAISS                   | Vector similarity search        |
| CSV                     | Knowledge-base dataset          |
| python-dotenv           | Environment variable management |

---

## 📂 Project Structure

```text
customer_service_chatbot_LLM/
│
├── dataset/
│   └── dataset.csv
│
├── faiss_index/
│   └── Generated FAISS vector database
│
├── src/
│   ├── main.py
│   └── langchain_helper.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The chatbot uses a CSV-based knowledge base.

The dataset contains customer-service questions and their corresponding answers.

Example structure:

```text
prompt,response
Do you provide internships?,Yes, internship opportunities are available...
What courses do you offer?,We provide various technical courses...
```

The dataset can be modified or expanded to improve the chatbot's knowledge.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/build-aayan1219/customer_service_chatbot_LLM.git
```

```bash
cd customer_service_chatbot_LLM
```

> Replace the repository URL above with your actual GitHub repository URL if it is different.

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

### 3. Activate the Virtual Environment

For Windows:

```bash
.\venv\Scripts\Activate.ps1
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration

The project uses the **Google Gemini API**.

Create a `.env` file in the project root directory:

```text
GOOGLE_API_KEY=your_google_gemini_api_key
```

Replace:

```text
your_google_gemini_api_key
```

with your actual Gemini API key.

### ⚠️ Security

Never upload your `.env` file or API key to GitHub.

The project includes `.gitignore` to prevent sensitive files and generated files from being committed.

---

## ▶️ Running the Application

Activate the virtual environment and run:

```bash
streamlit run src/main.py
```

The Streamlit application will open in your browser.

---

## 💬 Example Questions

You can ask questions such as:

```text
Do you provide internships?
```

```text
Do you offer EMI?
```

```text
Can I use Power BI on Mac?
```

```text
Tableau vs Power BI?
```

The chatbot searches the knowledge base and generates an answer using the retrieved information.

---

## 📚 Source Information

The application provides an option to view the source information used to generate an answer.

This helps users understand where the chatbot obtained the information from and improves transparency.

---

## 🛡️ Grounded Responses

The chatbot is instructed to answer questions using only the information retrieved from the knowledge base.

If the required information is not available, the chatbot responds:

```text
I don't know based on the available information.
```

This prevents the chatbot from unnecessarily generating unsupported information.

---

## 🔄 Knowledge Base Update

The application provides an option to create or update the knowledge base.

When the dataset is changed, the FAISS vector database can be regenerated so that the chatbot can search the updated information.

---

## 🎯 Benefits

* Reduces repetitive customer-support work
* Provides quick responses
* Available 24/7
* Uses natural-language interaction
* Makes information easier to access
* Can be customized for different organizations
* Can be expanded with additional knowledge
* Uses RAG to improve response grounding

---

## 🧪 Testing

The chatbot can be tested using:

### Relevant Questions

Questions whose answers exist in the dataset.

### Similar Questions

Questions phrased differently but having the same meaning.

### Unknown Questions

Questions whose information is not available in the knowledge base.

The expected behavior for unknown information is:

```text
I don't know based on the available information.
```

---

## 🔐 Security Considerations

* API keys are stored using environment variables.
* `.env` is excluded from GitHub using `.gitignore`.
* Sensitive credentials should never be hardcoded into the source code.
* Generated vector database files can be kept outside version control when appropriate.

---

## 🚀 Future Improvements

Possible future enhancements include:

* 🔐 User authentication
* 💾 Chat history storage
* 🌐 Deployment on cloud platforms
* 🎤 Voice-based interaction
* 🌍 Multi-language support
* 📈 Customer analytics dashboard
* 🗄️ Database integration
* 🔗 Integration with business websites
* 📱 Mobile application
* 🤝 Human-agent handoff
* 📊 Admin dashboard for knowledge-base management

---

## 📌 Project Status

**Status:** Completed / Working Prototype

The chatbot successfully provides AI-powered customer service responses using a Streamlit interface, FAISS vector search, Hugging Face embeddings, and Google Gemini.

---

## 📄 License

This project is developed for educational and internship purposes.

---

## 🙏 Acknowledgements

* Google Gemini
* LangChain
* Hugging Face
* FAISS
* Streamlit
* Python Community

---

## 👨‍💻 Author

**Aayan Shaikh**

GitHub:

[https://github.com/build-aayan1219](https://github.com/build-aayan1219)

```
```
