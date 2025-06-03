from flask import Flask, render_template, request
import hashlib, os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def hash_text(text, algorithm='sha256'):
    h = hashlib.new(algorithm)
    h.update(text.encode('utf-8'))
    return h.hexdigest()

def hash_file(file_path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

@app.route('/', methods=['GET', 'POST'])
def index():
    hash_result = ''
    selected_algo = ''
    text_input = ''
    file_uploaded = ''
    verify_result = ''
    entered_hash = ''

    if request.method == 'POST':
        text_input = request.form.get('text_input', '')
        entered_hash = request.form.get('entered_hash', '')
        uploaded_file = request.files.get('file')

        if 'hash_sha256' in request.form:
            selected_algo = 'sha256'
            if uploaded_file and uploaded_file.filename != '':
                path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(path)
                hash_result = hash_file(path, selected_algo)
                file_uploaded = uploaded_file.filename
            elif text_input.strip():
                hash_result = hash_text(text_input, selected_algo)

        elif 'hash_sha512' in request.form:
            selected_algo = 'sha512'
            if uploaded_file and uploaded_file.filename != '':
                path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(path)
                hash_result = hash_file(path, selected_algo)
                file_uploaded = uploaded_file.filename
            elif text_input.strip():
                hash_result = hash_text(text_input, selected_algo)

        elif 'verify_hash' in request.form:
            selected_algo = 'sha512'
            if uploaded_file and uploaded_file.filename != '' and entered_hash.strip():
                path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(path)
                computed_hash = hash_file(path, selected_algo)
                file_uploaded = uploaded_file.filename
                if computed_hash == entered_hash.strip():
                    verify_result = '✅ File toàn vẹn (không bị chỉnh sửa).'
                else:
                    verify_result = '❌ File đã bị thay đổi hoặc mã băm không khớp!'

    return render_template('index.html',
                           hash_result=hash_result,
                           selected_algo=selected_algo.upper(),
                           text_input=text_input,
                           file_uploaded=file_uploaded,
                           verify_result=verify_result,
                           entered_hash=entered_hash)

if __name__ == '__main__':
    app.run(debug=True)
