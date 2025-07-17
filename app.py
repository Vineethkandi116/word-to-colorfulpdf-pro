from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import uuid
from docx2pdf import convert

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Optional: Clear old uploads on startup
for f in os.listdir(UPLOAD_FOLDER):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    except:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    file = request.files['word_file']
    bg_color = request.form['bg_color']
    text_color = request.form['text_color']
    watermark = request.form.get('watermark', '')

    # Save with a unique name to avoid overwrite or PermissionError
    filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{file.filename}")
    file.save(filename)

    # Convert to PDF
    output_pdf = os.path.join(OUTPUT_FOLDER, 'converted.pdf')
    convert(filename, output_pdf)

    # Save user enhancement choices for future use (if needed)
    with open(os.path.join(OUTPUT_FOLDER, 'overlay.txt'), 'w') as f:
        f.write(f"{bg_color}\n{text_color}\n{watermark}")

    return render_template("pdf_preview.html", pdf_file='converted.pdf')

@app.route('/download')
def download():
    return send_file(os.path.join(OUTPUT_FOLDER, 'converted.pdf'), as_attachment=True)

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=True)
