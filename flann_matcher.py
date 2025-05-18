import cv2
import numpy as np

def match_template_in_frame(template_img, frame, min_match_count=10):
    """
    Recherche le template dans une frame en utilisant SIFT + FLANN + homographie.

    :param template_img: image du template (grayscale)
    :param frame: image vidéo (grayscale)
    :return: frame avec dessin (si match) et booléen match trouvé
    """
    sift = cv2.SIFT_create()

    kp1, des1 = sift.detectAndCompute(template_img, None)
    kp2, des2 = sift.detectAndCompute(frame, None)

    if des1 is None or des2 is None:
        return frame, False

    # FLANN parameters
    index_params = dict(algorithm=1, trees=5)  # KDTree
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    try:
        matches = flann.knnMatch(des1, des2, k=2)
    except:
        return frame, False

    # Ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > min_match_count:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if M is not None:
            h, w = template_img.shape
            pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            frame = cv2.polylines(frame, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
            return frame, True

    return frame, False
