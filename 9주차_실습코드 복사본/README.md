# Python 패키지와 이미지 처리 · uv 실행 안내

`실습코드` 폴더의 pyproject.toml, uv.lock, .python-version을 함께 사용합니다.
예제는 Python 3.12, Streamlit 1.50.0, OpenCV headless 4.12.0.88, NumPy 2.2.6을 사용합니다.
Python 3.12가 없으면 uv가 내려받을 수 있습니다.

## uv 설치 · 최초 한 번
Windows PowerShell(WinGet 사용):
```powershell
winget install --id=astral-sh.uv -e
```
macOS / Linux:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
macOS에서 Homebrew를 이미 사용한다면 `brew install uv`도 가능합니다.
설치 후 터미널을 다시 열고 `uv --version`을 실행합니다.
WinGet이 없거나 다른 설치 방법이 필요하면 [uv 공식 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)를 참고합니다.

## 배포된 예제 실행 · Windows / macOS 공통
터미널에서 app.py와 pyproject.toml이 있는 `실습코드` 폴더를 엽니다.
```sh
uv sync --locked
uv run streamlit run app.py
```
`uv sync --locked`는 잠금 파일과 설정이 맞는지 검사하고 그 버전으로 환경을 준비합니다.
`uv run`은 프로젝트 환경에서 실행합니다. 별도 가상환경 활성화는 필요 없습니다.
브라우저가 열리지 않으면 터미널의 Local URL을 엽니다. 종료는 Ctrl+C입니다.

## 예제 실행 명령
```sh
uv run python module_demo/main.py
uv run python inspect_image.py
uv run streamlit run first_app.py
uv run streamlit run mini_app.py
uv run streamlit run app.py
```
Streamlit 앱은 하나씩 실행합니다. 다른 앱으로 바꿀 때 기존 서버를 Ctrl+C로 종료합니다.

## 새 프로젝트를 만들 때
배포 예제에는 설정이 있으므로 아래 명령을 다시 실행하지 않습니다.
빈 새 폴더에서 프로젝트를 시작하는 경우의 예입니다.
```sh
uv init --bare --python 3.12
uv add streamlit opencv-python-headless numpy
```
새 프로젝트의 `uv add`는 실행 시점의 호환 버전을 선택합니다. 수업 예제의 확정 버전은 동봉된 uv.lock을 사용합니다.

## 예제의 데이터
- 컬러 샘플: 가로320·세로192, BGR shape=(192,320,3), dtype=uint8, nbytes=184320
- x=5,y=2는 image[2,5]로 접근합니다. BGR=[40,2,3], RGB=[3,2,40]입니다.
- 출력 너비 160 → 높이 96. 밝기 0.0 → 검정. 흑백 → 2차원 배열.
- 결과 PNG를 다시 올려 저장한 크기가 유지되는지 확인합니다.

## 파일과 환경
설치에는 인터넷이 필요합니다. 설치 후에는 외부 API 없이 샘플과 로컬 업로드로 실습합니다.
입력은 PNG/JPEG만 받으며 교육용 앱에서는 10 MiB·1200만 픽셀까지 사용합니다.
완성 앱은 IMREAD_UNCHANGED로 읽어 투명 입력을 흰 배경에 합성한 후 BGR로 처리합니다.
이 옵션은 EXIF 회전을 자동 적용하지 않습니다. 휴대폰 사진의 방향은 미리 확인합니다.
실습 입력은 uint8(채널당 8-bit)로 제한합니다. 16-bit PNG는 안내와 함께 거부합니다.
픽셀 수 제한은 디코딩 후 확인하는 수업용 검사이며 공개 서비스의 자원 보호 장치로 사용하지 않습니다.
샘플은 직접 생성한 픽셀 데이터이며 환자 데이터나 진단 결과가 아닙니다.
pyproject.toml에 직접 의존성을 선언하고, uv.lock에 간접 의존성을 포함한 확정 버전을 기록했습니다.
.python-version은 Python 3.12를 선택합니다. .venv는 배포하지 않으며 uv sync로 다시 만듭니다.

## OpenCV와 Pillow 비교
- 이번 이미지 처리 코드는 OpenCV(cv2)와 NumPy를 사용하며 PIL을 import하지 않습니다.
- OpenCV는 기본 컬러 읽기에서 BGR ndarray를 반환하고, Pillow는 RGB 등의 모드를 가진 Image 객체를 사용합니다.
- OpenCV 설치 종류 네 가지는 모두 cv2를 사용하므로 한 환경에 하나만 설치하세요. Streamlit 화면에는 headless가 적합합니다.
- Streamlit 내부 의존성으로 Pillow가 설치될 수 있습니다. 수업 코드에서 Pillow를 사용한다는 뜻은 아닙니다.
- st.image(image, channels="BGR") 또는 BGR2RGB 변환 후 st.image(rgb) 중 한 방법을 사용합니다.
- imencode에는 BGR/흑백 배열을 전달합니다. 표시용 RGB를 그대로 저장하면 색이 바뀔 수 있습니다.
