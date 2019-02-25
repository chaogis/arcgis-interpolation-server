#-*-coding=utf-8-*-
'''
Created on 2018年11月13日

@author: chao_qin
@description:请求数据并进行预处理
'''

import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

import urllib2
import os
import simplejson as json
# import datetime
from datetime import datetime
from datetime import timedelta

from config import station_url
from config import hourdata_recent_url
from config import hourdata_url
from config import daydata_url
from utils import get_absolute_path
from utils import write_txt
from utils import current_time
from utils import format_file_name
from utils import get_des_by_time
from utils import format_yestoday

#txt文件头
txt_header = 'stationCode,x,y,aqi,no2,pm25,o3,pm10,co,so2\n'

# BASE_DIR = os.path.dirname(__file__) #获取当前工作路径
# file_path = os.path.join(BASE_DIR, "statestation.txt") #完整路径

#请求数据
def request_data(url, time_interval = 'hour', current_task_name = None):
    try:
        return json.loads(urllib2.urlopen(url).read())
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 请求数据异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')

#将站点和小时数据挂接成ArcGIS支持格式
def struct_data(time_interval = 'hour', current_task_name = None, history = False):
    try:
        data_url = hourdata_recent_url

        if time_interval == 'hour':
            if history:
                data_url = hourdata_url.replace('{yyyy-mm-dd hh}', datetime.strptime(current_task_name,'%Y%m%d%H').strftime('%Y-%m-%d %H'))
            else:
                data_url = hourdata_recent_url
        elif time_interval == 'day':
            if current_task_name is not None:
                data_url = daydata_url.replace('{yyyy-mm-dd}', datetime.strptime(current_task_name,'%Y%m%d').strftime('%Y-%m-%d'))
            else:
                data_url = daydata_url.replace('{yyyy-mm-dd}', format_yestoday('%Y-%m-%d'))

        stations = request_data(station_url, time_interval, current_task_name)
        monitordatas = request_data(data_url, time_interval, current_task_name)
        
        features = stations['features']
        entries = monitordatas['entries']

        # print u'站点及小数数据数量：' , len(features), len(entries)

        text_content = []
        text_content.append(txt_header)

        for feature in features:
            stationCode = feature['properties']['stationCode'].strip()
            x = feature['geometry']['coordinates'][0]
            y = feature['geometry']['coordinates'][1]
            for entry in entries:
                MN = entry['MN'].strip()
                if stationCode == MN:
                    aqi = 0 if entry['V_AQI'] == -1 else entry['V_AQI']
                    no2 = entry['V_141']
                    pm25 = entry['V_121']
                    o3 = entry['V_108']
                    pm10 = entry['V_107']
                    co = entry['V_106']
                    so2 = entry['V_101']
                    text_content.append(stationCode+','+str(x)+','+str(y)+','+str(aqi)+','+str(no2)+','+str(pm25)+','+str(o3)+','+str(pm10)+','+str(co)+','+str(so2)+'\n')
                    entries.remove(entry)

        return text_content
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 数据挂接异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')

'''
   将专题信息写入文本
   history: 是否为历史数据
'''
def write_structed_data(time_interval, current_task_name = None, history = False):
    try:
        content = struct_data(time_interval, current_task_name, history)
        file_path = get_absolute_path('txt', time_interval = time_interval, current_task_name = current_task_name)
        write_txt(file_path, content)
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 写入TXT异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')

'''
    执行主方法
    history: 是否为历史数据
'''
def start(time_interval, current_task_name = None, history = False):
    write_structed_data(time_interval, current_task_name, history)
    print u'<<<<<<<<<<<<<<<<<<<<<<1. 写入', get_des_by_time(time_interval), u'TXT完成>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

'''
    函数入口
'''
if __name__ =='__main__':
    print u'>>>>>>>>>>数据预处理开始时间:', current_time(),'>>>>>>>>>>>>>>>>>>>>'
    start('hour')
    print u'>>>>>>>>>>数据预处理结束时间:', current_time(),'>>>>>>>>>>>>>>>>>>>>'
    print u'>>>>>>>>>>数据预处理成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'