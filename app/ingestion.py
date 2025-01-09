import os
from app.config import BATCH_SIZE
from app.preProcessing import DocumentProcessor

class DocumentIngestor:
    """
    A class to handle document ingestion, including reading, chunking, and inserting documents 
    into a ChromaDB collection.
    """

    def __init__(self):
        self.document_processor_instance = DocumentProcessor()

    def process_document(self, file_path: str):
        """
        Process a single document and prepare it for ChromaDB.
        Args:
            file_path (str): Path to the document to be processed.
        Returns:
            tuple: A tuple containing:
                - ids (list): A list of document chunk ids.
                - chunks (list): A list of document chunks.
                - metadatas (list): A list of metadata dictionaries.
        """
        try:
            content = self.document_processor_instance.read_document(file_path)
            chunks = self.document_processor_instance.chunking(content)
            file_name = os.path.basename(file_path)
            metadatas = [{"source": file_name, "chunk": i} 
                         for i in range(len(chunks))]
            ids = [f"{file_name}_chunk_{i}" 
                   for i in range(len(chunks))]
            return ids, chunks, metadatas
        
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Document file not found: {file_path}") from e
        except Exception as e:
            raise Exception(f"Error processing document: {e}") from e

    def insert_documents_into_collection(self, collection, ids, texts, metadatas):
        """
        Inserts documents into the ChromaDB collection in batches.
        Args:
            collection: The ChromaDB collection to insert documents into.
            ids (list): A list of document chunk ids.
            texts (list): A list of document chunks.
            metadatas (list): A list of metadata dictionaries.
        """
        if not texts:
            return

        try:
            for i in range(0, len(texts), BATCH_SIZE):
                end_idx = min(i + BATCH_SIZE, len(texts))
                collection.add(
                    documents=texts[i:end_idx],
                    metadatas=metadatas[i:end_idx],
                    ids=ids[i:end_idx]
                )
        except Exception as e:
            raise Exception(f"Error inserting documents into collection: {e}") from e

    def ingest_documents(self, collection, file_path: str):
        """
        Processes and ingests all documents from a specified folder into a ChromaDB collection.
        """
        try:
            ids, texts, metadatas = self.process_document(file_path)
            self.insert_documents_into_collection(collection, ids, texts, metadatas)
        except Exception as e:
            raise Exception(f"Error ingesting documents: {e}") from e
