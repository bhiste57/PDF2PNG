import os
import sys
from flask import Flask, request, send_file, render_template
from pdf2image import convert_from_bytes
from io import BytesIO

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

# Poppler path uniquement sous Windows
if sys.platform == "win32":
    POPPLER_PATH = os.path.join(base_dir, "poppler", "Library", "bin")
else:
    POPPLER_PATH = None


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    try:
        print("📥 Fichier reçu : ", request.files)
        pdf_file = request.files['pdf_file']
        pdf_bytes = pdf_file.read()

        kwargs = {
            "dpi": 300,
            "first_page": 1,
            "last_page": 1
        }
        if POPPLER_PATH:
            kwargs["poppler_path"] = POPPLER_PATH

        print("🔧 Conversion avec kwargs :", kwargs)
        images = convert_from_bytes(pdf_bytes, **kwargs)

        img_io = BytesIO()
        images[0].save(img_io, format='PNG')
        img_io.seek(0)

        print("✅ Conversion OK")
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='page1.png'
        )
    except Exception as e:
        print("❌ Erreur pendant le traitement :", str(e))
        return "Erreur interne", 500



if __name__ == '__main__':
    app.run(debug=True)
