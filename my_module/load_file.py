import time
import json


def load_file_number():#加载问题数量的函数
    try:
        file_num=len(load_question_file('question.txt'))
        return file_num
    except Exception as e:
        print('文件内没有内容')
        return 0
def check_question_part(question_check):
    try:
        question_check = question_check.split('.')
    except Exception as e:
        print(f'❌文件格式不对{e}')
        return False
    try:
        question_check_num = int(question_check[0])
        if question_check_num < 1:
            print('❌文档问题中的数字不对')
            return False
    except Exception as e:
        print(f'未找到数字{e}')
        return False
    return True
def check_options_part(options):
    for option in options:
        try:
            option = option.split('.')
        except Exception as e:
            print(f'❌文件格式不对{e}')
            return False
        if option[0] not in ['A', 'B', 'C', 'D']:
            print(option[0])
            print(f'❌你的格式不对')
            return False
    return True
def check_answer_part(answer):
    try:
        answer = answer.replace('：',':')
        answer_check = answer.split(':')
        print(answer_check)
    except Exception as e:
        print(f'❌文件格式不对{e}')
        return False
    if answer_check[0] not in ['correct_answer', '答案']:
        print(answer_check[0])
        print(f'❌你的格式不对')
        return False
    return True
def load_file_main():#添加问题(文件形式)
    try:
        file_name = input('please input file name:')
        file = open(f'../question file/{file_name}', 'r', encoding='utf-8')
        file.flush()
    except Exception as e:
        print('你输入了一个错误的文件名或者文件名位置不对')
        print(e)
        return False#尝试输入和对错误的纠正
    f_num=load_file_number()
    lines=[]
    add_success = 0
    add_fail = 0
    test_question=[]
    idx=0#指针位置
    for line in file:
        line=line.strip('\n')
        lines.append(line)#处理原文档中的空格和空行
    if f_num > 0:
        questions = load_question_file('question.txt')
    while idx < len(lines):
        #question的处理
        if f_num >0:
            parts=lines[idx].split('.',1)
            repeat = False
            for q in questions:
                question_split=q['question'].split('.',1)
                if parts[1].lower() == question_split[1].lower():
                    repeat = True
                    break
            if repeat:
                print('❌问题在文件中已经存在')
                idx += 6
                add_fail+= 1
                continue
            parts[0]=str(f_num+1)
            question='.'.join(parts)
            f_num += 1

        else:
            question=lines[idx]
        if not check_question_part(question):
            return False
        idx+=1
        #options的处理
        options=lines[idx:idx+4]
        if not check_options_part(options):
            return False
        idx+=4
        #answer的处理
        answer=lines[idx]
        answer = answer.replace('：', ':')
        if not check_answer_part(answer):
            return False
        idx+=1
        add_success += 1
        test_question.append({
            'question':question,
            'options':options,
            'answer':answer
        })
    file.close()
    edit_question_file_add(test_question,'question.txt')
    print(f"✅ 成功添加进入{add_success}道题目\n❌添加失败{add_fail}道题目")
    return True
def file_clear():#清除文件内容
    try:
        file_name = input('please input file name:')
        file = open(f'../question file/{file_name}', 'w', encoding='utf-8')
        pass
        file.close()
    except Exception as e:
        print('❌你输入了错误的文件名或者文件位置错误')
        print(e)
    print("✅ 成功清空文件")
def load_question_file(file_name):#加载文件变量名是文件名字
    try:
        with open(f'../question file/{file_name}', 'r',encoding='utf-8')as f:
            print("✅ 成功打开文件")
            question=json.load(f)
            return question
    except Exception as e:
        print('❌题库文件不存在或者格式不对或内容为空',e)
        return False
def edit_question_file(question,file_name):#将旧内容进行覆盖
    """

    :param question:你新添加的问题变量名称
    :return: None
    """
    try:# 先确保题库文件存在且是合法 JSON
         f=open(f'../question file/{file_name}', 'w', encoding='utf-8')
    except Exception as e:
        print(f'❌找不到文件{e}')
        return False
    json.dump(question, f, ensure_ascii=False, indent=2)
    print("✅ 成功覆盖文件")
    return True
def edit_question_file_add(new_question,file_name):#将新内容添加到就内容并进行合并覆盖
    """
    :param new_question:你新添加的问题变量名称
    :return: None
    """
    path = f'../question file/{file_name}'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            old = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        old = []  # 文件为空或损坏时兜底

    old.extend(new_question)  # 内存里合并

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(old, f, ensure_ascii=False, indent=2)  # 一次性覆盖
    print("✅ 成功覆盖文件")
    return
if __name__ == '__main__':
    load_file_main()