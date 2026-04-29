import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MarsCalculator(QWidget):
    def __init__(self):
        super().__init__()
        # 데이터 관리 변수
        self.current_expression = '0'  # 계산 로직용 
        self.is_calculation_complete = False 
        
        self.initialize_ui()

    def initialize_ui(self):
        '''UI 생성 후 배치'''
        self.setWindowTitle('Mars Mission Calculator')
        self.setFixedSize(320, 500)
        self.setStyleSheet('background-color: #000000;')

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 20, 10, 10)
        self.main_layout.setSpacing(10)

        # 결과창(Display)
        self.display_screen = QLineEdit('0')
        self.display_screen.setReadOnly(True)
        self.display_screen.setFixedHeight(100)
        self.display_screen.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display_screen.setStyleSheet('color: white; border: none; background: transparent;')
        
        self.main_layout.addWidget(self.display_screen)

        # 버튼 그리드
        self.grid_area = QGridLayout()
        self.grid_area.setSpacing(10)
        self.create_buttons()
        
        self.main_layout.addLayout(self.grid_area)
        self.setLayout(self.main_layout)
        self.refresh_display() # 초기 화면 업데이트

    def create_buttons(self):
        '''버튼 좌표 및 디자인 설정'''
        buttons = [
            ('AC', 0, 0, '#A5A5A5', 'black'), ('+/-', 0, 1, '#A5A5A5', 'black'), 
            ('%', 0, 2, '#A5A5A5', 'black'), ('/', 0, 3, '#FF9F0A', 'white'),
            ('7', 1, 0, '#333333', 'white'), ('8', 1, 1, '#333333', 'white'), 
            ('9', 1, 2, '#333333', 'white'), ('*', 1, 3, '#FF9F0A', 'white'),
            ('4', 2, 0, '#333333', 'white'), ('5', 2, 1, '#333333', 'white'), 
            ('6', 2, 2, '#333333', 'white'), ('-', 2, 3, '#FF9F0A', 'white'),
            ('1', 3, 0, '#333333', 'white'), ('2', 3, 1, '#333333', 'white'), 
            ('3', 3, 2, '#333333', 'white'), ('+', 3, 3, '#FF9F0A', 'white'),
            ('0', 4, 0, '#333333', 'white'), ('.', 4, 2, '#333333', 'white'), 
            ('=', 4, 3, '#FF9F0A', 'white')
        ]

        for text, r, c, bg, fg in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont('Arial', 18))
            style = f'background-color: {bg}; color: {fg}; border-radius: 30px;'
            
            if text == '0':
                btn.setFixedSize(145, 65)
                btn.setStyleSheet(style + 'text-align: left; padding-left: 25px;')
                self.grid_area.addWidget(btn, r, c, 1, 2)
            else:
                btn.setFixedSize(65, 65)
                btn.setStyleSheet(style)
                self.grid_area.addWidget(btn, r, c)
            
            btn.clicked.connect(self.press_event)

    def refresh_display(self):
        '''천 단위 콤마 적용 및 폰트 크기 자동 조절'''
        raw_text = self.current_expression
        
        # 1. 천 단위 콤마 포맷팅 로직
        try:
            # 연산자 없이 숫자만 있는 경우에만 콤마 적용
            if any(op in raw_text for op in ['+', '-', '*', '/']) and not raw_text.startswith('-'):
                display_text = raw_text # 수식일 때는 그대로 표시
            else:
                num = float(raw_text)
                if num == int(num): # 정수인 경우
                    display_text = "{:,}".format(int(num))
                else: # 소수인 경우
                    parts = str(num).split('.')
                    display_text = "{:,}.{}".format(int(parts[0]), parts[1])
        except:
            display_text = raw_text

        # 2. 보너스 과제: 글자 길이에 따른 폰트 크기 조정
        length = len(display_text)
        if length > 12: font_size = 22
        elif length > 8: font_size = 30
        else: font_size = 45

        self.display_screen.setFont(QFont('Arial', font_size))
        self.display_screen.setText(display_text)

    def press_event(self):
        '''버튼 클릭 핸들러'''
        btn_text = self.sender().text()

        if btn_text == 'AC':
            self.current_expression = '0'
            self.is_calculation_complete = False
        elif btn_text == '+/-':
            try:
                val = float(self.current_expression)
                self.current_expression = str(val * -1)
            except: pass
        elif btn_text == '%':
            try:
                val = float(self.current_expression)
                self.current_expression = str(val / 100)
            except: pass
        elif btn_text == '=':
            self.equal()
        elif btn_text == '.':
            # 소수점 중복 입력 방지
            last_part = self.current_expression.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').split()[-1]
            if '.' not in last_part:
                self.current_expression += '.'
        else:
            # 숫자 및 연산자 입력
            if self.current_expression == '0' or self.is_calculation_complete:
                if btn_text.isdigit():
                    self.current_expression = btn_text
                else:
                    self.current_expression += btn_text
                self.is_calculation_complete = False
            else:
                self.current_expression += btn_text
            
        self.refresh_display()

    def equal(self):
        '''최종 계산 및 예외 처리'''
        try:
            # 수식 계산
            result = eval(self.current_expression)
            
            # 보너스 과제: 소수점 6자리 반올림
            if isinstance(result, float):
                result = round(result, 6)
            
            self.current_expression = str(result)
            self.is_calculation_complete = True
        except ZeroDivisionError:
            self.current_expression = 'Error'
        except:
            self.current_expression = 'Error'
        
        self.refresh_display()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = MarsCalculator()
    calc.show()
    sys.exit(app.exec())