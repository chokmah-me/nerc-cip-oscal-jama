import pdfplumber
import os
from pathlib import Path

def extract_text_from_pdfs(pdf_dir, output_dir):
    """
    Iterates through all PDFs in a directory, extracts text, 
    and saves raw text files for AI processing.
    """
    pdf_path = Path(pdf_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    combined_text = ""
    
    files = list(pdf_path.glob('*.pdf'))
    print(f"Found {len(files)} PDF files in {pdf_dir}")

    for pdf_file in files:
        print(f"Processing: {pdf_file.name}...")
        text_content = f"--- START DOCUMENT: {pdf_file.name} ---\n"
        
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    # Extract text, preserving layout as best as possible
                    text = page.extract_text(x_tolerance=2, y_tolerance=2)
                    if text:
                        text_content += text + "\n"
            
            text_content += f"--- END DOCUMENT: {pdf_file.name} ---\n\n"
            
            # Save individual text file (good for debugging or granular processing)
            txt_filename = pdf_file.stem + ".txt"
            with open(output_path / txt_filename, 'w', encoding='utf-8') as f:
                f.write(text_content)
                
            combined_text += text_content
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")

    # Save the mega-file
    with open("nerc_all_combined.txt", 'w', encoding='utf-8') as f:
        f.write(combined_text)
    
    print(f"\n✅ Success! Extracted text from {len(files)} documents.")
    print(f"1. Individual text files saved in: {output_dir}/")
    print(f"2. Combined master file saved as: nerc_all_combined.txt")

if __name__ == "__main__":
    # CONFIGURATION
    # Create a folder named 'nerc_pdfs' and put your 40 files there
    PDF_SOURCE_DIR = "NERC-CIP" 
    OUTPUT_TEXT_DIR = "nerc_raw_text"
    
    if not os.path.exists(PDF_SOURCE_DIR):
        os.makedirs(PDF_SOURCE_DIR)
        print(f"Created directory '{PDF_SOURCE_DIR}'. Please drop your PDFs there and run again.")
    else:
        extract_text_from_pdfs(PDF_SOURCE_DIR, OUTPUT_TEXT_DIR)
