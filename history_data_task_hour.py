#-*-coding=utf-8-*-
'''
Created on 2018年11月13日

@author: chao_qin
@description:程序入口 - 对小时历史数据插值
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

str_start_time = '2018-10-20 00:00:00'
str_end_time = '2018-10-20 00:00:00'

def work(current_task_name):
    structdata.start('hour', current_task_name, True)
    interpolate.start('hour', current_task_name)
    exportpng.start('hour', current_task_name)
    # remove_files(get_file_directory('txt', 'hour'))

def run_task(func, day=0, hour=0, min=0, second=0):
    try:
        print u'>>>>>>>>>>>>>>>>>开始时间:',current_time(),'>>>>>>>>>>>>>>>>>>>>>'
        iter_next_time = start_time = datetime.datetime.strptime(str_start_time,'%Y-%m-%d %H:%M:%S')
        str_iter_next_time = str(iter_next_time)
        # 第一次任务名称
        task_name = start_time.strftime('%Y%m%d%H')
        interval = datetime.timedelta(days=day, hours=hour, minutes=min, seconds=second)

        while str_iter_next_time <= str_end_time:
            work(task_name)
            print u'>>>>>>>>>>>>>>>>>>>>>>>完成任务', task_name, u'插值>>>>>>>>>>>>>>>>>>>>>>>\n'
            iter_next_time = iter_next_time + interval
            str_iter_next_time = iter_next_time.strftime('%Y-%m-%d %H:%M:%S')
            task_name = iter_next_time.strftime('%Y%m%d%H')
        print u'>>>>>>>>>>>>>>>>>结束时间:',current_time(),'>>>>>>>>>>>>>>>>>>>>>\n'
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() +' 生成小时历史数据任务[ ' + task_name  + u' ]插值异常:\n')
        log.append(str(e) + '\n')
        print log
        write_txt(get_absolute_path('log'), log, 'a')

def start():
    run_task(work, hour = 1)

if __name__=='__main__':
    start()