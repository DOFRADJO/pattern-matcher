import cv2

def resize_frame(frame, width=None, height=None):
    """
    Redimensionne une image à la largeur ou hauteur spécifiée (en conservant les proportions).
    """
    if width is None and height is None:
        return frame

    h, w = frame.shape[:2]

    if width is not None:
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    else:
        ratio = height / float(h)
        dim = (int(w * ratio), height)

    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return resized

def draw_bbox(frame, bbox, color=(0, 255, 0), label=None):
    """
    Dessine une bounding box sur une image.
    """
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    if label:
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def convert_to_gray(image):
    """
    Convertit une image couleur en niveau de gris.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
