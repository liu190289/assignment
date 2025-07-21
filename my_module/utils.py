import threading,time,queue
from load_file import*
import json
from pyecharts.charts import Line
from pyecharts.options import TitleOpts, LegendOpts, ToolboxOpts, VisualMapOpts
def countdown(seconds,stop_evt,out_q):
    #如果没有给stop_evt就给一个永远不熄灭的灯
    stop_evt=stop_evt or threading.Event()
    time_min = 0
    for left in range(seconds,0,-1):
        time_sec =int(left%60)
        if stop_evt.is_set():#当灯亮的时候结束线程
            out_q.put(left)
            return
        if left>60:
            time_min=int(left/60)
        if left %10==0 or left<10:
            print(f'距离考试时间解释还有{time_min}分钟\t{time_sec}秒\n')
        time.sleep(1)
    print('\n时间到了')
    print('Please hit enter')
    out_q.put(0)
    stop_evt.set()
    return
#制作表格
def create_line_chart():
    data=load_question_file('leaderboard.txt')
    idx=0
    data_x_l = []
    data_y_l = []
    line = Line()
    while idx<len(data):
        data_x_1=data[idx]['test_name']
        data_y=data[idx]['score']
        data_x_2=data[idx]['time_left']
        data_x_2=data_x_2.replace(',',' ')
        dat_x_2=data_x_2.split(':')
        print(dat_x_2)
        data_x_2_1=dat_x_2[1][0]
        data_x_2_2=dat_x_2[2]
        data_x_2=f'(min:{data_x_2_1} sec:{data_x_2_2})'
        data_x=f'{data_x_1},{data_x_2}'
        print(data_x)
        data_x_l.append(data_x)
        data_y_l.append(data_y)
        idx+=1
    line.add_xaxis(data_x_l)
    line.add_yaxis('score',data_y_l)
    line.set_global_opts(
        title_opts=TitleOpts(title="leaderboard", pos_left='center', pos_bottom='1%'),
        legend_opts=LegendOpts(is_show=True),
        toolbox_opts=ToolboxOpts(is_show=True),
        visualmap_opts=VisualMapOpts(is_show=True)
    )
    line.render('line_chart.html')
    return True
create_line_chart()
