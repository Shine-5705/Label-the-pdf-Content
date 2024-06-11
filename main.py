import PyPDF2
import csv
import os

def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        num_pages = reader.numPages
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            pdf_text += page.extractText()
    return pdf_text

def categorize_document(pdf_text):
    if "IN THE SUPREME COURT OF INDIA" in pdf_text or "COURT" in pdf_text:
        return "Court Order / Writ Petition Disposition"
    elif "FIRST INFORMATION REPORT" in pdf_text or "FIR" in pdf_text:
        return "FIR"
    elif "NOTICE" in pdf_text:
        return "Notice"
    elif "SUMMONS" in pdf_text:
        return "Court Summon"
    elif "TAX INVOICE" in pdf_text or "INVOICE" in pdf_text:
        return "Tax Invoice"
    else:
        return "Other"

def process_pdf(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    document_type = categorize_document(pdf_text)
    return document_type, pdf_text

def write_to_csv(data, csv_path):
    headers = ["File Name", "Document Type", "Extracted Text"]
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

def main(pdf_directory, output_csv_path):
    data = []
    for file_name in os.listdir(pdf_directory):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, file_name)
            document_type, pdf_text = process_pdf(pdf_path)
            data.append([file_name, document_type, pdf_text])
    write_to_csv(data, output_csv_path)

# Define the directory containing the PDFs and the path for the output CSV
pdf_directory = 'pdfs'
output_csv_path = 'output_csv/output1.csv'

# Run the main function
main(pdf_directory, output_csv_path)
