import re
from itertools import product

#字典库
#产品
dir_chanpin=[""]
#特殊字符
dir_teshu=["!","@","#","$","%","^","&"]
#数字/日期
dir_shuzi=[]

#模式的选择，算是主目录吧
input_mode = input("请选择您需要的模式：1.默认模式、2.自定义模式\n") or "1"
if input_mode == "1":
    #默认模式，产品从外部输入，默认符号可使用字典也可自定义。日期可填可不填，默认往前追5年
    while True:
        chanpin = input("产品名:")
        if len(chanpin)==0:
            print("请输入产品名")
        else:
            break
    teshu = input("是否使用默认特殊符号") or "y"
    shuzi_time = input("日期:/默认为往前追5年")
    def tim(shuzi_time=5):
        import time
        time=time.strftime("%Y",time.localtime())
        tim2 = []
        for i in range(shuzi_time):
            num = int(time) - i
            tim2.append(num)
        return tim2
    if teshu=="y" or teshu=="yes":
        for i in dir_teshu:
            for j in tim():
                password = chanpin+i+str(j)
                print(password)
                # with open('passwd.txt', 'a') as f:
                    # f.write(password + '\n')
    if teshu=="n" or teshu=="no":
        new_testu=input("请输入您指定的一个或多个特殊符号,以空格或逗号分割")
        new_teshu=re.split("[, ]",new_testu)
        print(new_teshu)
        for i in new_teshu:
            for j in tim():
                password = chanpin+teshu+i+str(j)
                print(password)
                # with open('passwd.txt', 'a') as f:
                    # f.write(password + '\n')

if input_mode == "2":
    def process_input(input_str):
        processed_str = input_str
        processed_str = re.sub(r'\d', '1', processed_str)
        processed_str = re.sub(r'\W', '#', processed_str)
        processed_str = re.sub(r'[a-zA-Z]', 'a', processed_str)
        char_counts = {char: processed_str.count(char) for char in set(processed_str)}
        result_str = list(processed_str)
        input_dict = {}
        for char, count in char_counts.items():
            if count > 1:
                print(f"您有{count}个同型符号{char}，请确认他们是否要同步变换")
                chang = input("同意请输入y/yes，否则n/no:")
                while True:
                    if chang in ["yes", "y"]:
                        input_dict[char] = input(f"请输入{char}位：").split(',')
                        break
                    elif chang in ["no", "n"]:
                        next_chars = [chr(ord(char) + i) for i in range(0, count + 1)]
                        found_count = 0
                        for i, c in enumerate(result_str):
                            if c == char:
                                result_str[i] = next_chars[found_count]
                                input_dict[next_chars[found_count]] = input(f"请输入第{i+1}个{next_chars[found_count]}位：").split(',')
                                found_count += 1
                        break
                    else:
                        print("请重新输入")
        return ''.join(result_str), input_dict

    input_mod = input("请输入您的模板选择：字母表示字母，数字表示数字位，特殊字符表示特殊字符位，例如vv#1#，表示两个分开的特殊字符，前面两个字母，中间一个数字位\n")
    processed_str, input_dict = process_input(input_mod)
    print("您选择的模式为", processed_str)

    # 根据处理后的字符串生成输入提示
    inputs = []
    for i, char in enumerate(processed_str):
        if char in input_dict:
            inputs.append(input_dict[char])
        elif char == 'a':
            inputs.append(input(f"请输入第{i+1}个字母位：").split(','))
        elif char == '#':
            inputs.append(input(f"请输入第{i+1}个特殊字符位：").split(','))
        elif char == '1':
            inputs.append(input(f"请输入第{i+1}个数字位：").split(','))

    # 打印所有的排列组合
    with open('passwd.txt', 'w') as f:
        print("文件在当前目录下的passwd中")
    for combination in product(*inputs):
        password = ''.join(combination)
        print(password)
        with open('passwd.txt', 'a') as f:
            f.write(password + '\n')
