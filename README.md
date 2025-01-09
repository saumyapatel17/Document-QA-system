
# Document Q&A System

The **Document Q&A System** is a Retrieval-Augmented Generation (RAG)-based application that allows users to upload documents and ask questions to gain insights. It integrates semantic search with language models to provide precise answers using only the uploaded content.

---

## Features

- **Multi-format Document Ingestion**: Supports `.txt`, `.pdf`, and `.docx` files.
- **Chunking and Vectorization**: Processes documents into meaningful chunks for efficient retrieval.
- **Semantic Search**: Retrieves the most relevant information based on the user's query.
- **Gradio Interface**: Interactive user interface for uploading files and querying.
- **Chat History**: Maintains a conversational flow for multiple questions.

---

## Prerequisites

- Python 3.10.11
- Poetry (for managing dependencies)
- 
---

## Usage

1. Activate the Poetry virtual environment:
   ```bash
   poetry shell
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Open the Gradio interface in your browser (link provided in the terminal).

4. **Upload Documents**: Drag and drop files or use the upload button.

5. **Ask Questions**: Type your query in the chatbox to retrieve answers based on the document content.

---

## File Structure

### Main Files

- **`main.py`**: Entry point of the application, handles the UI and user interactions.
- **`app/rag.py`**: Implements the RAG workflow, including semantic search and response generation.
- **`app/ingestion.py`**: Handles document ingestion and chunking for vectorization.
- **`app/llm.py`**: Handles the generation of final responses using the LLM model.
- **`app/prompts.py`**: Contains system and user prompt templates for language model interactions.
- **`app/setupDB.py`**: Manages the setup and initialization of the ChromaDB vector database.

### Utility Files

- **`app/preProcessing.py`**: Processes files (`.txt`, `.pdf`, `.docx`) and splits them into chunks.
- **`app/clients.py`**: Manages environment variables and provides configuration details.
- **`.env`**: Stores environment-specific configurations.
- **`requirements.txt`**: Lists required Python libraries.

---

## Example Queries

1. "What is the name of the company mentioned in the document?"
2. "What is the CEO's name?"
3. "Can you summarize their vacation policy?"
4. "What does the termination policy state?"

---

## Ways to Make the Solution More Accurate:

1. **Query Expansion**: Use methods to expand the search so the system can find relevant information even if the user asks the question in different ways.
2. **Improved Chunking**: Make sure the document is split into meaningful parts, so important context isn't lost when breaking down large documents.
3. **Enhanced Semantic Search**: Use more advanced search techniques (like transformers, e.g., BERT) to make sure the system finds the most accurate and relevant documents based on the user's question.
4. **Re-ranking**: After finding the top results, adjust the order based on how relevant they are to the question, so the best answers come first.
5. **Post-processing of Responses**: Improve the final answers by summarizing or fact-checking them, ensuring they are clear, correct, and make sense.
6. **Feedback Loop**: Set up a system where the model can learn from user feedback to get better at answering questions in the future.

---

## Making the Code More Modular, Scalable, and Production-Grade:

1. **Containerization**: Use Docker to package the app, ensuring it runs the same way on any system, which makes deployment simpler.
2. **Task Management**: Use a queue system (like Celery) to manage tasks that run in the background (like processing documents), so the app remains responsive to users.
3. **CI/CD Pipeline**: Set up automated systems for testing, building, and deploying code updates to make sure they are fast, reliable, and error-free.
4. **Testing and Monitoring**: Implement thorough testing to catch bugs and use monitoring tools (like Prometheus) to keep track of system performance and health in real-time.
5. **Model Versioning**: Use a system (like MLflow) to track different versions of models and experiments, ensuring reproducibility and easier updates.
6. **Caching**: Use caching (like Redis) to store frequently accessed documents and answers, speeding up the system and reducing response time.
