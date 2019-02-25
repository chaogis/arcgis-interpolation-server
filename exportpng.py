#-*-coding=utf-8-*-
'''
Created on 2018年11月13日

@author: chao_qin
@description:导出png图片
'''

import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

from arcpy.mapping import *
from arcpy import env

from utils import get_absolute_path
from utils import get_file_name
from utils import write_txt
from utils import current_time
from utils import format_file_name
from utils import delete_if_exist
from utils import get_file_directory
from utils import get_des_by_time
from config import df_export_width
from config import df_export_height
from config import z_fields

env.overwriteOutput = True

def export_png(z_field, time_interval = 'hour', current_task_name = None):
    try:
        mxd = MapDocument(get_absolute_path('mxd', z_field, time_interval))
        df = ListDataFrames(mxd, "*")[0]
        #mxd中的图层
        layer = ListLayers(mxd, "*", df)[0]
        #替换图层的数据源
        source_layer = get_file_name('tif', z_field, time_interval, current_task_name)
        layer.replaceDataSource(get_file_directory('tif', time_interval),
                                'RASTER_WORKSPACE',
                                source_layer,
                                True)
        layer.name = source_layer
        mxd.save()
        #若png已存在则删除之
        delete_if_exist(get_absolute_path('png', z_field, time_interval, current_task_name))
        ExportToPNG(mxd, 
                    get_absolute_path('png', z_field, time_interval, current_task_name), 
                    # 表示按PAGE_LAYOUT模式输出
                    'PAGE_LAYOUT',
                    df_export_width,
                    df_export_height,
                    resolution = 96,
                    world_file = False,
                    background_color="255, 255, 255",
                    transparent_color="255, 255, 255")
        del mxd
    except Exception,e:
        log = []
        log.append('>>>>>>>>>>' + current_time() + ' [' + format_file_name(time_interval, current_task_name) + '] 导出PNG {'+  z_field + '} 异常:\n')
        log.append(str(e) + '\n')
        write_txt(get_absolute_path('log'), log, 'a')

'''
    执行主方法
'''
def start(time_interval = 'hour', current_task_name = None):
    for z_field in z_fields:
        export_png(z_field, time_interval, current_task_name)
    print u'<<<<<<<<<<<<<<<<<<<<<<<<<3. ' + get_des_by_time(time_interval) + u' 导出PNG完成>>>>>>>>>>>>>>>>>>>>>>>>>>'
    
'''
    函数入口
'''
if __name__ =='__main__':
    print u'>>>>>>>>>>>>>导出png开始时间:', current_time(),'>>>>>>>>>>>>>>>>>>>>>>>>>>'
    start('day', '20181120')
    print u'>>>>>>>>>>>>>导出png结束时间:', current_time(),'>>>>>>>>>>>>>>>>>>>>>>>>>>'
    print u'>>>>>>>>>>>>>导出png成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'