from flask import Flask, request, send_file
from flask import Flask, render_template
import traceback
from PyPDF2 import PdfMerger
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs():
    try:
        create_upload_folder()  # Crear el directorio de carga si no existe
        merger = PdfMerger()
        for file in request.files.getlist('pdfFiles[]'):
            if file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + '.pdf')
                file.save(file_path)
                print(f"Archivo guardado: {file_path}")  # Agregar declaración de registro
                merger.append(file_path)
        if merger.pages:
            merged_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged_pdf.pdf')
            merger.write(merged_file_path)
            merger.close()
            print("PDFs fusionados exitosamente.")  # Agregar declaración de registro
            return send_file(merged_file_path, as_attachment=True)
        else:
            error_message = "No se han seleccionado archivos PDF para fusionar."
            print(error_message)  # Agregar declaración de registro
            return error_message, 400
    except Exception as e:
        error_message = f"Error durante la fusión de PDF: {e}"
        traceback.print_exc()
        return error_message, 500


if __name__ == '__main__':
    app.run(debug=True)
