from pdf_extractor import PDFExtractor
import time

start_time = time.time()

extractor = PDFExtractor()
extractor.extract_text_to_file("C:/PRUEBAS_PDF/ENTRADA", "C:/PRUEBAS_PDF/SALIDA")

end_time = time.time()
execution_time = end_time - start_time

print(f"Tiempo de ejecución: {execution_time:.2f} segundos")