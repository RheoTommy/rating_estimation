import re


def extract_str_in_main(code: str) -> str:
    cnt_main = len(re.findall(r" main *\( *\) *{", code))
    if cnt_main == 0:
        raise Exception("なんで main 関数がないんや")
    elif cnt_main > 1:
        raise Exception("main 関数が2つ以上あるだなんて，そんなアホな")
    start = re.search(r" main *\( *\) *{", code).end()
    end = start
    now = 1
    while True:
        if end == len(code):
            raise Exception("main 関数の終わりが見つからねえ！")
        ch = code[end]
        if ch == '{':
            now += 1
        elif ch == '}':
            now -= 1
        if now == 0:
            break
        end += 1
    return code[start:end]
