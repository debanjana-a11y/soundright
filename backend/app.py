from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from score import score_recording

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
REFERENCES = os.path.join(os.path.dirname(__file__), '..', 'references')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/score', methods=['POST'])
def score():
    # expected form: file field 'audio', form field 'reference' (filename in references/)
    if 'audio' not in request.files:
        return jsonify({'error': 'no audio file uploaded'}), 400
    f = request.files['audio']
    ref_name = request.form.get('reference')
    if not ref_name:
        return jsonify({'error': 'missing reference name'}), 400
    filename = secure_filename(f.filename)
    dest = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(dest)

    ref_path = os.path.join(REFERENCES, secure_filename(ref_name))
    if not os.path.exists(ref_path):
        return jsonify({'error': 'reference not found'}), 404

    try:
        score_val, details = score_recording(ref_path, dest)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'score': float(score_val), 'details': details})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
