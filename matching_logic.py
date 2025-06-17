import cv2
import os
from db import frames_col

def match_template_in_video_frames(video_name: str, template_path: str):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError("Template introuvable")

    results = []
    h, w = template.shape

    for frame in frames_col.find({"video_name": video_name}):
        img_path = frame.get("image_path")
        if not img_path or not os.path.exists(img_path):
            continue

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None or img.shape[0] < h or img.shape[1] < w:
            continue

        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        results.append({
            "frame_id": frame.get("frame_id"),
            "timestamp": frame.get("timestamp"),
            "image_path": img_path,
            "match_score": round(float(max_val), 4),
            "match_position": {"x": max_loc[0], "y": max_loc[1]},
        })

    return results
