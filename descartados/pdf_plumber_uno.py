import pdfplumber

import os
import pathlib

class PDFPlumber:
    def extract_text_to_file(self, input_dir: str, output_dir: str) -> None:
        # Create output directory if it doesn't exist
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Iterate through all PDF files in input directory
        for pdf_file in os.listdir(input_dir):
            if pdf_file.lower().endswith('.pdf'):
                # Construct full input path
                pdf_path = os.path.join(input_dir, pdf_file)

                # Extract text from PDF
                text = self.extract_text_from_pdf(pdf_path)

                # Create output filename
                txt_filename = os.path.splitext(pdf_file)[0] + '.txt'
                output_path = os.path.join(output_dir, txt_filename)

                # Write extracted text to output file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                    
    def extract_text_to_file(self, pdf_path: str) -> None:
        # Open PDF and extract text
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
        
        # Get output path by replacing .pdf extension with .txt
        output_path = pdf_path.replace('.pdf', '.txt')
        
        # Write extracted text to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
