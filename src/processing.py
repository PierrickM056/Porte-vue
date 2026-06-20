from PIL import Image

def crop_ui_elements(image_path, output_path, top_percent=12, bottom_percent=12):
    """
    Rogne l'image pour enlever les barres d'interface (statut, navigation).
    Par défaut, enlève 12% en haut et 12% en bas.
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