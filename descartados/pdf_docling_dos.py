import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from docling.document_converter import DocumentConverter

def extract_text_from_pdf(input_path, output_path):
    """
    Extrae texto de un archivo PDF utilizando Docling y lo guarda en un archivo .txt.
    """
    try:
        # Extrae texto con Docling
        converter = DocumentConverter()
        text = converter.convert(input_path)

        # Guarda el texto extraído
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text.document.export_to_markdown())

    except Exception as e:
        print(f"Error procesando {input_path}: {e}")

def process_pdfs(input_folder, output_folder, max_workers=4):
    """
    Procesa todos los PDFs en una carpeta de entrada y los convierte a texto.
    Maneja errores de forma segura.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                extract_text_from_pdf,
                os.path.join(input_folder, pdf_file),
                os.path.join(output_folder, os.path.splitext(pdf_file)[0] + '.txt')
            ): pdf_file for pdf_file in pdf_files
        }

        for future in as_completed(futures):
            pdf_file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error procesando {pdf_file}: {e}")

if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) != 3:
        print("Uso: python pdf_docling_dos.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    start_time = time.time()
    process_pdfs(input_folder, output_folder)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")
