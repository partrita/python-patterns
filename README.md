# python-patterns.guide 소스 코드 (Quarto 변환 버전)

이 저장소는 Brandon Rhodes의 [python-patterns.guide](http://python-patterns.guide/) 사이트 소스를 기반으로 하며, 기존 Sphinx 구성을 **Quarto**와 **pixi**를 사용하도록 변환한 프로젝트입니다. GitHub Actions를 통해 GitHub Pages에 자동으로 배포되도록 설정되어 있습니다.

각 페이지의 실제 텍스트는 ©2018 Brandon Rhodes에게 모든 권리가 있습니다. 현재로서는 다른 곳에 텍스트가 복제되지 않고 제 자신의 아이디어를 기록할 자유를 누리고 있기 때문입니다.

## 프로젝트 개요

이 프로젝트는 Python 디자인 패턴에 대한 Brandon Rhodes의 가이드를 담고 있습니다. 원본의 reStructuredText (RST) 형식 문서를 `pandoc`을 통해 Quarto 마크다운(`qmd`)으로 변환하고, Quarto를 통해 정적 웹사이트 또는 책 형태로 빌드합니다. 패키지 및 실행 환경 관리는 `pixi`를 사용합니다.

## 프로젝트 설정 및 실행

### 필수 조건

* [pixi](https://pixi.sh/latest/) (패키지 관리자)
* Git

### 로컬에서 실행하기

1. **리포지토리 클론:**

   ```bash
   git clone <이 리포지토리의 URL>
   cd python-patterns
   ```

2. **의존성 설치 및 렌더링:**
   `pixi`를 사용하여 의존성을 설치하고, `rst` 파일을 `qmd`로 변환한 뒤, Quarto 책을 렌더링합니다.

   ```bash
   pixi run build
   ```
   *이 명령어는 내부적으로 `pixi install`, `python convert.py`, `quarto render mybook`을 순차적으로 실행합니다.*

3. **로컬에서 확인:**
   빌드가 완료되면 `mybook/_book` 디렉토리에 HTML 파일이 생성됩니다. 생성된 `index.html` 파일을 웹 브라우저에서 열어볼 수 있습니다.

   또는 Quarto의 미리보기 기능을 사용할 수 있습니다:
   ```bash
   pixi run quarto preview mybook
   ```

## 배포 (GitHub Pages)

이 프로젝트는 GitHub Actions를 통해 GitHub Pages에 자동으로 배포되도록 구성되어 있습니다.

`main` 브랜치나 `quarto-book` 브랜치에 변경 사항이 푸시되면 `.github/workflows/deploy.yml` 워크플로가 실행되어 자동으로 책을 빌드하고 배포합니다.

**설정 방법:**
GitHub 리포지토리의 **Settings > Pages** 메뉴로 이동하여, "Build and deployment" 섹션의 "Source"를 **"GitHub Actions"**로 설정해야 합니다.