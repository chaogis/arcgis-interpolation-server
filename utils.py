#-*-coding=utf-8-*-
'''
Created on 2018年11月13日

@author: chao_qin
@description:公共方法
'''

import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

import os
import shutil
import codecs
from datetime import datetime
from datetime import timedelta

from config import is_idw
from config import mxd_file_name
from config import clip_shp_name
from config import spatial_reference
from config import png_path
from config import log_path
from config import temp_path_hour
from config import temp_path_day
from config import common_path
from config import base_dir

#获取当前时间  YYYY-MM-DD HH:MM:SS格式
def current_time(format = '%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(format)

def format_yestoday(format = '%Y-%m-%d', date = None):
    if date is None:
        return (datetime.now() + timedelta(days=-1)).strftime(format)
    else:
        return (datetime.strptime(date,'%Y%m%d') + timedelta(days=-1)).strftime(format)

'''
    根据当前日期/小时构造文件名称 
    小时-YYYYMMDDHH 天-YYYYMMDD 月-YYYYMM
    type: hour, day, month
'''
def format_file_name(type = 'hour', current_task_name = None):
    if current_task_name is not None:
        return current_task_name
    else:
        if type == 'hour':
            return current_time('%Y%m%d%H')
        elif type == 'day':
            return format_yestoday('%Y%m%d')
        elif type == 'month':
            return current_time('%Y%m')

# 构造png图片路径
def format_png_path(time_interval, current_task_name = None):
    if current_task_name is not None:
        if time_interval == 'hour':
            return datetime.strptime(current_task_name,'%Y%m%d%H').strftime('%Y/%m/%d')
        elif time_interval == 'day':
            return datetime.strptime(current_task_name,'%Y%m%d').strftime('%Y/%m/%d')
        elif time_interval == 'month':
            return datetime.strptime(current_task_name,'%Y%m').strftime('%Y/%m')
    else:
        if time_interval == 'hour':
            return current_time('%Y/%m/%d')
        elif time_interval == 'month':
            return current_time('%Y/%m')
        elif time_interval == 'day':
            return format_yestoday('%Y/%m/%d')

'''
    根据类型获取文件名
    type: txt, shp, tif, png, log
    文件名:
        20181114090000.txt
        20181114090000.shp
        20181114090000_aqi_temp.tif
        20181114090000_so2_temp.tif
        20181114090000_aqi.tif
        20181114090000_so2.tif
        idw/kriging_station_aqi_20181113190000.png
        idw/kriging_station_so2_20181113190000.png
        20181114.log
'''
def get_file_name(file_type, factor = 'aqi', time_interval = 'hour', current_task_name = None):
    file_name = format_file_name(time_interval, current_task_name) + '.' + file_type
    if file_type == 'png':
        file_name = factor + '_' + format_file_name(time_interval, current_task_name) + '.' + file_type
    elif file_type == 'mxd':
        file_name = mxd_file_name.replace('$', factor).replace('#', time_interval)
    elif file_type == 'clip':
        file_name = clip_shp_name
    elif file_type == 'srs':
        file_name = spatial_reference
    elif file_type == 'temp_tif':
        file_name = format_file_name(time_interval, current_task_name) + '_' + factor + '_temp.tif'
    elif file_type == 'tif':
        file_name = format_file_name(time_interval, current_task_name) + '_' + factor + '.tif'
    elif file_type == 'log':
        file_name = datetime.now().strftime('%Y%m%d') + '.' + file_type

    return file_name

#获取文件目录
def get_file_directory(type, time_interval = 'hour', current_task_name = None):
    relative_path = common_path
    if type == 'mxd' or type == 'clip' or type == 'srs':
        relative_path = common_path
    elif type == 'png':
        relative_path = os.path.join(png_path, format_png_path(time_interval, current_task_name))
    elif type == 'log':
        relative_path = log_path
    elif type == 'txt' or type == 'shp' or type == 'tif' or type == 'temp_tif':
        if time_interval == 'hour':
            relative_path = temp_path_hour
        elif time_interval == 'day':
            relative_path = temp_path_day
    
    # 对png图片，若路径不存在则创建之
    if type == 'png':
        make_dir_if_not_exist(os.path.join(base_dir, relative_path))

    return os.path.join(base_dir, relative_path)

'''
    根据类型获取文件绝对路径
'''
def get_absolute_path(file_type, factor = 'aqi', time_interval = 'hour', current_task_name = None):
    file_dir = get_file_directory(file_type, time_interval, current_task_name)
    file_name = get_file_name(file_type, factor, time_interval, current_task_name)
    return os.path.join(file_dir, file_name) 

# 生成输出图层的名称 YYYYMMDDHHMMSS格式
def get_outlayer_name():
    return datetime.now().strftime('%Y%m%d%H%M%S')

#文本内容写入
def write_txt(file_path, content, mode = 'w'):
    with open(file_path, mode) as f:
        f.write(codecs.BOM_UTF8)
        f.writelines(content)
        f.flush()
        f.close()

# 删除目录中的所有文件
def remove_files(dir_path):
    if os.path.exists(dir_path):
        file_list=os.listdir(dir_path)
        for f in file_list:
            file_path = os.path.join(dir_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, True)
    else:
        print u'>>>>>>>>>>目录', dir_path, u'不存在！>>>>>>>>>>'


# 文件若存在则删除
def delete_if_exist(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    # else:
        # print u'>>>>>>>>>>文件', file_path, u'不存在！>>>>>>>>>>'

# 目录不存在则创建
def make_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 根据时间尺度类型获取对应中文说明
def get_des_by_time(type = 'hour'):
    if type == 'hour':
        return u'小时'
    elif type == 'day':
        return u'天度'
    elif type == 'month':
        return u'月度'
