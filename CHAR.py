# 모듈 로딩
import turtle
import random
import time
import colorsys
import platform
import os

# 기본 설정
screen = turtle.Screen()
screen.title("CHAR")

pen = turtle.Turtle()
pen.speed(0)

screen.colormode(255)

# 26가지 변수 시스템

variables = {chr(i + 97): 0 for i in range(26)}
current_var = 'a'

# 상태 변수
ascii_mode = False
show_variables = False
running = True

current_line = ""

hue = 0
thickness = 1

shape_visible = True

saved_state = None

# 색상
def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)
    return (
        int(r * 255),
        int(g * 255),
        int(b * 255)
    )

def apply_color():
    pen.pencolor(hsv_to_rgb(hue, 1, 1))

# 출력 (코드에 없으면 ? 출력)
def convert_output(value):
    global ascii_mode
    if ascii_mode:
        try:
            return chr(int(value))
        except:
            return "?"
    else:
        return str(value)

# 모든 변수 출력
def show_all_variables():
    for k, v in variables.items():
        print(f"{k} = {v}")

# 소리 출력
def play_sound():
    system = platform.system()
    try:
        # Windows
        if system == "Windows":
            import winsound
            winsound.Beep(600, 150)
            winsound.Beep(500, 150)
        # Linux/Mac
        else:
            os.system('printf "\\a"')
    except:
        print("멍멍!")

# Y 찾기
def find_matching_y(code, start_index):
    depth = 1
    for i in range(start_index + 1, len(code)):
        if code[i] in ['I', 'T', 'W']:
            depth += 1
        elif code[i] == 'Y':
            depth -= 1
            if depth == 0:
                return i
    return len(code) - 1

# 인터프리터 함수
def run(code):
    #변수지정
    global current_var
    global ascii_mode
    global running
    global current_line
    global hue
    global thickness
    global shape_visible
    global saved_state
    global show_variables

    i = 0

    loop_stack = []

    while i < len(code) and running:
        cmd = code[i]
        value = variables[current_var]

        # |: 주석지정 (코드|예시|)
        if cmd == "|":
            i += 1
            while i < len(code) and code[i] != "|":
                i += 1

        # 변수 변경
        elif 'a' <= cmd <= 'z':
            current_var = cmd
            
        # 1~0: 숫자 지정
        elif cmd.isdigit():
            variables[current_var] = int(cmd)

        # 연산
        elif cmd == "+": #+1
            variables[current_var] += 1
        elif cmd == "-": #-1
            variables[current_var] -= 1
        elif cmd == "*": # *2
            variables[current_var] *= 2
        elif cmd == "/": #/2
            variables[current_var] /= 2
        elif cmd == "%": #/2 나머지
            variables[current_var] %= 2
        elif cmd == "^": #제곱
            variables[current_var] **= 2
        elif cmd == "_": #역수
            if variables[current_var] != 0:
                variables[current_var] = 1 / variables[current_var]

        # A: 아스키-->정수 변환
        elif cmd == "A":
            ascii_mode = not ascii_mode

        # B: 소리 출력
        elif cmd == "B":
            play_sound()

        # C: 펜 색상 +10
        elif cmd == "C":
            hue = (hue + 10) % 360
            apply_color()

        # 이동
        # U/D/L/R: 상하좌우 10씩 이동
        # F: 앞으로 10씩 이동
        # G: 15도 회전
        elif cmd == "D":
            pen.sety(pen.ycor() - 10)
        elif cmd == "U":
            pen.sety(pen.ycor() + 10)
        elif cmd == "L":
            pen.setx(pen.xcor() - 10)
        elif cmd == "R":
            pen.setx(pen.xcor() + 10)
        elif cmd == "F":
            pen.forward(10)
        elif cmd == "G":
            pen.right(15)

        # E: 원래 위치로 되돌리기
        elif cmd == "E":
            if saved_state is None:
                saved_state = (
                    pen.position(),
                    pen.heading(),
                    hue,
                    thickness
                )
            else:
                pos, heading, hue, thickness = saved_state
                pen.goto(pos)

        # H: 1초 쉬기
        elif cmd == "H":
            time.sleep(1)
            
        # I: 만약 변숫값이 10인가?
        elif cmd == "I":
            if variables[current_var] != 10:
                i = find_matching_y(code, i)

        # J/P: 그리기 시작/멈춤
        elif cmd == "J":
            pen.penup()
        elif cmd == "P":
            pen.pendown()

        # K: 1~10까지 무작위 수 지정
        elif cmd == "K":
            variables[current_var] = random.randint(1, 10)

        # M: 변숫값 출력
        elif cmd == "M":
            print(convert_output(variables[current_var]), end="")

        # N: 줄바꿈
        elif cmd == "N":
            print()
            current_line = ""

        # O: 펜 초기화
        elif cmd == "O":
            if saved_state is None:
                saved_state = (
                    pen.position(),
                    pen.heading(),
                    hue,
                    thickness
                )
            else:
                pos, heading, hue, thickness = saved_state
                pen.penup()
                pen.setheading(heading)
                pen.pensize(thickness)
                apply_color()
                pen.clear()

        # Q: 정수 입력
        elif cmd == "Q":
            try:
                variables[current_var] = int(input("Input integer > "))
            except:
                variables[current_var] = 0

        # S: 펜 굵기 +1
        elif cmd == "S":
            thickness += 1
            pen.pensize(thickness)

        # T: 10번 반복하기
        elif cmd == "T":
            loop_stack.append({
                "start": i,
                "count": 10,
                "type": "repeat"
            })

        # V: 펜 보이기/숨기기
        elif cmd == "V":
            shape_visible = not shape_visible
            if shape_visible:
                pen.showturtle()
            else:
                pen.hideturtle()

        # W: 무한 반복하기
        elif cmd == "W":
            loop_stack.append({
                "start": i,
                "count": -1,
                "type": "while"
            })
            
        # X: 반복 중단하기
        elif cmd == "X":
            if loop_stack:
                i = find_matching_y(code, loop_stack[-1]["start"])
                loop_stack.pop()

        # Y: 반복/조건문 끝점
        elif cmd == "Y":
            if loop_stack:
                top = loop_stack[-1]
                if top["count"] == -1: # 무한반복
                    i = top["start"]
                else: # 일반 반복
                    top["count"] -= 1
                    if top["count"] > 0:
                        i = top["start"]
                    else:
                        loop_stack.pop()

        # Z: 강제종료
        elif cmd == "Z":
            running = False
            break

        # ?: 펜 모양 변경
        elif cmd == "?":

            current_shape = pen.shape()

            if current_shape == "turtle":
                pen.shape("classic")
            else:
                pen.shape("turtle")

        # !: 에러 발생
        elif cmd == "!":
            raise Exception("ERROR")

        # @: jwjwlove16 유튜브 홍보
        elif cmd == "@":
            print("\nhttps://www.youtube.com/@jwjwlove16\nSubscribe my YT channel plz\n")

        # $: 원-->달러
        elif cmd == "$":
            variables[current_var] *= 0.00072

        # \: 달러-->원
        elif cmd == "\\":
            variables[current_var] *= 1380

        # #: 변수 모두 출력
        elif cmd == "#":
            show_all_variables()

        # &: 소스코드 출력
        elif cmd == "&":
            print(code)
        
        i += 1

pen.penup()
pen.pencolor(hsv_to_rgb(0, 1, 1))
run(input("Input code >>> "))
screen.mainloop()
