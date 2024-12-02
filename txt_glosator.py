import os
import sys
import re

def actualizar_diccionario(input_folder, output_folder):
    # Verificar si las carpetas existen
    if not os.path.isdir(input_folder):
        raise FileNotFoundError(f"La carpeta de entrada '{input_folder}' no existe o no es válida.")
    if not os.path.isdir(output_folder):
        raise FileNotFoundError(f"La carpeta de salida '{output_folder}' no existe o no es válida.")
    
    # Ruta del archivo de salida
    diccionario_path = os.path.join(output_folder, 'DICCIONARIO.txt')
    
    # Leer palabras existentes en el diccionario (si existe)
    palabras_diccionario = set()
    if os.path.exists(diccionario_path):
        with open(diccionario_path, 'r', encoding='utf-8') as f:
            for linea in f:
                palabras_diccionario.update(linea.strip().split())
    
    # Procesar los archivos .txt en la carpeta de entrada
    for archivo in os.listdir(input_folder):
        if archivo.endswith('.txt'):
            archivo_path = os.path.join(input_folder, archivo)
            try:
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    for linea in f:
                        # Extraer palabras usando expresiones regulares
                        # palabras = re.findall(r'\b\w+\b', linea.lower())

                        # Extraer palabras alfabéticas (excluye números)
                        palabras = re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+\b', linea.lower())

                        palabras_diccionario.update(palabras)
            except Exception as e:
                print(f"Error al leer el archivo '{archivo}': {e}")
    
    # Escribir el diccionario ordenado en el archivo de salida
    try:
        with open(diccionario_path, 'w', encoding='utf-8') as f:
            for palabra in sorted(palabras_diccionario):
                f.write(f"{palabra}\n")
        print(f"DICCIONARIO.txt actualizado y guardado en '{diccionario_path}'.")
    except Exception as e:
        print(f"Error al escribir el archivo DICCIONARIO.txt: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python txt_glosator.py <carpeta_entrada> <carpeta_salida>")
    else:
        try:
            input_folder = sys.argv[1]
            output_folder = sys.argv[2]
            actualizar_diccionario(input_folder, output_folder)
        except Exception as e:
            print(f"Error: {e}")
