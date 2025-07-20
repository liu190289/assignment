from load_file import *
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