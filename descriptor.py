# Scikit-image
from skimage.feature import graycomatrix, graycoprops
import cv2
import numpy as np

def glcm(image_path):
    try:
        # Charger l'image en niveaux de gris
        data = cv2.imread(image_path, 0)
        
        # Vérifier si l'image est correctement lue
        if data is None:
            raise ValueError(f"Unable to load image at {image_path}")
        
        # Vérifier si l'image est en 2D
        if len(data.shape) != 2:
            raise ValueError(f"Expected 2D grayscale image, got {data.shape} dimensions")
        
        # Calculer la matrice GLCM
        co_matrix = graycomatrix(data, [1], [0], levels=256, symmetric=True, normed=True)
        diss = graycoprops(co_matrix, 'dissimilarity')[0,0]
        cont = graycoprops(co_matrix, 'contrast')[0,0]
        corr = graycoprops(co_matrix, 'correlation')[0,0]
        ener = graycoprops(co_matrix, 'energy')[0,0]
        asm = graycoprops(co_matrix, 'ASM')[0,0]
        homo = graycoprops(co_matrix, 'homogeneity')[0,0]
        
        return [diss, cont, corr, ener, asm, homo]
    
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None
