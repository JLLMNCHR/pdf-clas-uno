import os
import fitz  # PyMuPDF
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_text_from_pdf(input_path, output_path):
    """
    Extrae el texto de un archivo PDF y lo guarda en un archivo de texto.
    """
    try:
        with fitz.open(input_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        
        # Escribe el texto extraído en el archivo de salida
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
    except Exception as e:
        print(f"Error procesando {input_path}: {e}")

def process_pdfs(input_folder, output_folder, max_workers=4):
    """
    Procesa todos los PDFs en una carpeta y extrae el texto a la carpeta de salida.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    tasks = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for pdf_file in pdf_files:
            input_path = os.path.join(input_folder, pdf_file)
            output_path = os.path.join(output_folder, os.path.splitext(pdf_file)[0] + '.txt')
            tasks.append(executor.submit(extract_text_from_pdf, input_path, output_path))
        
        for future in as_completed(tasks):
            future.result()  # Esto asegura que los errores en los hilos sean manejados

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Uso: python script.py <carpeta_entrada> <carpeta_salida>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    start_time = time.time()
    process_pdfs(input_folder, output_folder, max_workers=4)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time:.2f} segundos")
