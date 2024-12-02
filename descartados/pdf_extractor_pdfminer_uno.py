from pdfminer.high_level import extract_text


print("******************** PROCESADO ********************")
text = extract_text('C:/PRUEBAS_PDF/SALIDA/PROCESADOS/0B2FFE18.pdf')
print(text)

print("******************** ERROR ********************")
text = extract_text('C:/PRUEBAS_PDF/SALIDA/ERROR/00B26978.pdf')
print(text)
