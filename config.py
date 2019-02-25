#-*-coding=utf-8-*-
'''
Created on 2018年11月13日

@author: chao_qin
@description:arcpy空间插值配置信息
'''

import sys
reload(sys)  
sys.setdefaultencoding('utf-8') 

import os

# 普通插值方式
is_idw = True

# 是否为地学统计下的IDW
is_idw_ga = True

#经度字段名称
x_field = 'x'

#纬度字段名称
y_field = 'y'

#插值因子
z_field = 'aqi'
z_fields = ['aqi', 'no2', 'pm25', 'o3', 'pm10', 'co', 'so2']

#mxd模板及颜色分类 - 默认32色
color_range = '30color'

#导出png图片宽高
df_export_width = 964
df_export_height = 707

#请求数据url
station_url = 'http://yun.fpi-inc.site/fpi-basemap-server/api/v1/stations'
#小时最新数据
hourdata_recent_url = 'http://yun.fpi-inc.site/scas/api/v1.0/stations/hour-data/recent'
#指定小时获取小时数据
hourdata_url = 'http://yun.fpi-inc.site/scas/api/v1.0/stations/hour-data/{yyyy-mm-dd hh}'
#指定日期获取日数据
daydata_url = 'http://yun.fpi-inc.site/scas/api/v1.0/stations/day-data/{yyyy-mm-dd}'

#当前工作空间
# base_dir = 'G:/InterpolationResult'
base_dir = os.path.join(os.getcwd(), 'interpolation_result_dir')

#mxd模板文件名称
mxd_file_name = 'state_$_export_template_#_' + color_range + '.mxd'

#裁切shape文件名称
clip_shp_name = 'china_clip_template.shp'

#生成shape文件的空间参考
spatial_reference = 'WGS 1984.prj'

#mxd模板及裁切shape、srs文件保存位置
common_path = 'common'

#png图片保存位置
png_path = 'state'

#日志文件保存位置
log_path = 'log'

#小时插值 - 临时文件保存文字，包括txt、shp、各因子tif等
temp_path_hour = 'temp_hour'

#日插值 - 临时文件保存文字，包括txt、shp、各因子tif等
temp_path_day = 'temp_day'