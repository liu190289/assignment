import threading,time,queue
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
