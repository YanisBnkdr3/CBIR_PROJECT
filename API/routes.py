from flask import request, jsonify
from . import api_bp
from descriptor import glcm
from distances import euclidean
import os

@api_bp.route('/search', methods=['POST'])
def search_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        UPLOAD_FOLDER = 'uploads'
        DATASET_FOLDER = 'datasets'
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        query_features = glcm(file_path)
        if query_features is None:
            return jsonify({'error': 'Error processing image'}), 500
        
        scores = []
        for root, dirs, files in os.walk(DATASET_FOLDER):
            for filename in files:
                if filename.endswith('.png') or filename.endswith('.jpg'):
                    image_path = os.path.join(root, filename)
                    feat_glcm = glcm(image_path)
                    dist = euclidean(query_features, feat_glcm)
                    relative_path = os.path.relpath(image_path, start=DATASET_FOLDER).replace("\\", "/")
                    scores.append((dist, relative_path))
        
        scores = sorted(scores, key=lambda x: x[0])
        
        return jsonify({'query_path': f'/uploads/{file.filename}', 'scores': scores[:10]})
