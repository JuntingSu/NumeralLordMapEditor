from numpy import random

import map_editor
import map_to_json
import json

from typing import Dict, List, Any
from pydantic import BaseModel

# map类里只有mapjson一个参数，mapjson的分支如下
# "version":        版本号，整数
# "title":          标题，字符串
# "description":    简介，字符串
# "author":         作者，字符串
# "length":         长，整数
# "width":          宽，整数
# "random_seat":    随机座位，0或1
# "cycle_map":      循环地图，0或1
# "fog_mode":       迷雾模式，0或1
# "star_mode":      星星模式，0或1
# "star_turn_three": 三星回合数，整数
# "star_turn_two":  二星回合数，整数
# "player":         玩家数量，整数
# "player_list":    玩家列表，玩家数组
# "terrain":        地形。整数数组
# "soldier":        士兵类，整数数组数组数组
# 玩家（playerlist里的元素）：
# "name": 名称，字符串
# "team": 队伍，整数
# "computer": 电脑难度，整数
# "seat": 座位号，整数
# "flag": 使用旗帜编号，整数
# 士兵（soldier）里的元素：
# [position,strength]表示在position处兵力为strength的兵，一层下标表示所属玩家

# 旗帜编号-非国旗部分
FLAGLIST_WITHOUT_NATIONAL_FLAG = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1101, 1102, 1103, 1104, 1105,
                                  1106, 1107, 1108, 1109, 1110, 1201, 1202, 1203, 1301, 1302, 3001, 3002, 3003, 4001,
                                  4002, 4003, 4004, 4101, 4102, 4103, 4104, 4114]
# 旗帜编号-国旗（未完成）
FLAGLIST_NATIONAL_FLAG = []


class Map(BaseModel):
    version: int = 1
    title: str = 'New Map'
    description: str = "This is a map created by JuntingSu's Python"
    author: str = "#JuntingSu"
    length: int = 7
    width: int = 7
    random_seat: bool = False
    cycle_map: bool = False
    fog_mode: bool = False
    star_mode: bool = False
    star_turn_three: int = 0
    star_turn_two: int = 0
    time_per_turn: int = 120
    time_total: int = 1800
    player_num: int = 2
    player_list: List[Dict[str, Any]] = [
        {
            "name": "Player1",
            "team": 1,
            "computer": 1,
            "seat": 1,
            "flag": 1001
        },
        {
            "name": "Player2",
            "team": 2,
            "computer": 1,
            "seat": 2,
            "flag": 1002
        }
    ]
    battlefield: List[List[int]] = [
        [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [2, 128, 0],
        [3, 128, 0], [1, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [2, 128, 0],
        [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [2, 128, 0],
        [3, 128, 0], [3, 128, 0], [3, 128, 0], [1, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0],
        [3, 128, 0], [3, 128, 0], [3, 128, 0], [1, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0],
        [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0],
        [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0], [3, 128, 0]
    ]

    #################################################################
    ################# Editor Functions ##############################
    #################################################################

    # 修改常规地图信息的母函数，私有
    def _changeNormalElements(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            raise ValueError(f"{key} is not a valid variable name in this class")

    # 修改标题
    def renameTitle(self, newTitle):
        self._changeNormalElements('title', newTitle)

    # 修改简介
    def renameDescription(self, newDescription):
        self._changeNormalElements('description', newDescription)

    # 修改作者名
    def renameAuthor(self, newAuthor):
        self._changeNormalElements('author', newAuthor)

    # 新增默认玩家
    def addDefaultPlayer(self) -> int:
        player = {}
        player_num = self.player_num
        player.update(
            {
                "name": "Player",
                "team": 2 ** player_num,
                "computer": 1,
                "seat": player_num + 1,
                "flag": FLAGLIST_WITHOUT_NATIONAL_FLAG[player_num]
            }
        )
        self.player_list.append(player)
        self.player_num += 1

        return player_num

    # 修改玩家信息
    def setPlayer(self, index: int | str, **kwargs) -> int:
        playerindex = -1
        if isinstance(index, str):
            for i in range(self.player_num):
                if self.player_list[i]['name'] == index:
                    playerindex = i
        elif isinstance(index, int):
            playerindex = index
        if playerindex < 0 or playerindex >= self.player_num:
            raise ValueError('找不到对应玩家')

        self.player_list[playerindex].update(kwargs)

        return playerindex

    # 新增玩家
    def addPlayer(self, **kwargs) -> int:
        seat = self.addDefaultPlayer()
        self.setPlayer(seat, **kwargs)

        return seat


    def resizeMap(self,length,width):
        # if length< self.length:
        if length< self.length:
            for i in range((self.length-length)*self.width):
                self.battlefield.pop()
        else:
            for i in range((length-self.length)*self.width):
                self.battlefield.append([3,128,3])
        self.length=length

        if width<self.width:
            for j in range(self.length):
                for i in range((self.width-width)):
                    self.battlefield.pop(width-1+(self.length-1-j)*self.width)

        else:
            for j in range(self.length):
                for i in range((width-self.width)):
                    self.battlefield.insert(self.width+(self.length-1-j)*self.width,[3,128,8])
        self.width = width

    # 删除指定玩家
    def removePlsyer(self, index: int | str) -> int:
        playerindex = self.finePlayer(index)
        for i in range(playerindex, self.player_num):
            self.player_list[i]['seat'] -= 1

        area = self.length * self.width
        for j in range(area):
            if self.battlefield[j][1] - 1 in range(playerindex, self.player_num):
                self.battlefield[j][1] -= 1

        self.player_list.pop(playerindex)
        self.player_num -= 1
        return self.player_num

    #################################################################
    #################### I/O Functions ##############################
    #################################################################

    # 输出玩家名列表
    def getPlayerList(self) -> List[str]:
        playerList = []
        for player in self.player_list:
            playerList.append(player['name'])
        return playerList

    # 输出完整的玩家信息
    def getCompletePlayerInfo(self) -> List[Dict]:
        playerList = []
        for player in self.player_list:
            playerList.append(player)
        return playerList

    # 输出地图中的信息
    def getBattlefield(self) -> List[List]:
        return self.battlefield

    # 输出json格式的地图码
    def getJsonMap(self)-> str:
        return map_to_json.json2str(self.dict())

    # 输出预览地图的jpg格式图片
    def getPicMap(self)->str:
        return ''

    # 输出地图码
    def getCodeMap(self)-> str:
        return map_to_json.json2map(self.dict())

    #################################################################
    #################### Map Functions ##############################
    #################################################################

    # 生成同一地形的地图
    def createNormalMap(self, terrain, length, width):

        self.length = length
        self.width = width
        self.battlefield = [[] for i in range(length * width)]
        for i in range(length * width):
            self.battlefield[i].append(terrain)
            self.battlefield[i].append(128)
            self.battlefield[i].append(0)

    # 生成地形随机的地图
    def createRandomMap(self, length, width):
        # 生成空白模板
        self.length = length
        self.width = width
        self.battlefield = [[] for i in range(length * width)]
        # 记录随机生成的据点位置
        basepointlist = []
        # 随机生成地形
        for i in range(length * width):
            terrain = int(5 * random.random())
            if terrain == 2:
                basepointlist.append(i)
            self.battlefield[i].append(terrain)
            self.battlefield[i].append(128)
            self.battlefield[i].append(0)
        # 给每个玩家一个随机的据点
        bases = random.sample(basepointlist, 2)
        for i, b in enumerate(bases):
            self.battlefield[b][1] = i + 1
            self.battlefield[b][2] = i + 3
            print(f"b:{b},i:{i}")

    # 生成更加合理的随机地形地图
    def createBetterRandomMap(self, length, width, mode, playernum=2, computernum=2):
        self.createNormalMap(3, length, width)
        if playernum > 2:
            for i in range(playernum - 2):
                jsonmap = map_editor.addNewPlayer(jsonmap)
        # 各个地形出现权重
        weightlist = [0.2, 0.4, 0.6, 0.8, 1]
        if mode == 'random':
            weightlist = [0.2, 0.4, 0.6, 0.8, 1]
            jsonmap = map_editor.changeNormalElements(jsonmap, 'title', '随机地图-破碎')
        elif mode == 'plain':
            weightlist = [0, 0.58, 0.6, 0.84, 1]
            jsonmap = map_editor.changeNormalElements(jsonmap, 'title', '随机地图-均衡')
        elif mode == 'river':
            weightlist = [0, 0.33, 0.35, 0.35, 1]
            jsonmap = map_editor.changeNormalElements(jsonmap, 'title', '随机地图-河谷')

        # 记录随机生成的据点位置
        basepointlist = []
        # 随机生成地形
        for i in range(length * width):

            terr = random.random()
            terrain = 0
            for t in range(len(weightlist)):
                if terr < weightlist[t]:
                    terrain = t
                    break

            if terrain == 2:
                basepointlist.append(i)

            jsonmap["battlefield"][i][0] = terrain
            jsonmap["battlefield"][i][1] = 128
            jsonmap["battlefield"][i][2] = 0
        # 给每个玩家一个随机的据点
        if len(basepointlist) < 2 * playernum:
            for i in range(2 * playernum - len(basepointlist)):
                r = int(length * width * random.random())
                jsonmap["battlefield"][r][0] = 2
                basepointlist.append(r)
        bases = random.sample(basepointlist, 2 * playernum)

        for i, b in enumerate(bases):
            jsonmap["battlefield"][b][1] = int(i / 2) + 1
            jsonmap["battlefield"][b][2] = int(i / 2) + 3
            if i >= (playernum - computernum) * 2:
                jsonmap["battlefield"][b][2] = 15

        return jsonmap

    def generate_general_map(self, terrian, length, width):
        self.battlefield = [[terrian, 128, 0]] * length * width
        self.length = length
        self.width = width

    #################################################################
    ################### Tool Functions ##############################
    #################################################################

    def finePlayer(self, index: str | int) -> int:
        playerindex = -1
        if isinstance(index, str):
            for i in range(self.player_num):
                if self.player_list[i]['name'] == index:
                    playerindex = i
        elif isinstance(index, int):
            playerindex = index
        if playerindex < 0 or playerindex >= self.player_num:
            raise ValueError('找不到对应玩家')

        return playerindex


if __name__ == "__main__":
    mm = map_to_json.readmap(filepath='file/example1.json')

    testMap = Map(**mm)
    print(testMap.getCodeMap())

    testMap.resizeMap(11,13)
    # print(len(testMap.getBattlefield()))
    print(testMap.getCodeMap())

    testMap.resizeMap(9,11)
    # print(len(testMap.getBattlefield()))
    # print(testMap.getJsonMap())
    print(testMap.getCodeMap())
    # testMap2=Map()
