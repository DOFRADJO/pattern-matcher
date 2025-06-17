import cv2
from db import frames_col
import os

def match_template_in_video_frames(video_name: str, template_path: str):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError("Template introuvable ou invalide")

    results = []
    template_h, template_w = template.shape

    for frame in frames_col.find({"video_name": video_name}):
        image_path = frame["image_path"]
        if not os.path.exists(image_path):
            continue

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None or img.shape[0] < template_h or img.shape[1] < template_w:
            continue

        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        # On enregistre toujours le résultat, quel que soit le score
        frame_match = {
            "video_name": video_name,
            "frame_id": frame["frame_id"],
            "image_path": frame["image_path"],
            "timestamp": frame["timestamp"],
            "match_score": round(float(max_val), 4),
            "match_position": {"x": max_loc[0], "y": max_loc[1]},
        }
        results.append(frame_match)

    return results
