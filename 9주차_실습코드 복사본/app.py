"""실행: uv run streamlit run app.py"""
from pathlib import Path
import hashlib
import cv2
import numpy as np
import streamlit as st
from image_ops import open_image, read_pixel, transform_image, to_png

st.set_page_config(page_title="이미지 탐색기 · OpenCV", layout="wide")
st.title("이미지 탐색기 · OpenCV")
st.caption("초급프로젝트 PBL · BGR 배열을 읽고, 값을 바꾸고, 결과를 비교합니다.")
assets = Path(__file__).parent / "assets"
with st.sidebar:
    st.header("이미지 선택")
    source_kind = st.radio("입력 방식", ["샘플 이미지", "직접 업로드"])
    if source_kind == "샘플 이미지":
        choice = st.selectbox("샘플", ["컬러 · 320×192", "흑백 · 8×8", "투명도 · BGRA"])
        name = {"컬러 · 320×192": "sample_rgb.png", "흑백 · 8×8": "sample_gray.png",
                "투명도 · BGRA": "sample_rgba.png"}[choice]
        raw = (assets / name).read_bytes()
    else:
        uploaded = st.file_uploader("JPG 또는 PNG", type=["jpg", "jpeg", "png"])
        if uploaded is None:
            st.info("이미지를 선택하면 탐색을 시작합니다.")
            st.stop()
        raw = uploaded.getvalue()
        name = uploaded.name
    st.caption("수업용 샘플은 직접 생성한 픽셀 데이터입니다.")
if len(raw) > 10 * 1024 * 1024:
    st.error("실습에서는 10 MiB 이하의 이미지를 선택하세요.")
    st.stop()
try:
    image, original = open_image(raw)
except (ValueError, OSError, cv2.error) as error:
    st.error(f"이미지를 열 수 없습니다: {error}")
    st.stop()
h, w = image.shape[:2]
identity = hashlib.sha256(raw).hexdigest()[:12]
info_tab, pixel_tab, process_tab = st.tabs(["1. 이미지 정보", "2. 픽셀 탐색", "3. 처리와 저장"])
with info_tab:
    left, right = st.columns([3, 2])
    left.image(image, channels="BGR", caption=name, width="stretch")
    right.subheader("파일과 배열")
    right.write({"파일 format": original["format"], "읽은 shape": original["shape"],
                 "처리 채널 순서": "BGR", "가로, 세로": (w, h),
                 "처리 shape": image.shape, "dtype": str(image.dtype),
                 "파일 bytes": len(raw), "배열 nbytes": image.nbytes})
    right.info("처리는 BGR로 통일합니다. 투명도는 흰 배경에 합성합니다. IMREAD_UNCHANGED를 사용하므로 EXIF 회전은 자동 적용하지 않습니다.")
with pixel_tab:
    left, right = st.columns([1, 2])
    x = int(left.number_input("x · 가로", 0, w - 1, 0, key=f"x_{identity}"))
    y = int(left.number_input("y · 세로", 0, h - 1, 0, key=f"y_{identity}"))
    color = read_pixel(image, x, y)
    left.code(f"image[{y}, {x}] = {color}  # BGR", language="python")
    left.write(f"같은 색의 RGB 값: {color[::-1]}")
    swatch = np.empty((80, 120, 3), dtype=np.uint8)
    swatch[:] = color
    left.image(swatch, channels="BGR", caption="선택 픽셀의 색")
    x0, y0 = max(0, x - 4), max(0, y - 4)
    x1, y1 = min(w, x + 5), min(h, y + 5)
    region = image[y0:y1, x0:x1]
    right.image(cv2.resize(region, (360, 360), interpolation=cv2.INTER_NEAREST),
                channels="BGR", caption=f"주변 영역 확대: x={x0}~{x1-1}, y={y0}~{y1-1}", width=360)
    right.caption("픽셀 관찰을 위해 칸을 확대했습니다. 원본 크기는 그대로입니다.")
with process_tab:
    controls, preview = st.columns([1, 3])
    width = int(controls.number_input("출력 너비", 1, 1600, min(w, 1600), key=f"width_{identity}"))
    factor = controls.slider("밝기 배율", 0.0, 2.0, 1.0, 0.1)
    grayscale = controls.checkbox("흑백으로 보기")
    try:
        result = transform_image(image, width, factor, grayscale)
    except ValueError as error:
        controls.warning(str(error))
        st.stop()
    a, b = preview.columns(2)
    a.image(image, channels="BGR", caption=f"원본 BGR · {w}×{h}", width="stretch")
    rh, rw = result.shape[:2]
    if result.ndim == 2:
        b.image(result, caption=f"흑백 결과 · {rw}×{rh}", width="stretch")
    else:
        b.image(result, channels="BGR", caption=f"BGR 결과 · {rw}×{rh}", width="stretch")
    controls.write(f"결과 shape: {result.shape}")
    controls.caption("비율 유지 → 밝기 배율 → 선택 시 흑백 변환")
    controls.download_button("결과 PNG 저장", to_png(result), "result.png", "image/png")
