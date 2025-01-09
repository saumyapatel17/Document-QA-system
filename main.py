import os
import gradio as gr
import shutil
import warnings
from app.rag import RAGProcessor
from app.ingestion import DocumentIngestor
from app.setupDB import VectorDBSetup
import app.clients as client
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

class DocumentQASystem:
    """
    A class to encapsulate the Document Q&A system, handling file uploads,
    document ingestion, and responding to user queries.
    """

    def __init__(self):
        self.client_manager = client.ClientManager()
        self.vector_db_instance = VectorDBSetup(self.client_manager)
        self.document_ingestor_instance = DocumentIngestor()
        self.rag_processor_instance = RAGProcessor(self.client_manager)
        self.folder = self.client_manager.get_folder()
        self.ensure_upload_folder()

    def ensure_upload_folder(self):
        """
        Ensures that the upload folder exists.
        """
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    def upload_file(self, files):
        """
        Handles file uploads and ingestion into the vector database.
        Args:
            files (list): List of files to upload and process.
        Returns:
            list: List of file paths of the uploaded files.
        """
        collection = self.vector_db_instance.initialize_vectorDB()
        file_paths = []

        for file in files:
            file_path = os.path.join(self.folder, os.path.basename(file))
            shutil.copy(file, file_path)
            file_paths.append(file_path)
            self.document_ingestor_instance.ingest_documents(collection, file_path)

        return file_paths

    def respond(self, message, chat_history):
        """
        Handles user queries by performing RAG operations and updating chat history.
        Args:
            message (str): The user's query message.
            chat_history (list): The chat history with previous messages and responses.
        Returns:
            tuple: Updated chat history.
        """
        bot_message = self.rag_processor_instance.rag_query(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    def create_ui(self):
        """
        Creates and configures the Gradio interface.
        """
        with gr.Blocks() as demo:
            gr.Markdown("# Document Q&A System\nWelcome to the Document Q&A System! Upload your documents and ask questions to get insights and summaries.")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Upload Your Files")
                    upload_button = gr.UploadButton("Click to Upload Files", file_count="multiple")
                    file_output = gr.File()
                    upload_button.upload(self.upload_file, upload_button, file_output)
                
                with gr.Column():
                    gr.Markdown("### Chat with Your Documents")
                    chatbot = gr.Chatbot()
                    msg = gr.Textbox(label="Ask a question about your documents")
                    clear = gr.ClearButton([msg, chatbot])

                    msg.submit(self.respond, [msg, chatbot], [msg, chatbot])

            gr.Markdown("### Sample Questions to Ask:")
            
            with gr.Row():
                sample_questions = [
                    "What is the name of the company?",
                    "what is the name of CEO Zania?",
                    "What is their vacation policy?",
                    "What is the termination policy?"
                ]
                for question in sample_questions:
                    button = gr.Button(question)
                    button.click(lambda q=question: self.respond(q, []), inputs=[], outputs=[msg, chatbot])
        
        return demo

if __name__ == "__main__":
    # Suppress all user warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    
    system = DocumentQASystem()
    demo = system.create_ui()
    demo.launch()
