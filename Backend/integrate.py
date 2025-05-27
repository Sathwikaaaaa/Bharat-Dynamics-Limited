from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from invoice import process_pdf, process_image, process_webcam  

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    field = request.form.get("field")
    file = request.files['file']
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if filename.lower().endswith('.pdf'):
            data = process_pdf(file_path)
        else:
            data = process_image(file_path)

        result = extract_selected_field(data, field)
        return jsonify(result)
    return jsonify({'error': 'No file uploaded'})

def extract_selected_field(data_list, field):
    results = []
    for data in data_list:
        results.append({field: data.get(field, 'Not Found')})
    return results

if __name__ == '__main__':
    app.run(debug=True)
