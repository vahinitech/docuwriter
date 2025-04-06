import unittest
from utils import (
    split_text_into_sections,
    analyze_text,
    generate_conceptual_cornell_notes,
    extract_prescription_data,
    extract_receipt_data,
)
import spacy
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from spellchecker import SpellChecker

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up resources that will be used for every test."""
        self.nlp = spacy.load("en_core_web_sm")
        self.spell = SpellChecker()
        self.sentiment_pipeline = None  #  Set to None for testing
        self.classification_pipeline = None  # Set to None for testing

    def test_split_text_into_sections(self):
        text = "Section 1\n====\nThis is section 1 content.\n\nParagraph 1\n\nParagraph 2\nSection 2\n----\nThis is section 2."
        expected_result = [
            {"type": "heading", "title": "Section 1", "content": "This is section 1 content."},
            {"type": "paragraph", "content": "Paragraph 1"},
            {"type": "paragraph", "content": "Paragraph 2"},
            {"type": "heading", "title": "Section 2", "content": "This is section 2."},
        ]
        self.assertEqual(split_text_into_sections(text), expected_result)

    def test_analyze_text(self):
        text = "This is a sample text with no mistakes.  I think it is good."
        analysis = analyze_text(text, self.spell, self.sentiment_pipeline, self.classification_pipeline)
        self.assertEqual(analysis["spelling_mistakes"], [])
        self.assertEqual(analysis["intent"], "Speculative")
        self.assertEqual(analysis["confidence"], "Low")

        text_with_mistakes = "This is a sampel text with mistkaes."
        analysis = analyze_text(text_with_mistakes, self.spell, self.sentiment_pipeline, self.classification_pipeline)
        self.assertEqual(analysis["spelling_mistakes"], ["sampel", "mistkaes"])

    def test_generate_conceptual_cornell_notes(self):
        text = "Heading 1\n====\nThis is the main idea. Supporting detail."
        cornell_pages, summary, _ = generate_conceptual_cornell_notes(text, self.nlp, None, self.spell, self.sentiment_pipeline, self.classification_pipeline)  # Pass None for summarizer
        self.assertEqual(len(cornell_pages), 1)
        self.assertEqual(cornell_pages[0]["title"], "Heading 1")
        self.assertEqual(cornell_pages[0]["main_idea"], "This is the main idea.")
        self.assertEqual(cornell_pages[0]["supporting_details"], "Supporting detail.")

    def test_extract_prescription_data(self):
        text = "Patient Name: John Doe\n====\nMedicine 1: Paracetamol\nDosage: 500mg\nInstructions: Take twice daily.\n\nMedicine 2: Amoxicillin\nDosage: 250mg\nInstructions: Take three times a day for 7 days."
        expected_result = {
            "patient_name": "John Doe",
            "date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "medicines": [
                {"name": "Paracetamol", "dosage": "500mg", "instructions": "Take twice daily."},
                {"name": "Amoxicillin", "dosage": "250mg", "instructions": "Take three times a day for 7 days."},
            ],
        }
        result = extract_prescription_data(text, self.nlp)
        self.assertEqual(result["patient_name"], expected_result["patient_name"])
        self.assertEqual(result["date"], expected_result["date"])
        self.assertEqual(result["medicines"], expected_result["medicines"])

    def test_extract_receipt_data(self):
        text = "Order ID: 12345\nCustomer Name: Jane Smith\n====\nItem: Product A\nPrice: $25\n\nItem: Product B\nPrice: $10\n\nTotal:\nPrice: $35"
        expected_result = {
            "order_id": "12345",
            "customer_name": "Jane Smith",
            "items": [{"item": "Product A", "price": "$25"}, {"item": "Product B", "price": "$10"}],
            "total": "$35",
        }
        self.assertEqual(extract_receipt_data(text, self.nlp), expected_result)


if __name__ == "__main__":
    unittest.main()