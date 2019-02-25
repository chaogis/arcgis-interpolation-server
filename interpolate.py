#-*-coding=utf-8-*-
'''
Created on 2018年11月13日

@author: chao_qin
@description:空间插值方法
'''

import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

import os
import arcpy
from arcpy import env
from arcpy.sa import *

from config import is_idw
from config import is_idw_ga
from config import x_field
from config import y_field
from config import z_fields
from utils import get_absolute_path
from utils import write_txt
from utils import current_time
from utils import get_outlayer_name
from utils import format_file_name
from utils import get_des_by_time

#插值生成栅格数据的裁切范围
env.extent = arcpy.Extent(73.44696, 18.160896, 135.09696, 53.560896)
env.overwriteOutput = True

#裁切矩形范围
clip_extent = "73.44696 18.160896 135.09696 53.560896"

#空间插值配置参数
#插值模型
kriging_model = KrigingModelOrdinary("SPHERICAL",0.05)
#像元大小（度）
cell_size = 0.05
#搜索半径
search_radius = RadiusVariable(12)
#距离指数 - IDW
power = 2

# 设置领域搜索参数
majorSemiaxis  = 8
minorSemiaxis  = 6
angle  = 0
#平滑参数
smoothFactor = 0.9
searchNeighbourhood = arcpy.SearchNeighborhoodSmooth(majorSemiaxis, 
                                                     minorSemiaxis,
                                                     angle, 
                                                     smoothFactor)

#裁切范围
clip_shp = "F:/temp_spatial_data/CHN_adm_shp/CHN_adm0.shp"

#生成shp文件
def make_shp(time_interval = 'hour', current_task_name = None):
    try:
        out_layer = get_outlayer_name()
        arcpy.MakeXYEventLayer_management(get_absolute_path('txt', time_interval = time_interval, current_task_name = current_task_name),
                                        x_field,
                                        y_field,
                                        out_layer,
                                        get_absolute_path('srs'))
        arcpy.FeatureToPoint_management(out_layer, get_absolute_path('shp', time_interval = time_interval, current_task_name = current_task_name))
        del out_layer
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 生成SHP异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')
#插值 - 普通IDW或Kriging插值
def do_interpolation(z_field, time_interval = 'hour', current_task_name = None):
    try:
        #检查空间分析模块权限
        arcpy.CheckOutExtension("Spatial")
        shp_path = get_absolute_path('shp', time_interval = time_interval, current_task_name = current_task_name)
        #根据配置选用IDW或Kriging插值算法
        out = Idw(shp_path, 
                  z_field, 
                  cell_size, 
                  power, 
                  search_radius) if is_idw else Kriging(shp_path, 
                                                        z_field, 
                                                        kriging_model, 
                                                        cell_size, 
                                                        search_radius)
        out.save(get_absolute_path('temp_tif', z_field, time_interval,current_task_name))
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 空间插值 {'+  z_field + '} 异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')

#插值 - 地统计插值
def do_interpolation_ga(z_field, time_interval = 'hour', current_task_name = None):
    try:
        # out_layer = get_outlayer_name()
        # arcpy.CheckOutExtension("Spatial")
        # 检查地统计模块权限
        arcpy.CheckOutExtension("GeoStats")
        shp_path = get_absolute_path('shp', time_interval = time_interval, current_task_name = current_task_name)
        arcpy.IDW_ga(shp_path, 
                     z_field, 
                     None, 
                     get_absolute_path('temp_tif', z_field, time_interval, current_task_name), 
                     cell_size, 
                     power, 
                     searchNeighbourhood)
        # del out_layer
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 空间插值 {'+  z_field + '} 异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')

#裁剪
def clip_tif(z_field, time_interval = 'hour', current_task_name = None):
    try:
        arcpy.Clip_management(
            #输入栅格-待裁切
            get_absolute_path('temp_tif', z_field, time_interval, current_task_name),
            clip_extent,
            #输出栅格数据集
            get_absolute_path('tif', z_field, time_interval, current_task_name),
            #裁切shape文件
            get_absolute_path('clip'), 
            "#", 
            "ClippingGeometry")
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 裁剪TIF {'+  z_field + '} 异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')
    

'''
    执行主方法
'''
def start(time_interval = 'hour', current_task_name = None):
    make_shp(time_interval, current_task_name)
    for z_field in z_fields:
        if is_idw_ga:
            do_interpolation_ga(z_field, time_interval, current_task_name)
        else:
            do_interpolation(z_field, time_interval)
        clip_tif(z_field, time_interval, current_task_name)
    print u'<<<<<<<<<<<<<<<<<<<<<<<<<2. ' + get_des_by_time(time_interval) + u' 空间插值完成>>>>>>>>>>>>>>>>>>>>>>>>>'
    
'''
    函数入口
'''
if __name__ =='__main__':
    print u'>>>>>>>>>>>>>插值开始时间:', current_time(),'>>>>>>>>>>>>>>>>>>>>>>>'
    start('day', '20181120')
    print u'>>>>>>>>>>>>>插值结束时间:', current_time(),'>>>>>>>>>>>>>>>>>>>>>>>'
    print u'>>>>>>>>>>>>>插值成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    