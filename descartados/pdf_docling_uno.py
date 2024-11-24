from docling.document_converter import DocumentConverter
import os
import pathlib

class PDFDocling:
    def extract_text_to_file(self, input_dir: str, output_dir: str) -> None:
        # Create output directory if it doesn't exist
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        converter = DocumentConverter()
        
        # Iterate through all PDF files in input directory
        for pdf_file in os.listdir(input_dir):
            if pdf_file.lower().endswith('.pdf'):
                # Construct full input path
                pdf_path = os.path.join(input_dir, pdf_file)
                
                # Convert PDF to text
                result = converter.convert(pdf_path)
                
                # Create output filename
                txt_filename = os.path.splitext(pdf_file)[0] + '.md'
                output_path = os.path.join(output_dir, txt_filename)
                
                # Write converted text to output file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result.document.export_to_markdown())

