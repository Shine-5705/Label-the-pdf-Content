import PyPDF2
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict

# Download NLTK stopwords
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\W+', ' ', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return tokens

# Function to classify the document
def classify_document(text):
    keywords = {
        'court order': ['order', 'bench', 'justice', 'judgment', 'disposed', 'petition', 'court'],
        'writ petition': ['writ', 'petition', 'respondent', 'petitioner', 'jurisdiction', 'civil'],
        'notice': ['notice', 'served', 'inform', 'reply'],
        'summon': ['summon', 'appear', 'court'],
        'fir': ['fir', 'first information report', 'police', 'crime'],
        'tax invoice': ['invoice', 'tax', 'payment', 'amount', 'due']
    }

    tokens = preprocess_text(text)
    classification = defaultdict(int)

    for doc_type, keywords_list in keywords.items():
        keyword_count = sum([tokens.count(keyword) for keyword in keywords_list])
        classification[doc_type] = keyword_count

    classified_as = max(classification, key=classification.get)
    return classified_as

# Function to extract specific details from the text
def extract_details(text):
    details = {}

    # Extracting the case title
    case_title_match = re.search(r'(\w+ vs \w+)', text)
    if case_title_match:
        details['Case Title'] = case_title_match.group(0)

    # Extracting the date
    date_match = re.search(r'\d{1,2} \w+ \d{4}', text)
    if date_match:
        details['Date'] = date_match.group(0)

    # Extracting the bench information
    bench_match = re.findall(r'justice\s+(\w+\s+\w+)', text, re.IGNORECASE)
    if bench_match:
        details['Bench'] = ', '.join(bench_match)

    # Adding a default jurisdiction
    details['Jurisdiction'] = "Supreme Court of India, Civil Original Jurisdiction"

    # Extracting the writ petition number
    writ_petition_match = re.search(r'writ petition \(civil\) no\.\s+\d+ of \d{4}', text, re.IGNORECASE)
    if writ_petition_match:
        details['Writ Petition No'] = writ_petition_match.group(0)

    # Extracting key participants
    participants = re.findall(r'for petitioner\(s\):\s+(.+?)\s+for respondent\(s\):\s+(.+?)\n', text, re.IGNORECASE | re.DOTALL)
    if participants:
        details['For Petitioner(s)'] = participants[0][0].strip().replace('\n', ', ')
        details['For Respondent(s)'] = participants[0][1].strip().replace('\n', ', ')

    return details

# Main function to label PDF with detailed information
def label_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    document_type = classify_document(text)
    details = extract_details(text)
    details['Type of Document'] = document_type
    return details

# Example usage
file_path = 'pdfs/M_S_Tdi_Infrastructure_Limited_vs_Union_Of_India_on_7_January_2020.PDF'
labels = label_pdf(file_path)
for key, value in labels.items():
    print(f"{key}: {value}")

