import os
import hashlib
import bisect

def calcular_hash(archivo, bloque_size=65536):
    """ Calcula el hash SHA-256 de un archivo. """
    sha = hashlib.sha256()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(bloque_size), b""):
            sha.update(bloque)
    return sha.hexdigest()

def encontrar_archivos_repetidos(ruta_base, terminaciones=[], lista_negra=[], salida_txt="archivos_repetidos.txt"):
    archivos = {}

    # Recorrer la carpeta y subcarpetas
    print("buscando")
    for root, _, files in os.walk(ruta_base):
        for file in files:
            #extension = os.path.splitext(file)[1]  # Obtener la extensión del archivo
            extension = os.path.splitext(file)[1].lower()  # Convierte la extensión a minúsculas

            # Aplicar filtro de terminaciones
            if terminaciones and extension not in terminaciones:
                continue
            if not terminaciones and extension in lista_negra:
                continue

            ruta_completa = os.path.join(root, file)
            peso = os.path.getsize(ruta_completa)  # Obtener el tamaño del archivo

            if extension not in archivos:
                archivos[extension] = []

            # Usamos búsqueda binaria para insertar ordenado por peso
            bisect.insort(archivos[extension], (peso, ruta_completa))

    # Buscar archivos repetidos y calcular el peso total de archivos duplicados
    repetidos = []
    peso_total_repetidos = 0
    print("ordenando")
    terminaciones = []
    for ext, lista in archivos.items():
        if len(lista) > 100:
            print("  ",ext,len(lista))
        else:
            terminaciones.append(ext)
        i = 0
        while i < len(lista) - 1:
            grupo_repetidos = [lista[i][1]]
            hash1 = calcular_hash(lista[i][1])
            peso_archivo = lista[i][0]

            while i + 1 < len(lista) and lista[i][0] == lista[i + 1][0]:  # Mismo tamaño
                hash2 = calcular_hash(lista[i + 1][1])
                if hash1 == hash2:  # Si tienen el mismo hash, son duplicados
                    grupo_repetidos.append(lista[i + 1][1])
                    i += 1
                else:
                    break
            
            if len(grupo_repetidos) > 1:  # Si hay más de un archivo idéntico
                grupo_repetidos.sort()  # Ordenar alfabéticamente
                repetidos.append(" == ".join(grupo_repetidos))
                peso_total_repetidos += peso_archivo * (len(grupo_repetidos) - 1)  # Sumar el peso de los duplicados

            i += 1
    print(terminaciones)

    # Guardar resultados en un archivo de texto
    print("imprimiendo")
    with open(salida_txt, "w") as f:
        f.write(f"Peso total de archivos duplicados: {peso_total_repetidos} bytes\n\n")
        for linea in sorted(repetidos):  # Ordenar las líneas alfabéticamente antes de escribirlas
            f.write(linea + "\n")

    print(f"Proceso completado. Peso total de archivos duplicados: {peso_total_repetidos} bytes")
    print(f"Resultados guardados en {salida_txt}")

# Ejemplo de uso
ruta_a_analizar = "../"
terminaciones_a_incluir = []  # Si está vacío, se incluyen todas las terminaciones excepto las de la lista negra
lista_negra_terminaciones = [".exe", ".dll"]  # Se excluyen si terminaciones_a_incluir está vacío

encontrar_archivos_repetidos(ruta_a_analizar, terminaciones_a_incluir, lista_negra_terminaciones)
