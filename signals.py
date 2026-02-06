import config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SignalDetector:
    def __init__(self, keywords):
        self.keywords = keywords

    def generate_hiring_manager_search(self):
        """
        Generates LinkedIn boolean strings to find hiring managers.
        """
        queries = []
        # Use first few keywords to avoid generating too many strings
        target_keywords = self.keywords[:3] if self.keywords else ["FinOps"]

        for keyword in target_keywords:
             query = config.LINKEDIN_PATTERNS["hiring_manager"].format(keyword=keyword)
             queries.append(query)
        return queries

    def detect_signals(self):
        """
        Placeholder for detecting signals using compliant APIs.
        For now, it returns the generated boolean strings for manual use or PhantomBuster feeding.
        """
        logging.info("Generating Hiring Signal Queries...")
        queries = self.generate_hiring_manager_search()
        return queries

if __name__ == "__main__":
    detector = SignalDetector(["FinOps", "AI Governance"])
    signals = detector.detect_signals()
    print("-" * 20)
    print("Generated Signal Queries (for LinkedIn/PhantomBuster):")
    for s in signals:
        print(f"- {s}")
    print("-" * 20)
