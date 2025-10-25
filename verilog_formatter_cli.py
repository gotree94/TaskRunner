#!/usr/bin/env python3
import sys
import re
import os

class VerilogFormatter:
    def __init__(self):
        self.indent_level = 0
        self.indent_size = 2
    
    def format_verilog(self, code):
        """Verilog 코드를 포맷팅합니다."""
        code = code.strip()
        
        # 한 줄에 여러 문장이 있는 경우 분리
        code = self._split_multiple_statements(code)
        
        lines = code.split('\n')
        formatted_lines = []
        self.indent_level = 0
        prev_line_type = None
        in_case_block = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # case 블록 추적
            if re.search(r'\bcase\b', line):
                in_case_block = True
            elif re.search(r'\bendcase\b', line):
                in_case_block = False
            
            current_line_type = self._get_line_type(line)
            
            if self._should_add_blank_line(prev_line_type, current_line_type):
                formatted_lines.append('')
            
            # case 레이블은 들여쓰기를 한 단계 덜 함
            is_case_label = in_case_block and self._is_case_label(line)
            
            if self._should_decrease_indent_before(line):
                self.indent_level = max(0, self.indent_level - 1)
            
            # 들여쓰기 적용 (case 레이블은 1단계 감소)
            if is_case_label:
                indent = max(0, self.indent_level - 1)
            else:
                indent = self.indent_level
            
            formatted_line = ' ' * (indent * self.indent_size) + line
            formatted_line = self._clean_spacing(formatted_line)
            formatted_lines.append(formatted_line)
            
            if self._should_increase_indent(line):
                self.indent_level += 1
            
            if self._should_decrease_indent_after(line):
                self.indent_level = max(0, self.indent_level - 1)
            
            prev_line_type = current_line_type
        
        return '\n'.join(formatted_lines)
    
    def _split_multiple_statements(self, code):
        """한 줄에 여러 문장이 있는 경우 분리"""
        lines = code.split('\n')
        new_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # begin, end가 같은 줄에 있는 경우 분리
            if 'begin' in line and not line.strip().endswith('begin'):
                # "begin" 이후의 내용을 다음 줄로
                match = re.search(r'(.*?\bbegin\b)\s*(.*)', line)
                if match and match.group(2).strip():
                    new_lines.append(match.group(1))
                    remaining = match.group(2).strip()
                    # remaining에 end가 있으면 다시 분리
                    if 'end' in remaining and not remaining.strip().startswith('end'):
                        parts = re.split(r'(\bend\b)', remaining)
                        for part in parts:
                            if part.strip():
                                new_lines.append(part.strip())
                    else:
                        new_lines.append(remaining)
                else:
                    new_lines.append(line)
            # end가 다른 코드와 같은 줄에 있는 경우
            elif re.search(r'\S+\s*\bend\b', line) and not line.strip().startswith('end'):
                # end 앞의 내용과 end를 분리
                parts = re.split(r'(\bend\b)', line)
                for part in parts:
                    if part.strip() and part.strip() != 'end':
                        new_lines.append(part.strip())
                    elif part.strip() == 'end':
                        new_lines.append('end')
            # 세미콜론으로 구분된 여러 문장 처리 (output reg 같은 특수 케이스 제외)
            elif ';' in line:
                # output reg oBusy; 같은 선언문은 분리하지 않음
                if re.match(r'^\s*(input|output|inout|wire|reg|parameter|localparam)\s', line):
                    new_lines.append(line)
                else:
                    # 할당문들이 세미콜론으로 연결된 경우 분리
                    parts = line.split(';')
                    for part in parts:
                        part = part.strip()
                        if part and not part.endswith(';'):
                            new_lines.append(part + ';')
                        elif part:
                            new_lines.append(part)
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _should_increase_indent(self, line):
        """들여쓰기를 증가시켜야 하는지 확인"""
        increase_keywords = [
            r'\bmodule\b', r'\bbegin\b', r'\bcase\b', r'\bcasex\b', r'\bcasez\b',
            r'\bfunction\b', r'\btask\b', r'\bfork\b', r'\bgenerate\b'
        ]
        for keyword in increase_keywords:
            if re.search(keyword, line):
                return True
        return False
    
    def _should_decrease_indent_before(self, line):
        """줄 시작 전에 들여쓰기를 감소시켜야 하는지 확인"""
        decrease_keywords = [
            r'^\s*\bend\b', r'^\s*\bendcase\b', r'^\s*\bendmodule\b', 
            r'^\s*\bendfunction\b', r'^\s*\bendtask\b', r'^\s*\bjoin\b', 
            r'^\s*\bendgenerate\b'
        ]
        for keyword in decrease_keywords:
            if re.search(keyword, line):
                return True
        return False
    
    def _should_decrease_indent_after(self, line):
        """줄 끝에서 들여쓰기를 감소시켜야 하는지 확인"""
        if re.search(r'\bbegin\b', line) and re.search(r'\bend\b', line):
            return True
        return False
    
    def _is_case_label(self, line):
        """case 문의 레이블인지 확인 (IDLE:, START:, default: 등)"""
        # case 레이블 패턴: 단어:begin 또는 단어:if 또는 default:
        if re.match(r'^\s*\w+\s*:', line):
            return True
        if re.match(r'^\s*default\s*:', line):
            return True
        if re.match(r'^\s*\d+\'[bdh]\w+\s*:', line):  # 4'b0000: 같은 패턴
            return True
        return False
    
    def _get_line_type(self, line):
        """라인의 타입을 판단"""
        if re.search(r'\bmodule\b', line):
            return 'module'
        elif re.search(r'\b(input|output|inout)\b', line):
            return 'port'
        elif re.search(r'\bparameter\b', line):
            return 'parameter'
        elif re.search(r'\blocalparam\b', line):
            return 'localparam'
        elif re.search(r'\b(wire|reg|integer)\b', line):
            return 'declaration'
        elif re.search(r'\bassign\b', line):
            return 'assign'
        elif re.search(r'\b(always|initial)\b', line):
            return 'always'
        elif re.search(r'\bendmodule\b', line):
            return 'endmodule'
        else:
            return 'other'
    
    def _should_add_blank_line(self, prev_type, current_type):
        """빈 줄을 추가해야 하는지 판단"""
        if prev_type is None:
            return False
        
        # parameter가 끝나고 localparam이 오면 빈 줄
        if prev_type == 'parameter' and current_type == 'localparam':
            return True
        
        # localparam이 끝나고 다른 타입이 오면 빈 줄
        if prev_type == 'localparam' and current_type != 'localparam':
            return True
        
        # port 선언 뒤에 parameter가 오면 빈 줄
        if prev_type == 'port' and current_type == 'parameter':
            return True
        
        # parameter가 끝나고 declaration이 오면 빈 줄
        if prev_type == 'parameter' and current_type == 'declaration':
            return True
        
        # port 선언 뒤에 declaration이 오면 빈 줄
        if prev_type == 'port' and current_type == 'declaration':
            return True
        
        # declaration 뒤에 assign이 오면 빈 줄
        if prev_type == 'declaration' and current_type == 'assign':
            return True
        
        # assign 뒤에 always가 오면 빈 줄
        if prev_type == 'assign' and current_type == 'always':
            return True
        
        # always 블록 뒤에 always가 또 오면 빈 줄
        if prev_type == 'always' and current_type == 'always':
            return True
        
        # always 블록 뒤에 endmodule이 오면 빈 줄
        if prev_type != 'endmodule' and current_type == 'endmodule':
            return True
        
        return False
    
    def _clean_spacing(self, line):
        """키워드와 연산자 주변의 공백을 정리"""
        indent_match = re.match(r'^(\s*)', line)
        indent = indent_match.group(1) if indent_match else ''
        code = line[len(indent):]
        
        # <= 연산자는 붙여쓰기
        code = re.sub(r'\s*<\s*=\s*', '<=', code)
        
        # >= 연산자는 양쪽 공백 (먼저 처리하여 > = 같은 분리된 경우 처리)
        code = re.sub(r'\s*>\s*=\s*', '>=', code)
        code = re.sub(r'>=', ' >= ', code)
        
        # 다른 비교 연산자들은 공백 추가
        code = re.sub(r'\s*==\s*', ' == ', code)
        code = re.sub(r'\s*!=\s*', ' != ', code)
        
        # = 연산자 (단, <=, >=, ==, != 제외)
        code = re.sub(r'(?<![<>=!])\s*=\s*(?!=)', ' = ', code)
        
        # 쉼표 뒤 공백
        code = re.sub(r',\s*', ', ', code)
        
        # 괄호 안쪽 공백 처리
        code = re.sub(r'\(\s+', '(', code)
        code = re.sub(r'\s+\)', ')', code)
        
        # 세미콜론 앞 공백 제거
        code = re.sub(r'\s+;', ';', code)
        
        # if, else 뒤에 공백 확보
        code = re.sub(r'\bif\s*\(', 'if (', code)
        code = re.sub(r'\belse\s+if\s*\(', 'else if (', code)
        code = re.sub(r'\belse\s+', 'else ', code)
        
        # for 문 공백
        code = re.sub(r'\bfor\s*\(', 'for (', code)
        
        # 키워드 뒤 공백 확보
        keywords = ['input', 'output', 'inout', 'wire', 'reg', 'module', 
                   'endmodule', 'assign', 'parameter', 'localparam', 'integer']
        for keyword in keywords:
            code = re.sub(rf'\b{keyword}\b\s+', f'{keyword} ', code)
            code = re.sub(rf'\b{keyword}\b(?=\S)', f'{keyword} ', code)
        
        return indent + code


def main():
    if len(sys.argv) < 2:
        print("Usage: python verilog_formatter_cli.py <verilog_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)
    
    # 파일 읽기
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # 포맷팅
    formatter = VerilogFormatter()
    try:
        formatted_code = formatter.format_verilog(code)
    except Exception as e:
        print(f"Error formatting code: {e}")
        sys.exit(1)
    
    # 파일 쓰기 (원본 파일 덮어쓰기)
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(formatted_code)
        print(f"Successfully formatted: {input_file}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()