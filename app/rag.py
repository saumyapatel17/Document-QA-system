import json
import os
from app.setupDB import VectorDBSetup
from app.llm import LLMProcessor
from app.config import N_CHUNKS, CONFIDENCE_THRESHOLD

class RAGProcessor:
    """
    A class to handle Retrieval-Augmented Generation (RAG) operations, including 
    performing semantic searches, processing context, and generating responses.
    """

    def __init__(self, client_manager):
        self.json_file_path = client_manager.get_json_file_path()
        self.vector_db_instance = VectorDBSetup(client_manager)
        self.llm_processor_instance = LLMProcessor(client_manager)

    @staticmethod
    def semantic_search(collection, query: str, n_results: int = 2) -> dict:
        """
        Perform semantic search on the collection.
        Args:
            collection: The ChromaDB collection to search.
            query (str): The query to search for in the collection.
            n_results (int, optional): The number of results to retrieve. Defaults to 2.
        Returns:
            dict: The search results containing documents and distances.
        """
        return collection.query(query_texts=[query], n_results=n_results)

    @staticmethod
    def get_context(results) -> str:
        """
        Get a combined context and formatted sources from search results.
        """
        return "\n\n".join(results['documents'][0])

    def save_qa_to_json(self, qa_data):
        """
        Save the Q&A data to a JSON file, appending to the history if the file exists.
        Args:
            qa_data (dict): The question and answer data to save.
        """
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as file:
                qa_history = json.load(file)
        else:
            qa_history = []

        qa_history.append(qa_data)

        with open(self.json_file_path, 'w') as file:
            json.dump(qa_history, file, indent=4)

    def rag_query(self, query: str, history) -> str:
        """
        Perform Retrieval-Augmented Generation (RAG) query: retrieve relevant chunks
        and generate an answer based on valid contexts.
        Args:
            query (str): The query to perform the RAG process.
            history: The history of previous queries or responses (unused here).
        Returns:
            str: The generated response or a message indicating data is unavailable.
        """
        try:
            # Initialize the vector database and perform a semantic search
            collection = self.vector_db_instance.initialize_vectorDB()
            results = self.semantic_search(collection, query, N_CHUNKS)

            # Filter valid contexts based on confidence threshold
            valid_contexts = [
                context for context, distance in zip(results['documents'][0], results['distances'][0])
                if distance >= CONFIDENCE_THRESHOLD
            ]

            # If no valid context remains, return "Data Not Available"
            if not valid_contexts:
                return "Data Not Available"

            # Generate context and response
            context = self.get_context({'documents': [valid_contexts], 'distances': [results['distances'][0]]})
            response = self.llm_processor_instance.generate_response(query, context)

            # Save the question and answer to JSON
            qa_data = {"question": query, "answer": response}
            self.save_qa_to_json(qa_data)

            return response

        except Exception as e:
            # Log the error and return a user-friendly error message
            print(f"Error during RAG query process: {e}")
            return "An error occurred while processing your query. Please try again later."
