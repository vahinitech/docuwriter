import re
import spacy
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from spellchecker import SpellChecker
import torch  # Import torch
import datetime

nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

# Load Hugging Face models and tokenizers (Consider loading these outside the function for efficiency)
try:
    sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(
        sentiment_model_name
    )
    sentiment_pipeline = pipeline(
        "sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer
    )

    classification_model_name = "distilbert-base-uncased"  # You can change this
    classification_tokenizer = AutoTokenizer.from_pretrained(classification_model_name)
    classification_model = AutoModelForSequenceClassification.from_pretrained(
        classification_model_name
    )
    classification_pipeline = pipeline(
        "text-classification", model=classification_model, tokenizer=classification_tokenizer
    )
except Exception as e:
    print(f"Error loading Hugging Face models: {e}")
    sentiment_pipeline = None
    classification_pipeline = None


def split_text_into_sections(text):
    """Splits text into sections based on headings and paragraphs."""
    sections = []
    heading_sections = re.split(r'(\w+\n[=-]{3,})', text)
    i = 0
    while i < len(heading_sections):
        if i + 1 < len(heading_sections) and re.match(
            r'\w+\n[=-]{3,}', heading_sections[i]
        ):
            heading = heading_sections[i].strip()
            content = heading_sections[i + 1].strip()
            sections.append({"type": "heading", "title": heading, "content": content})
            i += 2
        else:
            paragraph_sections = re.split(r'\n\s*\n', heading_sections[i])
            for p in paragraph_sections:
                if p.strip():
                    sections.append({"type": "paragraph", "content": p.strip()})
            i += 1
    return sections


def analyze_text(text):
    """
    Analyzes the text for spelling mistakes, intent, and confidence using Hugging Face.
    """
    analysis = {}
    # 1. Spell Check
    words = text.split()
    misspelled = spell.unknown(words)
    analysis["spelling_mistakes"] = list(misspelled)

    if sentiment_pipeline:
        # 2. Sentiment Analysis
        sentiment_result = sentiment_pipeline(text)
        analysis["sentiment"] = sentiment_result[0]["label"]
        analysis["sentiment_confidence"] = sentiment_result[0]["score"]
    else:
        analysis["sentiment"] = "N/A"
        analysis["sentiment_confidence"] = "N/A"

    if classification_pipeline:
        # 3. Text Classification
        classification_result = classification_pipeline(text)
        analysis["classification"] = classification_result[0]["label"]
        analysis["classification_confidence"] = classification_result[0]["score"]
    else:
        analysis["classification"] = "N/A"
        analysis["classification_confidence"] = "N/A"

    # 4.  Basic intent and confidence.
    if "I think" in text or "I believe" in text:
        intent = "Speculative"
        confidence = "Low"
    elif "It is clear that" in text or "The evidence shows" in text:
        intent = "Assertive"
        confidence = "High"
    else:
        intent = "Informative"
        confidence = "Medium"
    analysis["intent"] = intent
    analysis["confidence"] = confidence

    return analysis


def generate_conceptual_cornell_notes(text):
    """Generates Cornell Notes."""
    sections = split_text_into_sections(text)
    cornell_pages = []
    for section in sections:
        if section["type"] == "heading":
            title = section["title"]
            content = section["content"]

            # Process content with spaCy
            doc = nlp(content)
            sentences = [sent.text for sent in doc.sents]  # Get sentences

            # Summarize the content using Hugging Face
            summary_text = summarizer(content, max_length=150, min_length=30)[0][
                "summary_text"
            ]

            #  Simplest approach:  First sentence of summary
            main_idea = (
                nlp(summary_text).sents[0].text
                if nlp(summary_text).sents
                else sentences[0]
                if sentences
                else "N/A"
            )

            # Supporting details: all sentences that are not the main idea.
            supporting_details = (
                " ".join([sent for sent in sentences if sent != main_idea])
                if sentences
                else "N/A"
            )

            cues = f"What is the main idea of '{title}'?"
            page_analysis = analyze_text(content)
            cornell_pages.append(
                {
                    "page_type": "heading",
                    "title": title,
                    "main_idea": main_idea,
                    "supporting_details": supporting_details,
                    "cues": cues,
                    "analysis": page_analysis,  # Add the analysis here
                }
            )
        elif section["type"] == "paragraph":
            content = section["content"]
            # Process content with spaCy
            doc = nlp(content)
            sentences = [sent.text for sent in doc.sents]

            # Summarize the content using Hugging Face
            summary_text = summarizer(content, max_length=100, min_length=20)[0][
                "summary_text"
            ]

            #  Simplest approach:  First sentence of summary
            main_idea = (
                nlp(summary_text).sents[0].text
                if nlp(summary_text).sents
                else sentences[0]
                if sentences
                else "N/A"
            )

            # Supporting details: all sentences that are not the main idea.
            supporting_details = (
                " ".join([sent for sent in sentences if sent != main_idea])
                if sentences
                else "N/A"
            )

            cues = "What are the key points?"
            page_analysis = analyze_text(content)
            cornell_pages.append(
                {
                    "page_type": "paragraph",
                    "title": "Paragraph",
                    "main_idea": main_idea,
                    "supporting_details": supporting_details,
                    "cues": cues,
                    "analysis": page_analysis,  # Add analysis
                }
            )

    # Generate overall summary
    all_text = " ".join([s["content"] for s in sections])
    summary = summarizer(all_text, max_length=200, min_length=50)[0]["summary_text"]
    analysis = analyze_text(all_text)  # Analyze the entire text for the summary section
    return cornell_pages, summary, analysis


def extract_prescription_data(text):
    """
    Extracts data from prescription text using regex and spaCy.
    """
    doc = nlp(text)
    data = {}

    # Patient name extraction (improved with more variations)
    patient_name_match = re.search(
        r"(Patient Name:\s*([A-Za-z\s]+))|(Name:\s*([A-Za-z\s]+))", text
    )
    if patient_name_match:
        data["patient_name"] = (
            patient_name_match.group(2) or patient_name_match.group(4)
        )
    else:
        data["patient_name"] = "N/A"

    # Date extraction
    date_match = re.search(r"(Date:\s*(\d{4}-\d{2}-\d{2}))", text)
    if date_match:
        data["date"] = date_match.group(2)
    else:
        data["date"] = datetime.datetime.now().strftime("%Y-%m-%d")

    # Medicine extraction
    medicines = []
    medicine_matches = re.findall(
        r"(Medicine\s*\d+:\s*([A-Za-z\s]+)\nDosage:\s*([A-Za-z0-9\s]+)\nInstructions:\s*([A-Za-z0-9\s,.]+))",
        text,
    )
    for match in medicine_matches:
        medicines.append(
            {
                "name": match[1],
                "dosage": match[2],
                "instructions": match[3],
            }
        )
    data["medicines"] = medicines
    if not medicines:
        data["medicines"] = [{"name": "N/A", "dosage": "N/A", "instructions": "N/A"}]

    return data


def extract_receipt_data(text):
    """
    Extracts data from receipt text using regex and spaCy.
    """
    doc = nlp(text)
    data = {}

    # Order ID
    order_id_match = re.search(r"(Order ID:\s*([A-Za-z0-9-]+))", text)
    if order_id_match:
        data["order_id"] = order_id_match.group(2)
    else:
        data["order_id"] = "N/A"

    # Customer name
    customer_name_match = re.search(r"(Customer Name:\s*([A-Za-z\s]+))", text)
    if customer_name_match:
        data["customer_name"] = customer_name_match.group(2)
    else:
        data["customer_name"] = "N/A"

    # Extract items and prices
    items = []
    item_matches = re.findall(r"Item:\s*([A-Za-z0-9\s]+)\nPrice:\s*([$\d\.]+)", text)
    for match in item_matches:
        items.append({"item": match[0], "price": match[1]})
    data["items"] = items

    # Extract total
    total_match = re.search(r"Total:\s*Price:\s*([$\d\.]+)", text)
    if total_match:
        data["total"] = total_match.group(1)
    else:
        data["total"] = "N/A"
    return data