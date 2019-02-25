#-*-coding=utf-8-*-
'''
Created on 2018年11月13日

@author: chao_qin
@description:程序入口 - 设置定时程序
'''

import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

import datetime
import structdata
import interpolate
import exportpng

from utils import write_txt
from utils import get_absolute_path
from utils import get_file_directory
from utils import current_time
from utils import format_file_name
from utils import remove_files

# 初始化定时程序时间(比预定时间提前1天)
str_init_time_day = '2018-11-20 01:30:00'

def work(current_task_name):
    structdata.start('day', current_task_name)
    interpolate.start('day', current_task_name)
    exportpng.start('day', current_task_name)
    remove_files(get_file_directory('txt', 'day'))

def run_task(func, day=0, hour=0, min=0, second=0):
    try:
        print u'>>>>>>>>>>>>>>>>>初始化时间:',str_init_time_day,'>>>>>>>>>>>>>>>>>>>>>'       
        init_time = datetime.datetime.strptime(str_init_time_day,'%Y-%m-%d %H:%M:%S')

        # 第一次执行时间 - 初始时间 + 时间间隔
        interval = datetime.timedelta(days=day)
        next_time = init_time + interval
        str_next_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
        print u'>>>>>>>>>>>>>>>>>第一次执行时间:',str_next_time,'>>>>>>>>>>>>>>>>>\n'

        while True:
            # 获取当前系统时间
            iter_now = datetime.datetime.now()
            iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
            if str(iter_now_time) == str(str_next_time):
                # 当前执行任务名称-yyyymmdd
                current_task_name = format_file_name('day')
                # 打印每次任务开始时间
                print u'>>>>>>>>>>>>任务', current_task_name, u'开始时间: %s' % iter_now_time,'>>>>>>>>>>>>'
                # 调用任务函数
                func(current_task_name)
                print u'>>>>>>>>>>>>>>>>>>>>完成时间: %s' % current_time(), '>>>>>>>>>>>>>>>>>>>>'
                # 获取任务下次执行时间
                iter_time = iter_now + interval
                str_next_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
                print u'>>>>>>>>>>>>>>>>>>>>下次执行时间: %s' % str_next_time, '>>>>>>>>>>>>>>>>\n'
                # 继续下次迭代
                continue
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>定时任务异常:\n')
        log.append(str(e) + '\n')
        print log
        write_txt(get_absolute_path('log'), log, 'a')

# 每天1:30插值
def start():
    run_task(work, day = 1)

if __name__=='__main__':
    start()