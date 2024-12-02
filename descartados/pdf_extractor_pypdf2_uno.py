import PyPDF2


print("******************** PROCESADO ********************")
with open('C:/PRUEBAS_PDF/SALIDA/PROCESADOS/0B2FFE18.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    
    # Extraer el texto de la primera página
    page = reader.pages[0]
    text = page.extract_text()
    
    print(text)

print("******************** ERROR ********************")
with open('C:/PRUEBAS_PDF/SALIDA/ERROR/00B26978.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    
    # Extraer el texto de la primera página
    page = reader.pages[0]
    text = page.extract_text()
    
    print(text)
