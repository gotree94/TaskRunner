# VS Code Verilog 자동 정리 & 스니펫 설정 가이드

### 1. Verilog 익스텐션 확인
   * Ctrl + Shift + X (Extensions) → "Verilog" 검색
   * "Verilog-HDL/SystemVerilog/Bluespec SystemVerilog" (mshr-h) 익스텐션이:

설치가 되어있어야 함.

## 📦 필요한 파일들
1. `verilog_formatter_cli.py` - Python 포맷터 스크립트
2. `tasks.json` - VS Code 작업 설정
3. `keybindings.json` - 키보드 단축키 설정
4. `verilog.json` - Verilog 코드 스니펫

---

## 🔧 설치 방법

### 1단계: Python 스크립트 설치

1. `verilog_formatter_cli.py` 파일을 다음 경로에 저장
   ```
   C:\Users\Administrator\verilog_formatter\
   └── verilog_formatter_cli.py
   ```

### 2단계: VS Code Tasks 설정

1. **Ctrl + Shift + P** 눌러서 명령 팔레트 열기
2. "Tasks: Open User Tasks" 입력 후 선택
   - 또는 작업 폴더에 `.vscode` 폴더를 만들고 그 안에 `tasks.json` 생성
3. `tasks.json` 파일 내용을 붙여넣기

**중요:** Python 경로가 맞는지 확인하고, 스크립트 경로는 절대 경로로 설정되어 있습니다:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Format Verilog",
      "type": "shell",
      "command": "python",
      "args": [
        "C:/Users/Administrator/verilog_formatter/verilog_formatter_cli.py",
        "${file}"
      ],
      "presentation": {
        "reveal": "silent",
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```

```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "command": "msbuild",
            "args": [
                // Ask msbuild to generate full paths for file names.
                "/property:GenerateFullPaths=true",
                "/t:build",
                // Do not generate summary otherwise it leads to duplicate errors in Problems panel
                "/consoleloggerparameters:NoSummary"
            ],
            "group": "build",
            "presentation": {
                // Reveal the output only if unrecognized errors occur.
                "reveal": "silent"
            },
            // Use the standard MS compiler pattern to detect errors, warnings and infos
            "problemMatcher": "$msCompile"
        },
        {
            "label": "Format Verilog",
            "type": "shell",
            "command": "python",
            "args": [
                "C:/Users/Administrator/verilog_formatter/verilog_formatter_cli.py",
                "${file}"
            ],
            "presentation": {
                "reveal": "silent",
                "panel": "shared"
            },
            "problemMatcher": []
        }
    ]
}
```

이렇게 절대 경로를 사용하면 어떤 프로젝트에서도 포맷터를 사용할 수 있습니다!

### 3단계: 키보드 단축키 설정

1. **Ctrl + Shift + P** 눌러서 명령 팔레트 열기
2. "Preferences: Open Keyboard Shortcuts (JSON)" 입력 후 선택
3. `keybindings.json` 내용을 기존 파일에 **추가** (덮어쓰지 말고 추가!)

**결과:** Verilog 파일에서 **Altl + Shift + L**를 누르면 자동 정리!

```json
// Place your key bindings in this file to override the defaults
[
  {
    "key": "ctrl+shift+f",
    "command": "workbench.action.tasks.runTask",
    "args": "Format Verilog",
    "when": "editorLangId == verilog"
  }
]

```

```json
// Place your key bindings in this file to override the defaults
[
  {
    "key": "ctrl+n",
    "command": "explorer.newFile"
  },
  {
    "key": "alt+shift+l",
    "command": "workbench.action.tasks.runTask",
    "args": "Format Verilog",
    "when": "editorLangId == verilog"
  }
]

```

### 4단계: 새 스니펫 파일 생성 (추천)

1. Ctrl + Shift + P 눌러서 명령 팔레트 열기
1. "Preferences: Configure User Snippets" 입력 후 선택
1. "New Global Snippets file..." 선택
1. 파일 이름에 "verilog" 입력
1. 생성된 파일에 verilog.json 내용 붙여넣기

```json
{
  "8-bit Counter": {
    "prefix": "counter8",
    "body": [
      "module counter_8bit(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iEN,",
      "  output reg [7:0] oCount",
      ");",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn)",
      "      oCount<=8'd0;",
      "    else if (iEN)",
      "      oCount<=oCount + 1'b1;",
      "  end",
      "",
      "endmodule"
    ],
    "description": "8-bit counter with reset and enable"
  },
  "D Flip-Flop": {
    "prefix": "dff",
    "body": [
      "module d_ff(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iD,",
      "  output reg oQ",
      ");",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn)",
      "      oQ<=1'b0;",
      "    else",
      "      oQ<=iD;",
      "  end",
      "",
      "endmodule"
    ],
    "description": "D Flip-Flop with asynchronous reset"
  },
  "Module Template": {
    "prefix": "vmodule",
    "body": [
      "module ${1:module_name}(",
      "  input wire ${2:iCLK},",
      "  input wire ${3:iRSTn},",
      "  $0",
      ");",
      "",
      "  // Your code here",
      "",
      "endmodule"
    ],
    "description": "Basic Verilog module template"
  },
  "Always Block - Combinational": {
    "prefix": "always_comb",
    "body": [
      "always @(*) begin",
      "  $0",
      "end"
    ],
    "description": "Combinational always block"
  },
  "Always Block - Sequential": {
    "prefix": "always_seq",
    "body": [
      "always @(posedge ${1:iCLK} or negedge ${2:iRSTn}) begin",
      "  if (!${2:iRSTn})",
      "    $0",
      "  else",
      "    ",
      "end"
    ],
    "description": "Sequential always block with async reset"
  }
}

```

```json
{
  "8-bit Counter": {
    "prefix": "counter8",
    "body": [
      "module counter_8bit(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iEN,",
      "  output reg [7:0] oCount",
      ");",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn)",
      "      oCount<=8'd0;",
      "    else if (iEN)",
      "      oCount<=oCount + 1'b1;",
      "  end",
      "",
      "endmodule"
    ],
    "description": "8-bit counter with reset and enable"
  },
  "N-bit Counter": {
    "prefix": "countern",
    "body": [
      "module counter_${1:n}bit(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iEN,",
      "  output reg [${1:n}-1:0] oCount",
      ");",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn)",
      "      oCount<={${1:n}}'d0;",
      "    else if (iEN)",
      "      oCount<=oCount + 1'b1;",
      "  end",
      "",
      "endmodule"
    ],
    "description": "N-bit parameterized counter"
  },
  "D Flip-Flop": {
    "prefix": "dff",
    "body": [
      "module d_ff(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iD,",
      "  output reg oQ",
      ");",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn)",
      "      oQ<=1'b0;",
      "    else",
      "      oQ<=iD;",
      "  end",
      "",
      "endmodule"
    ],
    "description": "D Flip-Flop with asynchronous reset"
  },
  "T Flip-Flop": {
    "prefix": "tff",
    "body": [
      "module t_ff(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iT,",
      "  output reg oQ",
      ");",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn)",
      "      oQ<=1'b0;",
      "    else if (iT)",
      "      oQ<=~oQ;",
      "  end",
      "",
      "endmodule"
    ],
    "description": "T Flip-Flop with asynchronous reset"
  },
  "Shift Register": {
    "prefix": "shiftreg",
    "body": [
      "module shift_register #(",
      "  parameter WIDTH = 8",
      ")(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iEN,",
      "  input wire iSI,",
      "  output wire oSO,",
      "  output reg [WIDTH-1:0] oData",
      ");",
      "",
      "  assign oSO = oData[WIDTH-1];",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn)",
      "      oData<={WIDTH{1'b0}};",
      "    else if (iEN)",
      "      oData<={oData[WIDTH-2:0], iSI};",
      "  end",
      "",
      "endmodule"
    ],
    "description": "Shift register with serial in/out"
  },
  "FIFO": {
    "prefix": "fifo",
    "body": [
      "module fifo #(",
      "  parameter DATA_WIDTH = 8,",
      "  parameter DEPTH = 16",
      ")(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire iWrEn,",
      "  input wire iRdEn,",
      "  input wire [DATA_WIDTH-1:0] iWrData,",
      "  output reg [DATA_WIDTH-1:0] oRdData,",
      "  output reg oFull,",
      "  output reg oEmpty",
      ");",
      "",
      "  reg [DATA_WIDTH-1:0] memory [0:DEPTH-1];",
      "  reg [$$clog2(DEPTH)-1:0] wr_ptr, rd_ptr;",
      "  reg [$$clog2(DEPTH):0] count;",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn) begin",
      "      wr_ptr<=0;",
      "      rd_ptr<=0;",
      "      count<=0;",
      "      oFull<=0;",
      "      oEmpty<=1;",
      "    end else begin",
      "      // Write logic",
      "      if (iWrEn && !oFull) begin",
      "        memory[wr_ptr]<=iWrData;",
      "        wr_ptr<=wr_ptr + 1;",
      "      end",
      "      // Read logic",
      "      if (iRdEn && !oEmpty) begin",
      "        oRdData<=memory[rd_ptr];",
      "        rd_ptr<=rd_ptr + 1;",
      "      end",
      "      // Update count and flags",
      "      if (iWrEn && !oFull && !(iRdEn && !oEmpty))",
      "        count<=count + 1;",
      "      else if (iRdEn && !oEmpty && !(iWrEn && !oFull))",
      "        count<=count - 1;",
      "      ",
      "      oFull<=(count == DEPTH);",
      "      oEmpty<=(count == 0);",
      "    end",
      "  end",
      "",
      "endmodule"
    ],
    "description": "Synchronous FIFO buffer"
  },
  "FSM Template": {
    "prefix": "fsm",
    "body": [
      "// State definitions",
      "parameter IDLE = 2'd0,",
      "          STATE1 = 2'd1,",
      "          STATE2 = 2'd2,",
      "          STATE3 = 2'd3;",
      "",
      "reg [1:0] state, next_state;",
      "",
      "// State register",
      "always @(posedge ${1:iCLK} or negedge ${2:iRSTn}) begin",
      "  if (!${2:iRSTn})",
      "    state<=IDLE;",
      "  else",
      "    state<=next_state;",
      "end",
      "",
      "// Next state logic",
      "always @(*) begin",
      "  next_state = state;",
      "  case(state)",
      "    IDLE: begin",
      "      if (${3:condition})",
      "        next_state = STATE1;",
      "    end",
      "    STATE1: begin",
      "      next_state = STATE2;",
      "    end",
      "    STATE2: begin",
      "      next_state = STATE3;",
      "    end",
      "    STATE3: begin",
      "      next_state = IDLE;",
      "    end",
      "    default: next_state = IDLE;",
      "  endcase",
      "end",
      "",
      "// Output logic",
      "always @(*) begin",
      "  case(state)",
      "    IDLE: begin",
      "      $0",
      "    end",
      "    STATE1: begin",
      "      ",
      "    end",
      "    STATE2: begin",
      "      ",
      "    end",
      "    STATE3: begin",
      "      ",
      "    end",
      "  endcase",
      "end"
    ],
    "description": "Finite State Machine template"
  },
  "Module Template": {
    "prefix": "vmodule",
    "body": [
      "module ${1:module_name}(",
      "  input wire ${2:iCLK},",
      "  input wire ${3:iRSTn},",
      "  $0",
      ");",
      "",
      "  // Your code here",
      "",
      "endmodule"
    ],
    "description": "Basic Verilog module template"
  },
  "Testbench": {
    "prefix": "testbench",
    "body": [
      "`timescale 1ns / 1ps",
      "",
      "module tb_${1:module_name};",
      "",
      "  // Clock and reset",
      "  reg iCLK;",
      "  reg iRSTn;",
      "",
      "  // Test signals",
      "  $0",
      "",
      "  // Instantiate DUT",
      "  ${1:module_name} dut (",
      "    .iCLK(iCLK),",
      "    .iRSTn(iRSTn)",
      "  );",
      "",
      "  // Clock generation",
      "  initial begin",
      "    iCLK = 0;",
      "    forever #5 iCLK = ~iCLK;  // 100MHz clock",
      "  end",
      "",
      "  // Test sequence",
      "  initial begin",
      "    // Initialize",
      "    iRSTn = 0;",
      "    #100;",
      "    iRSTn = 1;",
      "    #100;",
      "    ",
      "    // Test cases",
      "    ",
      "    ",
      "    #1000;",
      "    $$finish;",
      "  end",
      "",
      "endmodule"
    ],
    "description": "Testbench template"
  },
  "Always Block - Combinational": {
    "prefix": "always_comb",
    "body": [
      "always @(*) begin",
      "  $0",
      "end"
    ],
    "description": "Combinational always block"
  },
  "Always Block - Sequential": {
    "prefix": "always_seq",
    "body": [
      "always @(posedge ${1:iCLK} or negedge ${2:iRSTn}) begin",
      "  if (!${2:iRSTn})",
      "    $0",
      "  else",
      "    ",
      "end"
    ],
    "description": "Sequential always block with async reset"
  },
  "Case Statement": {
    "prefix": "case",
    "body": [
      "case(${1:signal})",
      "  ${2:value1}: begin",
      "    $0",
      "  end",
      "  ${3:value2}: begin",
      "    ",
      "  end",
      "  default: begin",
      "    ",
      "  end",
      "endcase"
    ],
    "description": "Case statement template"
  },
  "For Loop": {
    "prefix": "for",
    "body": [
      "for (${1:i} = 0; ${1:i} < ${2:N}; ${1:i} = ${1:i} + 1) begin",
      "  $0",
      "end"
    ],
    "description": "For loop"
  },
  "Generate For": {
    "prefix": "genfor",
    "body": [
      "generate",
      "  genvar ${1:i};",
      "  for (${1:i} = 0; ${1:i} < ${2:N}; ${1:i} = ${1:i} + 1) begin : ${3:gen_block}",
      "    $0",
      "  end",
      "endgenerate"
    ],
    "description": "Generate for loop"
  },
  "Multiplexer 2-to-1": {
    "prefix": "mux2",
    "body": [
      "assign ${1:out} = ${2:sel} ? ${3:in1} : ${4:in0};"
    ],
    "description": "2-to-1 multiplexer"
  },
  "Multiplexer 4-to-1": {
    "prefix": "mux4",
    "body": [
      "always @(*) begin",
      "  case(${1:sel})",
      "    2'd0: ${2:out} = ${3:in0};",
      "    2'd1: ${2:out} = ${4:in1};",
      "    2'd2: ${2:out} = ${5:in2};",
      "    2'd3: ${2:out} = ${6:in3};",
      "    default: ${2:out} = ${3:in0};",
      "  endcase",
      "end"
    ],
    "description": "4-to-1 multiplexer"
  },
  "Encoder 4-to-2": {
    "prefix": "encoder",
    "body": [
      "always @(*) begin",
      "  case(${1:in})",
      "    4'b0001: ${2:out} = 2'd0;",
      "    4'b0010: ${2:out} = 2'd1;",
      "    4'b0100: ${2:out} = 2'd2;",
      "    4'b1000: ${2:out} = 2'd3;",
      "    default: ${2:out} = 2'd0;",
      "  endcase",
      "end"
    ],
    "description": "4-to-2 priority encoder"
  },
  "Decoder 2-to-4": {
    "prefix": "decoder",
    "body": [
      "always @(*) begin",
      "  ${1:out} = 4'b0000;",
      "  case(${2:in})",
      "    2'd0: ${1:out} = 4'b0001;",
      "    2'd1: ${1:out} = 4'b0010;",
      "    2'd2: ${1:out} = 4'b0100;",
      "    2'd3: ${1:out} = 4'b1000;",
      "  endcase",
      "end"
    ],
    "description": "2-to-4 decoder"
  },
  "Clock Divider": {
    "prefix": "clkdiv",
    "body": [
      "module clock_divider #(",
      "  parameter DIV_RATIO = ${1:100}",
      ")(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  output reg oCLK_DIV",
      ");",
      "",
      "  reg [31:0] counter;",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn) begin",
      "      counter<=0;",
      "      oCLK_DIV<=0;",
      "    end else begin",
      "      if (counter >= DIV_RATIO/2 - 1) begin",
      "        counter<=0;",
      "        oCLK_DIV<=~oCLK_DIV;",
      "      end else begin",
      "        counter<=counter + 1;",
      "      end",
      "    end",
      "  end",
      "",
      "endmodule"
    ],
    "description": "Clock divider module"
  },
  "Edge Detector": {
    "prefix": "edge",
    "body": [
      "reg ${1:signal}_d;",
      "wire ${1:signal}_posedge = ${1:signal} & ~${1:signal}_d;",
      "wire ${1:signal}_negedge = ~${1:signal} & ${1:signal}_d;",
      "",
      "always @(posedge ${2:iCLK} or negedge ${3:iRSTn}) begin",
      "  if (!${3:iRSTn})",
      "    ${1:signal}_d<=1'b0;",
      "  else",
      "    ${1:signal}_d<=${1:signal};",
      "end"
    ],
    "description": "Rising/Falling edge detector"
  },
  "Synchronizer": {
    "prefix": "sync",
    "body": [
      "reg ${1:signal}_sync1, ${1:signal}_sync2;",
      "",
      "always @(posedge ${2:iCLK} or negedge ${3:iRSTn}) begin",
      "  if (!${3:iRSTn}) begin",
      "    ${1:signal}_sync1<=1'b0;",
      "    ${1:signal}_sync2<=1'b0;",
      "  end else begin",
      "    ${1:signal}_sync1<=${1:signal};",
      "    ${1:signal}_sync2<=${1:signal}_sync1;",
      "  end",
      "end"
    ],
    "description": "Two-stage synchronizer"
  },
  "PWM Generator": {
    "prefix": "pwm",
    "body": [
      "module pwm_generator #(",
      "  parameter WIDTH = 8",
      ")(",
      "  input wire iCLK,",
      "  input wire iRSTn,",
      "  input wire [WIDTH-1:0] iDuty,",
      "  output reg oPWM",
      ");",
      "",
      "  reg [WIDTH-1:0] counter;",
      "",
      "  always @(posedge iCLK or negedge iRSTn) begin",
      "    if (!iRSTn) begin",
      "      counter<=0;",
      "      oPWM<=0;",
      "    end else begin",
      "      counter<=counter + 1;",
      "      oPWM<=(counter < iDuty);",
      "    end",
      "  end",
      "",
      "endmodule"
    ],
    "description": "PWM signal generator"
  }
}
```


### 5단계: 코드 스니펫 설정

1. **Ctrl + Shift + P** 눌러서 명령 팔레트 열기
2. "Preferences: Configure User Snippets" 입력 후 선택
3. "verilog" 또는 "verilog (Verilog)" 선택
   - 만약 없다면 "New Global Snippets file..." 선택하고 "verilog" 입력
4. `verilog.json` 파일 내용을 붙여넣기


3. VS Code에서 테스트

VS Code에서 test.v 파일 열기
Ctrl + Shift + P → "Tasks: Run Task" → "Format Verilog" 선택
또는 Altl + Shift + L 누르기
---

## 🎯 사용 방법

### 자동 정리 (Formatting)

1. Verilog 파일(`.v` 또는 `.sv`) 열기
2. **Altl + Shift + L** 누르기
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
"command": "C:/Python311/python.exe",  // 또는 실제 Python 설치 경로
```

### 2. 작업이 실행되지 않음

**해결책:**
- `verilog_formatter_cli.py`가 `C:\Users\Administrator\verilog_formatter\` 경로에 있는지 확인
- 터미널에서 직접 테스트:
```powershell
python C:\Users\Administrator\verilog_formatter\verilog_formatter_cli.py your_file.v
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

## 📥 설치 방법 (간단 요약)

1. `C:\Users\Administrator\verilog_formatter\` 폴더 생성
2. `verilog_formatter_cli.py` 파일을 해당 폴더에 저장
3. VS Code에서:
   - 아무 프로젝트나 열기
   - **Ctrl+Shift+P** → "Tasks: Open User Tasks" → `tasks.json` 내용 붙여넣기
   - **Ctrl+Shift+P** → "Keyboard Shortcuts (JSON)" → `keybindings.json` 내용 추가
   - **Ctrl+Shift+P** → "Configure User Snippets" → "verilog" → `verilog.json` 내용 붙여넣기

자세한 설치 방법은 위의 단계별 가이드를 참고하세요!

---

## 🎉 완료!

이제 다음 기능들을 사용할 수 있습니다:
- ✅ **Altl + Shift + L**: Verilog 코드 자동 정리
- ✅ **counter8 + Tab**: 8비트 카운터 생성
- ✅ **dff + Tab**: D Flip-Flop 생성
- ✅ 그 외 다양한 코드 스니펫

## 📋 사용 가능한 모든 Verilog 스니펫

1. counter8 + Tab
```verilog
verilogmodule counter_8bit(
  input wire iCLK,
  input wire iRSTn,
  input wire iEN,
  output reg [7:0] oCount
);

  always @(posedge iCLK or negedge iRSTn) begin
    if (!iRSTn)
      oCount<=8'd0;
    else if (iEN)
      oCount<=oCount + 1'b1;
  end
endmodule
```
설명: 8비트 카운터 (리셋 및 인에이블 포함)

2. dff + Tab
```verilog
verilogmodule d_ff(
  input wire iCLK,
  input wire iRSTn,
  input wire iD,
  output reg oQ
);

  always @(posedge iCLK or negedge iRSTn) begin
    if (!iRSTn)
      oQ<=1'b0;
    else
      oQ<=iD;
  end

endmodule
```
설명: D 플립플롭 (비동기 리셋)

3. vmodule + Tab
```verilog
verilogmodule module_name(
  input wire iCLK,
  input wire iRSTn,
  
);

  // Your code here

endmodule
```
설명: 기본 모듈 템플릿 (커서가 자동으로 이동하며 이름 수정 가능)

4. always_comb + Tab
```verilog
verilogalways @(*) begin
  
end
```
설명: 조합 논리(Combinational) always 블록

5. always_seq + Tab
```verilog
verilogalways @(posedge iCLK or negedge iRSTn) begin
  if (!iRSTn)
    
  else
    
end
```
## 스니펫 목록
1. 🔢 카운터 & 레지스터
   * counter8 - 8비트 카운터
   * countern - N비트 파라미터화 카운터 (비트 수 조정 가능)
   * shiftreg - 시프트 레지스터

2. 🔄 플립플롭
   * dff - D 플립플롭
   * tff - T 플립플롭

3. 📦 메모리 & 버퍼
   * fifo - 동기식 FIFO 버퍼 (완전한 구현)

4. 🎯 상태 머신
   * fsm - 유한 상태 머신 템플릿 (3 always 블록)

5. 🏗️ 기본 구조
   * vmodule - 모듈 템플릿
   * testbench - 테스트벤치 템플릿 (클럭 생성 포함)

6. 🔁 제어 구조
   * always_comb - 조합 논리 블록
   * always_seq - 순차 논리 블록
   * case - Case 문
   * for - For 루프
   * genfor - Generate for 루프

7. 🔌 조합 논리
   * mux2 - 2-to-1 멀티플렉서
   * mux4 - 4-to-1 멀티플렉서
   * encoder - 4-to-2 인코더
   * decoder - 2-to-4 디코더

8. ⚡ 유틸리티
   * clkdiv - 클럭 분주기
   * edge - 엣지 검출기 (rising/falling)
   * sync - 2단 동기화기 (CDC 처리)
   * pwm - PWM 신호 생성기

### 🎯 사용 예시

```
verilog// fsm + Tab
parameter IDLE = 2'd0,
          STATE1 = 2'd1,
          STATE2 = 2'd2,
          STATE3 = 2'd3;
...

// fifo + Tab
module fifo #(
  parameter DATA_WIDTH = 8,
  parameter DEPTH = 16
)(
  ...
);

// testbench + Tab
`timescale 1ns / 1ps
module tb_module_name;
  ...
```

