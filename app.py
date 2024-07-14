app.py:from flask import Flask, render_template, request, send_from_directory
from descriptor import glcm
from distances import euclidean
import os
 
app = Flask(__name__)
 
# Dossier pour les téléchargements
UPLOAD_FOLDER = 'uploads'
DATASET_FOLDER = 'datasets'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
 
@app.route('/datasets/<path:filename>')
def dataset_file(filename):
    return send_from_directory(DATASET_FOLDER, filename)
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'query_img' not in request.files:
            return 'Aucun fichier sélectionné'
        file = request.files['query_img']
        if file.filename == '':
            return 'Aucun fichier sélectionné'
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
           
            # Calculer les caractéristiques de l'image téléchargée
            query_features = glcm(file_path)
 
            # Parcourir le dossier dataset pour trouver les images similaires
            scores = []
            for root, dirs, files in os.walk(DATASET_FOLDER):
                for filename in files:
                    if filename.endswith('.png') or filename.endswith('.jpg'):
                        image_path = os.path.join(root, filename)
                        feat_glcm = glcm(image_path)
                        dist = euclidean(query_features, feat_glcm)
                        relative_path = os.path.relpath(image_path, start=DATASET_FOLDER).replace("\\", "/")
                        print(f"Chemin relatif de l'image : {relative_path}")
                        scores.append((dist, relative_path))
           
            # Trier les scores
            scores = sorted(scores, key=lambda x: x[0])
           
            return render_template('index.html', query_path=f'/uploads/{file.filename}', scores=scores[:10])
   
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug=True)