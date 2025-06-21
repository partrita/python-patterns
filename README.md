# python-patterns.guide 소스 코드

이것은 Brandon Rhodes의 [python-patterns.guide](http://python-patterns.guide/) 사이트의 소스입니다. 이 저장소는 Sphinx를 사용하여 이 정적 사이트를 생성하는 방법을 확인하는 데 도움이 될 수 있습니다.

각 페이지의 실제 텍스트는 ©2018 Brandon Rhodes에게 모든 권리가 있습니다. 현재로서는 다른 곳에 텍스트가 복제되지 않고 제 자신의 아이디어를 기록할 자유를 누리고 있기 때문입니다.

하지만 MIT 라이선스에 따라 CSS 및 Makefile에서 자유롭게 빌려가십시오\!

## 프로젝트 개요

이 프로젝트는 Python 디자인 패턴에 대한 Brandon Rhodes의 가이드를 담고 있습니다. Sphinx를 통해 reStructuredText (RST) 형식으로 작성된 문서를 HTML 정적 웹사이트로 변환합니다.

## 프로젝트 설정 및 실행

### 필수 조건

  * Python 3.x
  * pip (Python 패키지 설치 도구)
  * Git

### 로컬에서 실행하기

1.  **리포지토리 클론:**

    ```bash
    git clone https://github.com/brandon-rhodes/python-patterns.git
    cd python-patterns
    ```

2.  **의존성 설치:**
    이 프로젝트는 Sphinx와 테마를 사용합니다. `requirements.txt` 파일에 필요한 패키지들이 명시되어 있습니다.

    ```bash
    pip install -r requirements.txt
    ```

3.  **문서 빌드:**
    문서를 HTML로 빌드하려면 다음 명령어를 실행합니다.

    ```bash
    sphinx-build -b html docs/source docs/build
    ```

    이 명령은 `docs/source` 디렉토리의 RST 파일을 읽어 `docs/build` 디렉토리에 HTML 파일을 생성합니다.

4.  **로컬에서 확인:**
    빌드가 완료되면 `docs/build` 디렉토리로 이동하여 `index.html` 파일을 웹 브라우저에서 열어볼 수 있습니다.

    ```bash
    open docs/build/index.html # macOS
    start docs/build/index.html # Windows
    xdg-open docs/build/index.html # Linux
    ```

## Sphinx-friendly 배포 옵션

Sphinx 문서를 호스팅할 수 있는 몇 가지 옵션이 있고 저는 아래 방법을 사용했습니다.

### Read the Docs

[Read the Docs](https://readthedocs.org/)는 Sphinx 및 MkDocs로 작성된 기술 문서 호스팅을 전문으로 하는 온라인 서비스입니다. 버전 관리 문서, 트래픽 및 검색 분석, 사용자 지정 도메인, 사용자 정의 리디렉션 등 다양한 추가 기능을 제공합니다.
