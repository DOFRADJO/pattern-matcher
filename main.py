import cv2
import os
from utils import convert_to_gray
from flann_matcher import match_template_in_frame

# Chemins
video_path = "test.mp4"
template_path = "template.png"
output_dir = "output/frames_matched"

# Création du dossier de sortie s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)

# Charger template
template_img = cv2.imread(template_path)
template_gray = convert_to_gray(template_img)

cap = cv2.VideoCapture(video_path)

frame_id = 0
saved_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = convert_to_gray(frame)

    result_frame, found = match_template_in_frame(template_gray, frame_gray)

    label = f"Frame {frame_id} - {'FOUND' if found else 'NOT FOUND'}"
    cv2.putText(result_frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if found:
        filename = f"frame_{frame_id:04d}.jpg"
        save_path = os.path.join(output_dir, filename)
        cv2.imwrite(save_path, result_frame)
        saved_count += 1

    cv2.imshow("Pattern Matching", result_frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break

    frame_id += 1

cap.release()
cv2.destroyAllWindows()

print(f"\n✅ {saved_count} frames enregistrées avec motif détecté dans '{output_dir}'")
