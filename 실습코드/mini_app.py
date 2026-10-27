from pathlib import Path
import cv2
import numpy as np
import streamlit as st

st.title("작은 이미지 탐색기 · OpenCV")
file = st.file_uploader("PNG 또는 JPG", type=["png", "jpg", "jpeg"])
raw = file.getvalue() if file is not None else (Path(__file__).parent / "assets/sample_rgb.png").read_bytes()
image = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
if image is None:
    st.error("이미지를 읽지 못했습니다. 다른 PNG 또는 JPG를 선택하세요.")
    st.stop()
st.caption("짧은 예제: 기본 컬러 읽기입니다. 알파 합성은 app.py에서 확인하세요.")
factor = st.slider("밝기 배율", 0.0, 2.0, 1.0, 0.1)
result = np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)
if st.checkbox("흑백으로 보기"):
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
left, right = st.columns(2)
left.image(image, channels="BGR", caption="원본", width="stretch")
if result.ndim == 2:
    right.image(result, caption="흑백 결과", width="stretch")
else:
    right.image(result, channels="BGR", caption="결과", width="stretch")
ok, buffer = cv2.imencode(".png", result)
if ok:
    st.download_button("결과 PNG 저장", buffer.tobytes(), "result.png", "image/png")
else:
    st.error("PNG 인코딩에 실패했습니다.")
