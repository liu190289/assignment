from load_file import *
import time
def admin_change_question_num():
        new_question_num=int(input('please enter new question num: '))
        if new_question_num is int:
            edit_question_file(new_question_num, 'question_num.json')
            return "✅change question num success"
        else:
            return '❌only allow integer'
def admin_change_answer_time():
    answer_time=input('please enter new answer_time: ')
    if answer_time is int:
        edit_question_file(answer_time,'answer_time.json')
        return "✅change answer_time success"
    else:
        return '❌only allow integer'
def admin_change_question_time_seconds():
    question_time_seconds=input('please enter new question_time_seconds: ')
    if question_time_seconds is int:
        edit_question_file(question_time_seconds,'question_time_seconds.json')
        return "✅change question_time_seconds success"
    else:
        return '❌only allow integer'
def search_file(keyword):#搜索基础
    questions=load_question_file('question.txt')
    result=[]
    try:
        for q in questions:
            if keyword.lower() in q['question'].lower():
                result.append(q)
    except Exception as e:
        print(f'❌问题文件内没有内容{e}')
    return result
def search_file_main():#搜索主题
    keyword=input('please input keyword:')
    questions=search_file(keyword)
    search_result=[]
    if questions:
        print(f'✅成功搜索到{len(questions)}道题,分别为:')
        for q in questions:
            print(q['question'])
            for opt in q['options']:
                print(opt)
            print(q['answer'])
            time.sleep(0.5)
            search_result.append({
                'question':q['question'],
                'options':q['options'],
                'answer':q['answer']
            })
        return search_result
    else:
        print('❌对不起哦在题库中没有发现这道题')
        return None
def enter_add_question():#添加新问题(输入添加)
    questions=load_question_file('question.txt')
    q=input('please input question:')
    q= f'{str(load_file_number())}.{q}'
    repeat=False
    for q in questions:
        question_split = q['question'].split('.', 1)
        if q.lower() == question_split[1].lower():
            repeat = True
            break
    if repeat:
        print('❌你输入了一个重复的问题请重试')
        return False
    i=1
    options = []
    while i <=4:
        for letter in ['A','B','C','D']:
            opt=input(f'please input {letter}\toption:')
            opt=f'{opt}\n'
            options.append(opt.lower())
            i+=1
    answer=input('please input answer:').upper()
    if answer not in ['A','B','C','D']:
        print('you entered wrong answer')
        return False
    new_add=[
        {
            'question':q,
            'options':options,
            'answer':answer
        }
    ]
    edit_question_file_add(new_add,'question.txt')
    print("✅ 成功添加新问题")
    return True
def ask_replace_question():#询问更换哪道题目(手写)
    select_question=search_file_main()
    try:
        select_question_num=int(input(f'please input which question number you want to replace:\nif you want to replace the first question,enter 1 others is same'))
    except Exception as e:
        print(f'you enter a wrong number{e}')
    replace_question=select_question[select_question_num-1]
    r_q_s=replace_question['question']
    r_q_s=r_q_s.split('.',maxsplit=1)
    q_num=r_q_s[0]
    print(f'你选择的题目题号是{q_num}')
    return q_num
def replace_question(q_num):
    question_new=input('please input new question:')
    old_question = load_question_file('question.txt')
    q_num = int(q_num)
    old_question[q_num - 1]['question'] = f"{q_num}.{question_new}"
    edit_question_file(old_question,'qestion.txt')
    print("✅ question replaced successfully")
def replace_options(q_num):
    options = []
    i=1
    while i <=4:
        for letter in ['A', 'B', 'C', 'D']:
            opt = input(f'please input {letter}\toption:')
            opt=f'{letter}.{opt}'
            options.append(opt)
            i += 1
    q_num =int(q_num)
    old_question=load_question_file('question.txt')
    old_question[q_num-1]['options']=options
    edit_question_file(old_question,'qestion.txt')
    print("✅ question replaced successfully")
def replace_answer(q_num):
    answer = input('please input answer:').upper()
    if answer not in ['A', 'B', 'C', 'D']:
        print('you entered wrong answer')
        return False
    q_num = int(q_num)
    old_question = load_question_file('question.txt')
    old_question[q_num - 1]['answer'] = answer
    edit_question_file(old_question,'qestion.txt')
    print("✅ question replaced successfully")
    return True
def replace_all(q_num):
    question_new = input('please input new question:')
    options = []
    i = 1
    while i <= 4:
        for letter in ['A', 'B', 'C', 'D']:
            opt = input(f'please input {letter}\toption:')
            opt = f'{letter}.{opt}'
            options.append(opt)
            i += 1
    answer = input('please input answer:').upper()
    if answer not in ['A', 'B', 'C', 'D']:
        print('you entered wrong answer')
        return False
    q_num = int(q_num)
    old_question = load_question_file('question.txt')
    old_question[q_num - 1]['question'] = f"{q_num}.{question_new}"
    old_question[q_num - 1]['options'] = options
    old_question[q_num - 1]['answer'] = f"答案：{answer}"
    edit_question_file(old_question,'qestion.txt')
    print("✅ question replaced successfully")
    return True
def delete_question():
    question=load_question_file('question.txt')
    for idx in range(len(question)):
        question_select=question[idx]
        print(question_select['question'])
        time.sleep(0.5)
        idx+=5
    select_num=int(input('which question you want to delete:'))
    s = ''.join(str(i) for i in range(1, len(question) + 1))
    if str(select_num) not in s:
        print('❌you entered wrong answer')
        return False
    question.pop(select_num-1)
    edit_question_file(question,'qestion.txt')
    return True
def replace_main():
    q_num=ask_replace_question()
    print('which part you want to replace:')
    print('if you want to change question,please enter 1')
    print('if you want to change options,please enter 2')
    print('if you want to change answer,please enter 3')
    print('if you want to change all,please enter 4')
    change_answer=int(input('please input answer:'))
    if change_answer not in [1,2,3,4]:
        print('you entered wrong answer')
        return False
    if change_answer==1:
        replace_question(q_num)
        print("✅ question replaced successfully")
    if change_answer==2:
        replace_options(q_num)
        print("✅ question replaced successfully")
    if change_answer==3:
        replace_answer(q_num)
        print("✅ question replaced successfully")
    if change_answer==4:
        replace_all(q_num)
        print("✅ question replaced successfully")
    return True
def search_test_data(test_name):#搜索基础
    test_data=load_question_file('test_data.txt')
    result=[]
    try:
        for q in test_data:
            if test_name.lower() in q['test_name'].lower():
                result.append(q)
    except Exception as e:
        print(f'❌问题文件内没有内容{e}')
    print(result)
    return result
def search_test_data_main():#搜索主题
    test_name=input('please input keyword:')
    test_name_data=search_test_data(test_name)
    idx=0
    if test_name_data:
        print(f'✅成功搜索到{test_name}的数据,分别为:')
        for t in test_name_data:
            if 'question' in t:
                idx += 1
                if idx==0 or idx%11==0:
                    print(t['test_name'])
                    time.sleep(0.2)
                print(t['question'])
                time.sleep(0.2)
                print(t['options'])
                time.sleep(0.2)
                print(f'答案是{t['answer']}')
                time.sleep(0.2)
                print(f'用户作答的答案是{t['test_answer']}')
                time.sleep(1)
            if 'time_left' in t:
                print(f'{test_name}的用时是{t['time_left']}')
                time.sleep(0.2)
                print(f'{test_name}的答题时间是{t['readable']}')
                time.sleep(0.2)
                print(f'{test_name}的得分是{t['score']}')
        return True
    else:
        print('❌对不起哦在题库中没有发现这道题')
        return False
search_test_data_main()