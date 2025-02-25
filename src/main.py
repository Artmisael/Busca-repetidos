import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

def hash_file(filepath):
    """Calcula el hash SHA-256 de un archivo"""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def buscar_duplicados(extension_list, folder_path, output_path):
    archivos = {}
    duplicados = []
    peso_total = 0
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extension_list):
                filepath = os.path.join(root, file)
                file_size = os.path.getsize(filepath)
                file_hash = hash_file(filepath)
                
                key = (file_size, file_hash)
                
                if key in archivos:
                    archivos[key].append(filepath)
                else:
                    archivos[key] = [filepath]
    
    for key, paths in archivos.items():
        if len(paths) > 1:
            duplicados.append(paths)
            peso_total += key[0] * (len(paths) - 1)  # Sumar el peso de los duplicados
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Peso total de archivos duplicados: {peso_total / 1024 / 1024:.2f} MB\n\n")
        for grupo in sorted(duplicados):
            f.write("\n".join(grupo) + "\n\n")
    
    messagebox.showinfo("Completado", f"Proceso finalizado. Resultados guardados en {output_path}")

def seleccionar_origen():
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry_origen.delete(0, tk.END)
        entry_origen.insert(0, carpeta)

def seleccionar_destino():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
    if archivo:
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, archivo)

def ejecutar_busqueda(extension_list):
    folder_path = entry_origen.get()
    output_path = entry_destino.get()
    
    if not folder_path or not output_path:
        messagebox.showerror("Error", "Debe seleccionar la carpeta de origen y destino")
        return
    
    buscar_duplicados(extension_list, folder_path, output_path)

# Extensiones predefinidas
ext_imagenes = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
ext_texto = [".txt", ".doc", ".docx", ".pdf"]
ext_audio = [".mp3", ".wav", ".aac", ".flac"]
ext_videos = [".mp4", ".avi", ".mkv", ".mov"]
ext_bases_datos = [".csv", ".xls", ".xlsx", ".sql"]

# Crear la ventana
root = tk.Tk()
root.title("Buscador de archivos duplicados")
root.geometry("500x400")

tk.Label(root, text="Carpeta de origen:").pack()
entry_origen = tk.Entry(root, width=50)
entry_origen.pack()
tk.Button(root, text="Seleccionar", command=seleccionar_origen).pack()

tk.Label(root, text="Guardar resultados en:").pack()
entry_destino = tk.Entry(root, width=50)
entry_destino.pack()
tk.Button(root, text="Seleccionar", command=seleccionar_destino).pack()

tk.Label(root, text="Seleccione el tipo de archivo:").pack()
tk.Button(root, text="Imágenes", command=lambda: ejecutar_busqueda(ext_imagenes)).pack()
tk.Button(root, text="Texto", command=lambda: ejecutar_busqueda(ext_texto)).pack()
tk.Button(root, text="Audio", command=lambda: ejecutar_busqueda(ext_audio)).pack()
tk.Button(root, text="Videos", command=lambda: ejecutar_busqueda(ext_videos)).pack()
tk.Button(root, text="Bases de datos", command=lambda: ejecutar_busqueda(ext_bases_datos)).pack()

root.mainloop()
