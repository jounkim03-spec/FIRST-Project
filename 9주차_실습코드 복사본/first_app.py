import streamlit as st
st.title("나의 첫 이미지 앱")
st.write("Python으로 웹 화면을 만듭니다.")
factor = st.slider("밝기 배율", 0.0, 2.0, 1.0, 0.1)
st.write("100 × 배율:", 100 * factor)
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("한 번 더"):
    st.session_state.count += 1
st.write("클릭 횟수:", st.session_state.count)
