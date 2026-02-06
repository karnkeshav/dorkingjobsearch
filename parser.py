from pdfminer.high_level import extract_text
import config
import logging
import docx  # Added for .docx support

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResumeParser:
    def __init__(self, file_path):
        self.file_path = file_path # Renamed from pdf_path for clarity
        self.text = ""
        self.found_keywords = []

    def parse(self):
        """
        Parses PDF or DOCX and extracts keywords defined in config.py.
        """
        try:
            logging.info(f"Parsing resume: {self.file_path}")
            
            # Check file extension to determine parsing method
            if self.file_path.lower().endswith('.docx'):
                self.text = self._extract_text_from_docx(self.file_path)
            else:
                self.text = extract_text(self.file_path)
            
            self._extract_keywords()
            logging.info(f"Found keywords: {self.found_keywords}")
            return self.found_keywords
        except Exception as e:
            logging.error(f"Error parsing resume: {e}")
            return []

    def _extract_text_from_docx(self, path):
        """
        Extracts text from a .docx file.
        """
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _extract_keywords(self):
        """
        Checks for presence of target keywords in the resume text.
        """
        if not self.text:
            return

        # Normalize text: remove extra whitespace and convert to lowercase
        text_lower = " ".join(self.text.split()).lower()

        for keyword in config.TARGET_KEYWORDS:
            if keyword.lower() in text_lower:
                self.found_keywords.append(keyword)

    def generate_boolean_string(self):
        """
        Generates a basic boolean string from found keywords.
        """
        if not self.found_keywords:
            return ""

        quoted_keywords = [f'"{k}"' for k in self.found_keywords]
        return f"({' OR '.join(quoted_keywords)})"

if __name__ == "__main__":
    # Test execution with docx
    parser = ResumeParser("resume.docx")
    keywords = parser.parse()
    print("-" * 20)
    print(f"Keywords Found: {keywords}")
    print(f"Boolean Logic: {parser.generate_boolean_string()}")
    print("-" * 20)
