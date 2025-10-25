# TaskRunner

## 1. CLI 버전 Python 스크립트

```py
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
        lines = code.split('\n')
        formatted_lines = []
        self.indent_level = 0
        prev_line_type = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            current_line_type = self._get_line_type(line)
            
            if self._should_add_blank_line(prev_line_type, current_line_type):
                formatted_lines.append('')
            
            if self._should_decrease_indent_before(line):
                self.indent_level = max(0, self.indent_level - 1)
            
            formatted_line = ' ' * (self.indent_level * self.indent_size) + line
            formatted_line = self._clean_spacing(formatted_line)
            formatted_lines.append(formatted_line)
            
            if self._should_increase_indent(line):
                self.indent_level += 1
            
            if self._should_decrease_indent_after(line):
                self.indent_level = max(0, self.indent_level - 1)
            
            prev_line_type = current_line_type
        
        return '\n'.join(formatted_lines)
    
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
            r'\bend\b', r'\bendcase\b', r'\bendmodule\b', r'\bendfunction\b',
            r'\bendtask\b', r'\bjoin\b', r'\bendgenerate\b'
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
    
    def _get_line_type(self, line):
        """라인의 타입을 판단"""
        if re.search(r'\bmodule\b', line):
            return 'module'
        elif re.search(r'\b(input|output|inout)\b', line):
            return 'port'
        elif re.search(r'\b(wire|reg|integer|parameter)\b', line):
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
        
        if prev_type == 'port' and current_type == 'declaration':
            return True
        if prev_type == 'declaration' and current_type == 'assign':
            return True
        if prev_type == 'assign' and current_type == 'always':
            return True
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
        
        # 다른 연산자들은 공백 추가
        code = re.sub(r'\s*==\s*', ' == ', code)
        code = re.sub(r'\s*!=\s*', ' != ', code)
        code = re.sub(r'(?<!<)\s*=\s*(?!=)', ' = ', code)
        
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
        
        # 키워드 뒤 공백 확보
        keywords = ['input', 'output', 'inout', 'wire', 'reg', 'module', 'endmodule', 'assign']
        for keyword in keywords:
            code = re.sub(rf'\b{keyword}\b\s*', f'{keyword} ', code)
        
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
```



