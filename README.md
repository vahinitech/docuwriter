# Vahini AI DocuWriter

Vahini AI DocuWriter is a Flask-based web application that intelligently processes and formats text captured by the Vahini AI Pen. It transforms raw text into structured digital formats, catering to various needs such as Cornell Notes, CoreNLP-style output, doctor prescriptions, and receipts.

## Features

* **Input Processing**: Processes text captured by the Vahini AI Pen.
* **Multi-Template Support**: Converts captured text into different formats:
    * Cornell Notes: For structured learning and note-taking.
    * Corenll Output: For linguistic analysis.
    * Doctor Prescription: For medical prescriptions.
    * Receipt: For generating formatted receipts.
    * Custom Template: For user-defined formatting.
* **Text Analysis**: Analyzes input text for:
    * Spelling mistakes
    * Intent
    * Confidence level
    * Sentiment
    * Sentiment Confidence
    * Text Classification
    * Classification Confidence
* **AI-Powered Analysis**:
    * Hugging Face Transformers for advanced NLP tasks (summarization, sentiment analysis, text classification).
    * spaCy for efficient text processing (sentence detection, etc.).
* **Output Viewing**: Displays the converted text in a user-friendly format.
* **Customizable Styling**: Styled with CSS for a visually appealing and user-friendly experience.

## Technical Details

* Built with Flask (Python web framework).
* Uses Jinja2 for templating.
* Natural Language Processing (NLP) with libraries like spaCy and Hugging Face Transformers.
* Python SpellChecker.

## Prerequisites

* Python 3.10
* pip
* A system that supports running the required Python libraries
* Install the packages from the  `requirements.txt`  file
* Install the English language model for spaCy:  `python -m spacy download en_core_web_sm`

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd cornell_notes_app
    ```
2.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  Download the required spaCy model:

    ```bash
    python -m spacy download en_core_web_sm
    ```

## Usage

1.  Run the Flask application:

    ```bash
    python app.py
    ```

2.  Open your web browser and go to  `http://127.0.0.1:5000/`.

3.  Paste your text into the text area.

4.  Select the desired output format from the dropdown menu.

5.  Click the "Convert" button.

6.  The converted text will be displayed in the selected format.

## Templates

The application provides the following templates:

* **Cornell Notes**:  For structured note-taking, with sections for main ideas, supporting details, and cues/questions.
* **Corenll Output**:  For linguistic analysis, formatted in a way that is similar to the output of the CoreNLP tool.
* **Doctor Prescription**:  For displaying medical prescriptions, with fields for patient name, date, medicines, dosages, and instructions.
* **Receipt**:  For generating formatted receipts, with fields for order ID, customer name, items, prices, and total.
* **Custom Template**:  A basic template that you can customize.

## Input Text Formatting

To ensure accurate conversion, please format the input text as follows:

### General Text
For general text, you can use headings and paragraphs.

* **Headings:** Use the following format for headings:

    ```
    Heading Text
    ====
    ```

    or

    ```
    Heading Text
    ----
    ```

* **Paragraphs:** Separate paragraphs with double newlines:

    ```
    This is the first paragraph.

    This is the second paragraph.
    ```

### Doctor Prescription

For prescription data, use the following format:

```text
Patient Name: John Doe
Medicine 1: Paracetamol
Dosage: 500mg
Instructions: Take twice daily after meals.
Medicine 2: Amoxicillin
Dosage: 250mg
Instructions: Take three times daily for 7 days.
```

### Receipt

For receipt data, use the following format:

```text
Order ID: 12345
Customer Name: Jane Smith
Item: Product A
Price: $25
Item: Product B
Price: $10
Total:Price: $35
```

## Text Analysis

The application analyzes the input text and provides the following information:

* **Spelling Mistakes**:  A list of misspelled words.
* **Intent**:  The detected intent of the text (e.g., "Informative," "Persuasive," "Speculative").
* **Confidence**:  The confidence level of the intent detection (e.g., "High," "Medium," "Low").
* **Sentiment**:  The overall sentiment of the text (e.g., "Positive," "Negative," "Neutral").
* **Sentiment Confidence**:  The confidence level of the sentiment analysis.
* **Classification**: The type of text.
* **Classification Confidence**: The confidence level of the classification.

## Contributing

Contributions are welcome!  If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Write tests to cover your changes.
5.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
