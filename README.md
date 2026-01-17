# 🛍️ E-Commerce Chatbot

An intelligent chatbot designed for e-commerce platforms, capable of answering FAQs and querying product databases using natural language. Built with Streamlit, Semantic Router, and Groq (LLM).

## ✨ Features

-   **Semantic Routing**: Intelligently routes user queries to either the FAQ knowledge base or the SQL product database.
-   **FAQ Engine**: Retrieval-Augmented Generation (RAG) using ChromaDB to answer general questions (return policy, payment methods, etc.).
-   **Product Search (Text-to-SQL)**: Converts natural language questions (e.g., "Show me top rated Nike shoes") into SQL queries to fetch real-time product data.
-   **Interactive UI**:
    -   Polished **Dark Theme**.
    -   **HTML Product Cards** with images and clickable "View" buttons.
    -   Smart handling of unanswerable queries.

## 🛠️ Tech Stack

-   **Frontend**: Streamlit
-   **Routing**: Semantic Router (HuggingFace Embeddings)
-   **LLM**: Groq (Llama3/Mixtral)
-   **Vector Store**: ChromaDB
-   **Database**: SQLite

## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/RudyMontoo/ECommerce_Chatbot.git
    cd ECommerce_Chatbot
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure you have `streamlit`, `pandas`, `groq`, `semantic-router`, `chromadb`, `python-dotenv` installed)*

3.  **Configure Environment:**
    Create a `.env` file in the `app/` directory:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    GROQ_MODEL=llama3-8b-8192
    ```

## 🏃‍♂️ Usage

Run the Streamlit application:

```bash
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`.

## 📂 Project Structure

-   `app/main.py`: Entry point of the Streamlit app.
-   `app/router.py`: Handles semantic routing of queries.
-   `app/faq.py`: Manages FAQ ingestion and RAG logic.
-   `app/sql.py`: Handles Natural Language to SQL generation and formatting.
-   `app/resources/faq.csv`: Source data for FAQs.
-   `db.sqlite`: SQLite database containing product inventory.

## 📷 Screenshots

*(Add screenshots here)*
