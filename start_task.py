#-*-coding=utf-8-*-
'''
Created on 2018年11月20日

@author: chao_qin
@description:程序入口 - 设置定时程序
'''

import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

import logging
logging.basicConfig()
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

import structdata
import interpolate
import exportpng

from utils import write_txt
from utils import get_absolute_path
from utils import get_file_directory
from utils import current_time
from utils import format_file_name
from utils import remove_files

def hour_job():
    current_task_name = format_file_name('hour')
    # 打印每次任务开始时间
    print u'>>>>>>>>>>>>任务', current_task_name, u'开始时间: %s' % current_time(),'>>>>>>>>>>>>'
    structdata.start('hour', current_task_name, False)
    interpolate.start('hour', current_task_name)
    exportpng.start('hour', current_task_name)
    remove_files(get_file_directory('txt', 'hour'))
    print u'>>>>>>>>>>>>>>>>>>>>完成时间: %s' % current_time(), '>>>>>>>>>>>>>>>>>>>>\n'

def day_job():
    current_task_name = format_file_name('day')
    # 打印每次任务开始时间
    print u'>>>>>>>>>>>>任务', current_task_name, u'开始时间: %s' % current_time(),'>>>>>>>>>>>>'
    current_task_name = format_file_name('day')
    structdata.start('day', current_task_name, False)
    interpolate.start('day', current_task_name)
    exportpng.start('day', current_task_name)
    remove_files(get_file_directory('txt', 'day'))
    print u'>>>>>>>>>>>>>>>>>>>>完成时间: %s' % current_time(), '>>>>>>>>>>>>>>>>>>>>\n'

if __name__ == '__main__':
    # executors = {
    #     'default': ProcessPoolExecutor(3)
    # }
    executors = {
        'default': ProcessPoolExecutor(5),
        'processpool': ThreadPoolExecutor(20)
    }
    sched = BlockingScheduler(executors=executors)
    sched.add_job(hour_job, 'cron', minute='13, 28, 43, 58', id='hour_job_id', misfire_grace_time=60)
    sched.add_job(day_job, 'cron', hour = '16', minute = '48', id='day_job_id', misfire_grace_time=600)
    try:
        print u'>>>>>>>>>>>>>>当前时间: %s' % current_time(), u'等待执行任务>>>>>>>>>>>>>>'
        sched.start()
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>定时任务异常:\n')
        log.append(str(e) + '\n')
        print log
        write_txt(get_absolute_path('log'), log, 'a')
