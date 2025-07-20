import sys
import select
from load_file import *
from utils import *
import random
import threading
stop_evt = threading.Event()#创建红绿灯
out_q=queue.Queue()# 创建“邮箱”
question_num=int(load_question_file('question_num.json'))#题目数量
def choose_question(question_num):
    question=load_question_file('question.txt')
    question_choose=random.sample(question,question_num)#从question中抽取question_num个问题
    return question_choose
'''def input_listener(stop_evt,input_q,answer_time):#macos不知能否使用windows无法使用
    while not stop_evt.is_set():
        start_time=time.time()
        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
            user_input = sys.stdin.readline().strip().upper()
            print(f'your type{user_input}')
            input_q.put(user_input)
            return
        if time.time()-start_time>answer_time:
            print('time over')
            input_q.put(None)
            return'''
def enter_answer(answer_time):
    start_time = time.time()
    while not stop_evt.is_set():
        user_input=input('please input your answer:')
        return user_input.strip().upper()
    if start_time-answer_time>answer_time:
        print('time over')
        return None
    return False
def score_judgment(score):
    if 90<=score<100:
        return 'A'
    elif 70<=score<90:
        return 'B'
    elif 50<=score<69:
        return 'C'
    else:
        return 'D\tyou need to work hard'
def test_main():
    answer_time = int(load_question_file('answer_time.json'))#回答时间
    correct_answer_num=0
    wrong_answer_num=0
    number_of_questions_skipped=0
    question_time_seconds=int(load_question_file('question_time_seconds.json'))#问题总时间
    print('welcome to the test')
    print('You have ten minutes to take this test.\n There are 10 multiple-choice questions in total.\n You have 90 seconds to answer each question\nPlease enter your selected options A, B, C, D respectively.\nIf you want to skip just enter s')
    test_name=input("enter test name")
    test_data=[]
    test_question_choose=choose_question(question_num)
    idx=0
    countdown_thread = threading.Thread(target=countdown, args=(question_time_seconds, stop_evt, out_q))
    countdown_thread.daemon = True
    while idx < len(test_question_choose):
        question=test_question_choose[idx]['question']
        options=test_question_choose[idx]['options']
        answer=test_question_choose[idx]['answer']
        answer=answer.strip().upper()
        answer=answer.split(':')
        answer=answer[1]
        idx+=1
        user_answer='empty'
        if idx==1:
            countdown_thread.start()
        if not stop_evt.is_set():
            print(question)
            for opt in options:
                print(opt)
        enter_result=enter_answer(answer_time) #input_listener_thread=threading.Thread(target=input_listener,args=(stop_evt,input_q,answer_time))
        #input_listener_thread.daemon=True
        #input_listener_thread.start()#???也许macos可用
        if enter_result is not None:
            if enter_result == answer:
                user_answer=enter_result
                print('✅correct')
                correct_answer_num+=1
            elif enter_result =='S':
                print('You skipped this question')
                number_of_questions_skipped+=1
            else:
                user_answer = enter_result
                print(f'❌wrong answer\ncorrect answer:{answer}')
                wrong_answer_num+=1
        test_data.append({
            'test_name': test_name,
            'question':question,
            'answer':answer,
            'test_answer':user_answer,
        })
    if wrong_answer_num+correct_answer_num<question_num:
        number_of_questions_skipped=question_num-correct_answer_num
    stop_evt.set()#停止字进程
    countdown_thread.join()#等子进程停止
    time_left = out_q.get()#拿取时间
    time_min_use = int((question_time_seconds-time_left) / 60)
    time_sec_use = int((question_time_seconds-time_left) % 60)
    score = correct_answer_num / question_num * 100
    # 1) 获取当前本地时间
    now = time.localtime()
    # 2) 按指定格式转成字符串#%y四位年m两位月%d两位天#24小时制小时....
    readable = time.strftime('%Y-%m-%d %H:%M:%S', now)
    result = score_judgment(score)
    print(
        f'Congratulations, you have completed the test. Your test date is{time_min_use} minutes {time_sec_use} seconds\nThe number of questions you answered correctly is\t{correct_answer_num}\nThe number of questions you answered wrongly is\t{wrong_answer_num}\nThe number of questions you skipped is\t{number_of_questions_skipped}\nThe score of your test is\t{score}\nThe end time is\t{readable}\nThe evaluation is\t{result}\n')
    test_data.append({
        'test_name': test_name,
        'time_left':f'minutes:{time_min_use},seconds:{time_sec_use}',
        'readable':readable,
        'score':score
    })
    edit_question_file_add(test_data,'test_data.txt')
def save_result():
    leaderboard_data=[]
    test_data=load_question_file('test_data.txt')
    for leaderboard in test_data:
        if 'score' in leaderboard:
            leaderboard_data.append(leaderboard)
    leaderboard_data.sort(key=lambda x:(-x['score'],x['time_left']))#进行排序
    edit_question_file_add(leaderboard_data,'leaderboard.txt')
def view_leaderboard():
    leaderboard_data=load_question_file('leaderboard.txt')
    leaderboard_num=0
    while leaderboard_num<=10:
        for leaderboard in leaderboard_data:
            print(leaderboard)
            leaderboard_num+=1
if __name__ == '__main__':
   save_result() 
   view_leaderboard()