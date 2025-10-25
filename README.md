# VS Code Verilog 자동 정리 & 스니펫 설정 가이드

## 📦 필요한 파일들
1. `verilog_formatter_cli.py` - Python 포맷터 스크립트
2. `tasks.json` - VS Code 작업 설정
3. `keybindings.json` - 키보드 단축키 설정
4. `verilog.json` - Verilog 코드 스니펫

---

## 🔧 설치 방법

### 1단계: Python 스크립트 설치

1. `verilog_formatter_cli.py` 파일을 작업 폴더(workspace)의 루트에 복사
   ```
   C:\Users\56\Desktop\your_project\
   └── verilog_formatter_cli.py
   ```

### 2단계: VS Code Tasks 설정

1. **Ctrl + Shift + P** 눌러서 명령 팔레트 열기
2. "Tasks: Open User Tasks" 입력 후 선택
   - 또는 작업 폴더에 `.vscode` 폴더를 만들고 그 안에 `tasks.json` 생성
3. `tasks.json` 파일 내용을 붙여넣기

**중요:** `tasks.json`에서 Python 경로가 맞는지 확인!
```json
"command": "python",  // 또는 "python3" 또는 전체 경로
```

### 3단계: 키보드 단축키 설정

1. **Ctrl + Shift + P** 눌러서 명령 팔레트 열기
2. "Preferences: Open Keyboard Shortcuts (JSON)" 입력 후 선택
3. `keybindings.json` 내용을 기존 파일에 **추가** (덮어쓰지 말고 추가!)

**결과:** Verilog 파일에서 **Ctrl + Shift + F**를 누르면 자동 정리!

### 4단계: 코드 스니펫 설정

1. **Ctrl + Shift + P** 눌러서 명령 팔레트 열기
2. "Preferences: Configure User Snippets" 입력 후 선택
3. "verilog" 또는 "verilog (Verilog)" 선택
   - 만약 없다면 "New Global Snippets file..." 선택하고 "verilog" 입력
4. `verilog.json` 파일 내용을 붙여넣기

---

## 🎯 사용 방법

### 자동 정리 (Formatting)

1. Verilog 파일(`.v` 또는 `.sv`) 열기
2. **Ctrl + Shift + F** 누르기
3. 파일이 자동으로 정리됨!

### 코드 스니펫

#### 8비트 카운터 생성
1. Verilog 파일에서 `counter8` 입력
2. **Tab** 키 누르기
3. 8비트 카운터 코드가 자동 생성됨!

#### 다른 스니펫들
- `dff` + Tab → D Flip-Flop
- `vmodule` + Tab → 기본 모듈 템플릿
- `always_comb` + Tab → Combinational always 블록
- `always_seq` + Tab → Sequential always 블록

---

## 🎹 단축키 변경하기

### Ctrl+% 로 변경하고 싶다면?

**주의:** Windows에서 `Ctrl + %`는 일반적인 조합이 아닙니다. 
대신 다음과 같이 사용하세요:

1. `keybindings.json`에서 키 조합 변경:
```json
{
  "key": "ctrl+5",  // Ctrl + 5 (% 기호)
  "command": "editor.action.insertSnippet",
  "args": {
    "name": "8-bit Counter"
  },
  "when": "editorLangId == verilog"
}
```

2. 또는 더 쉬운 방법: 그냥 `counter8` 타이핑 후 Tab!

---

## ❓ 문제 해결

### 1. "python을 찾을 수 없습니다" 오류

**해결책:**
- Python이 설치되어 있는지 확인
- `tasks.json`에서 Python 전체 경로 지정:
```json
"command": "C:/Users/56/AppData/Local/Programs/Python/Python311/python.exe",
```

### 2. 작업이 실행되지 않음

**해결책:**
- `verilog_formatter_cli.py`가 작업 폴더 루트에 있는지 확인
- VS Code에서 폴더를 열었는지 확인 (파일만 열면 안됨)
- 터미널에서 직접 테스트:
```powershell
python verilog_formatter_cli.py your_file.v
```

### 3. 스니펫이 나타나지 않음

**해결책:**
- 파일 확장자가 `.v` 또는 `.sv`인지 확인
- VS Code 하단 상태바에서 언어가 "Verilog"로 설정되었는지 확인
- VS Code 재시작

### 4. 단축키가 작동하지 않음

**해결책:**
- Verilog 파일에서 시도하는지 확인
- 다른 익스텐션과 단축키 충돌 확인
- `Ctrl + K, Ctrl + S`로 키보드 단축키 설정 열어서 "Format Verilog" 검색

---

## 📝 추가 설정

### 저장 시 자동 정리 (선택사항)

`settings.json`에 추가:
```json
{
  "files.autoSave": "onFocusChange",
  "[verilog]": {
    "editor.formatOnSave": false  // 수동 포맷터 사용 시 false
  }
}
```

---

## 🎉 완료!

이제 다음 기능들을 사용할 수 있습니다:
- ✅ **Ctrl + Shift + F**: Verilog 코드 자동 정리
- ✅ **counter8 + Tab**: 8비트 카운터 생성
- ✅ **dff + Tab**: D Flip-Flop 생성
- ✅ 그 외 다양한 코드 스니펫

Happy Coding! 🚀
