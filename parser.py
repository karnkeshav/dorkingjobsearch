from pdfminer.high_level import extract_text
import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = ""
        self.found_keywords = []

    def parse(self):
        """
        Parses the PDF and extracts keywords defined in config.py.
        """
        try:
            logging.info(f"Parsing resume: {self.pdf_path}")
            self.text = extract_text(self.pdf_path)
            self._extract_keywords()
            logging.info(f"Found keywords: {self.found_keywords}")
            return self.found_keywords
        except Exception as e:
            logging.error(f"Error parsing resume: {e}")
            return []

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
    parser = ResumeParser("resume.pdf")
    keywords = parser.parse()
    print("-" * 20)
    print(f"Keywords Found: {keywords}")
    print(f"Boolean Logic: {parser.generate_boolean_string()}")
    print("-" * 20)
