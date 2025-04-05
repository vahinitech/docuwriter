from flask import Flask, render_template, request, url_for
import re
import spacy
from transformers import pipeline

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="distilbart-cnn-12-3")

def split_text_into_sections(text):
    \"\"\"Splits text into sections based on headings and paragraphs.\"\"\"
    sections = []
    heading_sections = re.split(r'(\w+\n[=-]{3,})', text)
    i = 0
    while i < len(heading_sections):
        if i + 1 < len(heading_sections) and re.match(r'\w+\n[=-]{3,}', heading_sections[i]):
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

def generate_conceptual_cornell_notes(text):
    \"\"\"Generates Cornell Notes using spaCy and Hugging Face summarization.\"\"\"
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
            summary_text = summarizer(content, max_length=150, min_length=30)[0]['summary_text']

            #  Simplest approach:  First sentence of summary
            main_idea = nlp(summary_text).sents[0].text if nlp(summary_text).sents else sentences[0] if sentences else "N/A"
            
            # Supporting details: all sentences that are not the main idea.
            supporting_details = " ".join([sent for sent in sentences if sent != main_idea]) if sentences else "N/A"

            cues = f"What is the main idea of '{title}'?"
            cornell_pages.append({
                "page_type": "heading",
                "title": title,
                "main_idea": main_idea,
                "supporting_details": supporting_details,
                "cues": cues,
            })
        elif section["type"] == "paragraph":
            content = section["content"]
            # Process content with spaCy
            doc = nlp(content)
            sentences = [sent.text for sent in doc.sents]

            # Summarize the content using Hugging Face
            summary_text = summarizer(content, max_length=100, min_length=20)[0]['summary_text']
            
             #  Simplest approach:  First sentence of summary
            main_idea = nlp(summary_text).sents[0].text if nlp(summary_text).sents else sentences[0] if sentences else "N/A"
            
            # Supporting details: all sentences that are not the main idea.
            supporting_details = " ".join([sent for sent in sentences if sent != main_idea]) if sentences else "N/A"

            cues = "What are the key points?"
            cornell_pages.append({
                "page_type": "paragraph",
                "title": "Paragraph",
                "main_idea": main_idea,
                "supporting_details": supporting_details,
                "cues": cues,
            })

    # Generate overall summary
    all_text = " ".join([s["content"] for s in sections])
    summary = summarizer(all_text, max_length=200, min_length=50)[0]['summary_text']
    return cornell_pages, summary

@app.route('/', methods=['GET', 'POST'])
def index():
    \"\"\"Handles the main page, processing text input and rendering the template.\"\"\"
    cornell_pages = []
    summary = ""
    template_name = 'index.html'  # Default template
    if request.method == 'POST':
        text = request.form['text']
        cornell_pages, summary = generate_conceptual_cornell_notes(text)
        if 'template' in request.form and request.form['template'] == 'vahini':
            template_name = 'vahini_template.html'
    return render_template(template_name, cornell_pages=cornell_pages, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
