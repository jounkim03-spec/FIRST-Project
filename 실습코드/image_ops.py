"""OpenCV + NumPy 처리 함수. 내부 컬러 배열은 BGR, 출력은 BGR 또는 흑백."""
from pathlib import Path
import cv2
import numpy as np

MAX_PIXELS = 12_000_000

def open_image(source):
    if isinstance(source, (str, Path)):
        raw = Path(source).read_bytes()
    elif isinstance(source, bytes):
        raw = source
    else:
        raw = source.read()
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        file_format = "PNG"
    elif raw.startswith(b"\xff\xd8\xff"):
        file_format = "JPEG"
    else:
        raise ValueError("PNG 또는 JPEG 이미지를 선택하세요.")
    data = np.frombuffer(raw, dtype=np.uint8)
    # 채널과 비트 깊이를 보존합니다. 이 옵션은 EXIF 회전을 자동 적용하지 않습니다.
    original = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    if original is None:
        raise ValueError("이미지 바이트를 해석하지 못했습니다.")
    h, w = original.shape[:2]
    if h * w > MAX_PIXELS:
        raise ValueError("실습에서는 1,200만 픽셀 이하의 이미지를 사용하세요.")
    if original.dtype != np.uint8:
        raise ValueError("실습에서는 채널당 8-bit PNG/JPEG를 사용하세요.")
    metadata = {"format": file_format, "shape": original.shape,
                "dtype": str(original.dtype), "stored_size": (w, h)}
    if original.ndim == 2:
        bgr = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    elif original.shape[2] == 4:
        # BGRA의 투명도는 흰 배경에 합성합니다. 원본 파일은 변경하지 않습니다.
        alpha = original[:, :, 3:4].astype(np.float32) / 255.0
        colors = original[:, :, :3].astype(np.float32)
        bgr = np.rint(colors * alpha + 255 * (1 - alpha)).astype(np.uint8)
    elif original.shape[2] == 3:
        bgr = original.copy()
    else:
        raise ValueError("지원하지 않는 채널 수입니다.")
    return bgr, metadata

def read_pixel(image, x, y):
    h, w = image.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        raise ValueError("이미지 범위 안의 좌표를 선택하세요.")
    return image[y, x].tolist()

def transform_image(image, width, factor=1.0, grayscale=False):
    if width < 1 or not np.isfinite(factor) or factor < 0:
        raise ValueError("너비는 1 이상, 밝기 배율은 0 이상의 유한한 수여야 합니다.")
    h, w = image.shape[:2]
    height = max(1, round(h * width / w))
    if width * height > MAX_PIXELS:
        raise ValueError("출력 픽셀 수가 너무 큽니다. 너비를 줄이세요.")
    method = cv2.INTER_AREA if width < w else cv2.INTER_LINEAR
    result = cv2.resize(image, (width, height), interpolation=method)
    work = result.astype(np.float32) * factor
    result = np.clip(work, 0, 255).astype(np.uint8)
    return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) if grayscale else result

def to_png(image):
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("PNG 인코딩에 실패했습니다.")
    return buffer.tobytes()
