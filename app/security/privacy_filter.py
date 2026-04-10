import re
from typing import Dict, List, Tuple

class PrivacyFilter:
    """
    OmniAgent Privacy Filter
    Responsible for scanning and masking sensitive information in user inputs and AI outputs.
    """
    
    def __init__(self):
        # Define common sensitive data patterns
        self.patterns = {
            "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "phone": r"(\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
            "password": r"(?i)(password|passwd|pwd|secret)\s*[:=]\s*([^\s]+)",
            "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        }
        self.mask_token = "[SENSITIVE_DATA]"

    def filter_text(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Scans text for sensitive information and replaces it with mask tokens.
        Returns the filtered text and a list of detected entities.
        """
        filtered_text = text
        detected_entities = []

        for label, pattern in self.patterns.items():
            matches = re.finditer(pattern, filtered_text)
            for match in matches:
                value = match.group()
                start, end = match.span()
                
                # Store the original value and its position for potential decryption/recovery
                detected_entities.append({
                    "label": label,
                    "value": value,
                    "start": start,
                    "end": end
                })
                
        # Replace in reverse order to maintain index integrity
        for entity in sorted(detected_entities, key=lambda x: x['start'], reverse=True):
            start, end = entity['start'], entity['end']
            filtered_text = filtered_text[:start] + self.mask_token + filtered_text[end:]

        return filtered_text, detected_entities

    def unmask_text(self, text: str, entities: List[Dict]) -> str:
        """
        Restores masked text using the provided entities list.
        """
        unmasked_text = text
        # This is a simplified version; in production, we'd use unique IDs for each mask
        for entity in entities:
            unmasked_text = unmasked_text.replace(self.mask_token, entity['value'], 1)
        return unmasked_text

# Example usage for testing
if __name__ == "__main__":
    pf = PrivacyFilter()
    test_text = "My email is test@example.com and my card is 1234-5678-9012-3456. Password: secret123"
    filtered, entities = pf.filter_text(test_text)
    print(f"Original: {test_text}")
    print(f"Filtered: {filtered}")
    print(f"Entities: {entities}")
