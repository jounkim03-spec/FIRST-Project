from pathlib import Path
import cv2
import numpy as np
from image_ops import open_image
image, metadata = open_image(Path(__file__).parent / "assets/sample_rgb.png")
print("shape:", image.shape, "dtype:", image.dtype, "nbytes:", image.nbytes)
print("x=5, y=2 BGR:", image[2, 5].tolist())
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
print("same pixel RGB:", rgb[2, 5].tolist())
print("uint8 250+20:", (np.array([250], dtype=np.uint8) + 20).tolist())
print("safe 250+20:", np.clip(np.array([250], dtype=np.float32) + 20, 0, 255).astype(np.uint8).tolist())
