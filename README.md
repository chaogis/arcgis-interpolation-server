# ArcGIS空间插值服务
    ArcGIS空间插值服务，依赖ArcGIS Desktop/ArcGIS Server 及 python 2.7.x，实现从请求站点及小时/日/实时数据到反距离插值并输出插值结果png图片的完成流程。

### 本地运行项目

1. 下载代码：

    ``` 
        git@git.fpi-inc.site:product/public-products/arcgis-interpolation-server.git
     ```

2. 运行环境：

    ``` 
        python 2.7.x
        ArcGIS Desktop/Server  
    ```

3. 安装依赖：

    ``` shell
        pip install simplejson
        pip install apscheduler
    ```
    
4. 新建数据保存文件夹(interpolation_result_dir路径下)

    ``` 
        log
        state
        temp_day
        temp_hour
    ```
    * 若日志、临时文件及结果png存储在其他路径下，请在对应位置创建，若已存在请忽略
5. 启动项目

    ``` 
        python run_task.py
        python history_data_task_hour.py
        python history_data_task_day.py
    ```
    * 以上启动项目的方式中，根据需要选择运行，其中   
        第一个为常规的进行小时和日数据插值  
        第二个为历史小数数据插值   
        第三个为历史日数据插值


### 可自定义的配置


1. 出图模板

    出图模板``.mxd``文件配置在``/common/``文件夹下，其中``6colors``文件夹中为6色阶出图方案，``32colors``为32色阶出图方案，common根目录下为30色阶的小时和日数据出图方案。

    可根据需要，进行模板的定制化。

2. 插值结果图片的宽度和高度  

    ``config.py``中的``df_export_width、df_export_height``分别代表图片的宽度和高度，会决定输出图片的大小，该宽度与高度与插值过程中设置的栅格像元大小有关。若插值中像元大小发生变化，需重新计算输出图片的宽高。

3. 插值算法

    程序中可选用的插值算法包括``IDW、Kriging、IDW_ga（地统计分析反距离权重）``,经实验发现IDW_ga插值效果最好。``config.py``中的``is_idw``用于设置普通插值方式，``is_idw_ga``用于设置是否为 地统计学IDW。

4. 站点和监测数据请求路径

    ``config.py``中的``state_station_url``表示站点请求url，现在设置的是全国所有的国控站点，``state_hourdata_recent_url、state_hourdata_url、state_daydata_url``分别表示国控站最新的数据、国控站小时数据和国控站日数据接口，它们分别应用于常规和历史的小时/日数据插值。  
    
    针对其他区域的插值，若站点和监测数据请求路径发送变化，请替换数据请求路径。

5. 工作空间

    ``config.py``中的``base_dir``表示结果图片、日志、临时文件、出图模板等的存放路径，目前设置的路径是当前路径下的```interpolation_result_dir```，应确保该路径下有``log、state、temp_hour、temp_day``目录。

### 如何应用于其他项目


1. 配置该行政功能区的出图模板

    配置出图模板主要包括两方面：  
    （1）设置分类和色阶；  
    （2）做好``PAGE_LAYOUT``模式下的图幅配置

2. 修改站点和监测数据接口

* 站点接口返回数据格式应为标准GeoJSON格式，下面是数据格式示例：

``` json
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "coordinates": [
                        113.235,
                        23.1422
                    ],
                    "type": "Point"
                },
                "properties": {
                    "id": "5a13fa03e4ca2e05e4dd91dd",
                    "name": "广雅中学",
                    "type": "国控站",
                    "area": "广州市",
                    "cityCode": "440100.0",
                    "stationCode": "1345A"
                }
            }
        ]
    }
```

* 下面是监测数据格式示例：

``` json
    {
        "entries": [
            {
                "stationCode": "1071A",
                "stationName": null,
                "area": "沧州市",
                "measure": null,
                "heath": null,
                "quality": "重度污染",
                "year": "2018",
                "month": "2018-11",
                "day": "2018-11-27",
                "hours": "2018-11-27 11",
                "longitude": null,
                "latitude": null,
                "citycode": null,
                "MN": "1071A",
                "V_141": 26,
                "V_108": 54,
                "V_108_8H": 28,
                "V_121": 63,
                "V_101": 8,
                "V_AQI": 232,
                "V_107": 372,
                "V_106": 0.3,
                "V_127": null,
                "V_126": null,
                "V_129": null,
                "V_130": null,
                "V_128": null,
                "gb_hours": "2018-11-27 11",
                "MAIN_POLLUTANTS": [
                    "107"
                ]
            }
        ]
    }
```

### 项目目录结构

```
├── config.py                                   // 插值程序配置变量
├── utils.py                                    // 公共方法
├── structdata.py                               // 请求数据并对数据预处理代码
├── interpolate.py                              // 插值代码
├── exportpng.py                                // 出图代码
├── run_task.py                                 // 常规定时插值代码
├── history_data_task_hour.py                   // 历史小数数据插值代码
├── history_data_task_day.py                    // 历史日数据插值代码
├── main_hour.py                                // 小时数据常规定时插值代码（循环写法）
├── main_day.py                                 // 日数据常规定时插值代码（循环写法）
├── README.md                                   // 项目介绍
├── .gitignore                                  // git不需要上传的配置
├── interpolation_result_dir                    // 插值结果保存目录
│   ├── common                                  // 出图模板目录
│   ├── log                                     // 日志目录
│   ├── state                                   // 结果图片目录
│   ├── temp_hour                               // 小时数据插值生成临时文件目录
│   ├── temp_day                                // 日数据插值生成临时文件目录
```

### 其他说明

* 小时数据插值结果存储规范:  
    ``state/yyyy/mm/dd/因子名称_yyyymmddHH.png``
* 日数据插值结果存储规范:  
    ``state/yyyy/mm/dd/因子名称_yyyymmdd.png``  
* 月数据插值结果存储规范:  
    ``state/yyyy/mm/因子名称_yyyymm.png``  

    如以下示例：
    ```
        /state/2018/10/20/aqi_20181020.png
        /state/2018/10/20/aqi_2018102012.png
    ```