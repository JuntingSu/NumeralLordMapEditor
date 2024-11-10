数字领主地图码翻译工具：
两个工具包（旧）：
map_to_json负责进行地图码和json格式（文件）之间的转换
map_editor负责操作json文件
一个新的类Map，理论上可以实现上述两个文件内所有函数（但是还没有完成）




**调用工具包即可编写修改地图信息的程序，调用示例如下：
from  map_to_json import *
from  map_editor import *
