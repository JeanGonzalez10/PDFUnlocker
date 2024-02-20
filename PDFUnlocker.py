import os
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import ttk
import webbrowser
import sys
from PIL import ImageTk, Image

class  PDFUnlockerApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Unlocker") 
        self.setup_ui()

    def setup_ui(self):
        self.label_password = tk.Label(self.master, text="Ingrese la contraseña de los PDF's:")
        self.label_password.pack(anchor=tk.CENTER)

        self.input_password = tk.Entry(self.master, show='')
        self.input_password.pack(pady=20)

        self.btn_desbloquear = ttk.Button(self.master, text="Desbloquear PDFs", command=self.start_unlocker)
        self.btn_desbloquear.pack(pady=10)

        self.console_text = tk.Text(self.master, height=10, width=50)
        self.console_text.pack(pady=10)

        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

        self.label_creador = tk.Label(self.bottom_frame, text="Create by: Jean Carlos Gonzalez G.")
        self.label_creador.grid(row=0, column=0, sticky='w')

        image = Image.open(self.resource_path(r'images\github-mark.png'))
        image = image.resize((35, 35))

        self.image = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self.bottom_frame, image=self.image, cursor="hand2")

        self.image_label.bind("<Button-1>", self.open_web)
        self.image_label.grid(row=0, column=1, sticky='e', padx=172)

    def open_web(self, event):
        webbrowser.open_new(r'https://github.com/JeanGonzalez10/PDFUnlocker')

    def start_unlocker(self):

        folder_input = 'input'
        folder_output = 'output'
        password = self.input_password.get()

        if not os.path.exists(folder_output):
            os.makedirs(folder_output)

        files_input = os.listdir(folder_input)

        for file in files_input:
            path_input = os.path.join(folder_input, file)
            self.unlock_PDF(path_input, folder_output, password)

        msg = f'PDFs desbloqueados correctamente'
        self.update_console(msg)

    def unlock_PDF(self, file_input, folder_output, password):
        try:
            pdf_reader = PdfReader(file_input)

            # Desbloquear el PDF con la contraseña
            pdf_reader.decrypt(password)

            pdf_writer = PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Construir la ruta para el nuevo archivo PDF en la carpeta de salida
            path_output = os.path.join(folder_output, os.path.basename(file_input))

            # Guardar el nuevo archivo PDF
            with open(path_output, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            msg = f'PDF {os.path.basename(file_input)} desbloqueado y movido a la carpeta {folder_output}'
            self.update_console(msg)

            os.remove(file_input)

        except Exception as e:
            msg = f'Error al desbloquear {file_input}: {str(e)}'
            self.update_console(msg)

    def update_console(self, message):
        current_content = self.console_text.get("1.0", tk.END)
        self.console_text.delete("1.0", tk.END)
        self.console_text.insert(tk.END, current_content + message + "\n")

    def resource_path(self, relative_path: str):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFUnlockerApp(root)
    root.geometry("400x400")
    root.mainloop()