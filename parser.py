import config
import logging
import os
from docx import Document
from pdfminer.high_level import extract_text as extract_pdf_text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResumeParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
        self.found_keywords = []

    def parse(self):
        """
        Parses the file (PDF or DOCX) and extracts keywords defined in config.py.
        """
        try:
            logging.info(f"Parsing resume: {self.file_path}")

            if not os.path.exists(self.file_path):
                logging.error(f"File not found: {self.file_path}")
                return []

            file_ext = os.path.splitext(self.file_path)[1].lower()

            if file_ext == '.pdf':
                self.text = extract_pdf_text(self.file_path)
            elif file_ext == '.docx':
                self.text = self._extract_docx_text(self.file_path)
            else:
                logging.error(f"Unsupported file format: {file_ext}")
                return []

            self._extract_keywords()
            logging.info(f"Found keywords: {self.found_keywords}")
            return self.found_keywords
        except Exception as e:
            logging.error(f"Error parsing resume: {e}")
            return []

    def _extract_docx_text(self, docx_path):
        """
        Extracts text from a DOCX file using python-docx.
        """
        try:
            doc = Document(docx_path)
            full_text = []
            for paragraph in doc.paragraphs:
                full_text.append(paragraph.text)
            return '\n'.join(full_text)
        except Exception as e:
            logging.error(f"Error reading DOCX file: {e}")
            return ""

    def _extract_keywords(self):
        """
        Checks for presence of target keywords in the resume text.
        """
        if not self.text:
            return

        # Normalize text: remove extra whitespace and convert to lowercase
        text_lower = " ".join(self.text.split()).lower()

        for keyword in config.TARGET_KEYWORDS:
            # Escape special characters for regex if necessary, but simple check is okay for now
            # using straight string check for simplicity
            if keyword.lower() in text_lower:
                self.found_keywords.append(keyword)

    def generate_boolean_string(self):
        """
        Generates a basic boolean string from found keywords.
        Example: ("Keyword1" OR "Keyword2")
        """
        if not self.found_keywords:
            return ""

        quoted_keywords = [f'"{k}"' for k in self.found_keywords]
        return f"({' OR '.join(quoted_keywords)})"

if __name__ == "__main__":
    # Test execution
    parser = ResumeParser("Resume.docx")
    keywords = parser.parse()
    print("-" * 20)
    print(f"Keywords Found: {keywords}")
    print(f"Boolean Logic: {parser.generate_boolean_string()}")
    print("-" * 20)
