import os
import docx
import PyPDF2
from app.config import CHUNK_SIZE

class DocumentProcessor:
    """
    A class to handle various document processing tasks, including reading
    and chunking different types of files (txt, pdf, docx).
    """

    def read_text_file(self, file_path: str) -> str:
        """
        Read content from a txt file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Text file not found: {file_path}") from e
        except IOError as e:
            raise IOError(f"Error reading text file: {file_path}") from e

    def read_pdf_file(self, file_path: str) -> str:
        """
        Read content from a PDF file.
        """
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except FileNotFoundError as e:
            raise FileNotFoundError(f"PDF file not found: {file_path}") from e
        except PyPDF2.errors.PdfReadError as e:
            raise PyPDF2.errors.PdfReadError(f"Error reading PDF file: {file_path}") from e

    def read_docx_file(self, file_path: str) -> str:
        """
        Read content from a docx file.
        """
        try:
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Docx file not found: {file_path}") from e
        except IOError as e:
            raise IOError(f"Error reading docx file: {file_path}") from e

    def read_document(self, file_path: str) -> str:
        """
        Reads document content based on the file extension.
        """
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        try:
            if file_extension == '.txt':
                return self.read_text_file(file_path)
            elif file_extension == '.pdf':
                return self.read_pdf_file(file_path)
            elif file_extension == '.docx':
                return self.read_docx_file(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except ValueError as e:
            raise ValueError(f"Error processing document: {e}")

    def chunking(self, text: str, chunk_size: int = CHUNK_SIZE) -> list:
        """
        Split text into chunks of a specified size.
        Args:
            text (str): The text to be split.
            chunk_size (int, optional): The maximum size of each chunk. Defaults to CHUNK_SIZE.
        Returns:
            list: A list of text chunks.
        """
        try:
            sentences = text.replace('\n', ' ').split('. ')
            chunks = []
            current_chunk = []
            current_size = 0

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                if not sentence.endswith('.'):
                    sentence += '.'

                sentence_size = len(sentence)
                if current_size + sentence_size > chunk_size and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_size = sentence_size
                else:
                    current_chunk.append(sentence)
                    current_size += sentence_size

            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks
        except Exception as e:
            raise RuntimeError(f"Error during text chunking: {e}")
