from PIL import Image
from typing import Optional


def crop_ui_elements(
    image_path: str,
    output_path: str,
    top_percent: float = 12,
    bottom_percent: float = 12
) -> str:
    """
    Rogne l'image pour enlever les barres d'interface (statut, navigation).
    
    Args:
        image_path: Chemin vers l'image originale
        output_path: Chemin où sauvegarder l'image rognée
        top_percent: Pourcentage à rogner en haut (défaut: 12%)
        bottom_percent: Pourcentage à rogner en bas (défaut: 12%)
    
    Returns:
        Le chemin de l'image rognée
    """
    with Image.open(image_path) as img:
        width, height = img.size
        
        # Calcul des coordonnées de pixels à conserver
        # left, top, right, bottom
        left = 0
        top = int(height * (top_percent / 100))
        right = width
        bottom = int(height * (1 - (bottom_percent / 100)))
        
        # Application du rognage
        cropped_img = img.crop((left, top, right, bottom))
        
        # Sauvegarde de l'image propre
        cropped_img.save(output_path)
        
    return output_path