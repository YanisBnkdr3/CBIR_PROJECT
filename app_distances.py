from descriptor import glcm
from distances import euclidean, manhattan, chebyshev, canberra
import os

def calculate_distances(base_path='datasets'):
    # Parcourir les sous-dossiers pour extraire les caractéristiques GLCM de toutes les images
    image_features = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                image_path = os.path.join(root, file)
                feat_glcm = glcm(image_path)
                image_features.append((image_path, feat_glcm))
    
    # Calculer et afficher les distances entre chaque paire d'images
    for i in range(len(image_features)):
        for j in range(i + 1, len(image_features)):
            path1, feat1 = image_features[i]
            path2, feat2 = image_features[j]
            print(f'Comparing {path1} and {path2}:')
            print(f'Euclidean: {euclidean(feat1, feat2)}')
            print(f'Manhattan: {manhattan(feat1, feat2)}')
            print(f'Chebyshev: {chebyshev(feat1, feat2)}')
            print(f'Canberra: {canberra(feat1, feat2)}')
            print()

def main():
    calculate_distances()

if __name__ == '__main__':
    main()
