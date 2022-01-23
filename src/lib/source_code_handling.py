import re


def exclude_comments(code: str) -> str:
    sz = len(code)
    res = ""
    it = 0
    while it < sz:
        if it < sz - 1 and code[it:it + 2] == "//":
            next_it = sz
            for j in range(it + 2, sz):
                if code[j] == '\n' or code[j] == '\r':
                    next_it = j + 1
                    break
            it = next_it
        elif it < sz - 1 and code[it:it + 2] == "/*":
            next_it = -1
            for j in range(it + 2, sz - 1):
                if code[j:j + 2] == "*/":
                    next_it = j + 2
                    break
            if next_it == -1:
                raise Exception("コメントの終わりはどこ...?")
            it = next_it
        else:
            res += code[it]
            it += 1
    return res


def extract_str_in_main(code: str) -> str:
    pattern = r"\bmain\b[ \r\n]*\(.*?\)[ \r\n]*{"
    cnt_main = len(re.findall(pattern, code))
    if cnt_main == 0:
        raise Exception("なんで main 関数がないんや")
    elif cnt_main > 1:
        raise Exception("main 関数が2つ以上あるだなんて，そんなアホな")
    start = re.search(pattern, code).end()
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
