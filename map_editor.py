import json

# 旗帜编号-非国旗部分
FLAGLIST_WITHOUT_NATIONAL_FLAG = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1101, 1102, 1103, 1104, 1105,
                                  1106, 1107, 1108, 1109, 1110, 1201, 1202, 1203, 1301, 1302, 3001, 3002, 3003, 4001,
                                  4002, 4003, 4004, 4101, 4102, 4103, 4104, 4114]
# 旗帜编号-国旗（未完成）
FLAGLIST_NATIONAL_FLAG = []

# 地图json文件中的一些变量
TEXT_VALUE = ['title', 'description', 'author']
INT_VALUE = ['version', 'length', 'width', 'star_turn_three', 'star_turn_two', 'time_per_turn', 'time_total']
BOOL_VALUE = ['random_seat', 'cycle_map', 'fog_mode', 'star_mode']
NORMAL_VALUE = TEXT_VALUE + INT_VALUE + BOOL_VALUE


def createDefaultMap() -> json:
    blankmap = '''
    {
        "title": "New Map",
    	"description": "This is a map created by JuntingSu's Python code.",
    	"author": "#JuntingSu",
    	"version": 1,
    	"length": 25,
    	"width": 25,
    	"star_turn_three": 0,
    	"star_turn_two": 0,
    	"time_per_turn":120,
    	"time_total":1800,
    	"random_seat": 0,
    	"cycle_map": 0,
    	"fog_mode": 0,
    	"star_mode": 0,
    	"player": 2,
    	"player_list": [
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
    	],
    	"battlefield": [
    		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],
    		[3,128,0],[1,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],
    		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],
    		[3,128,0],[3,128,0],[3,128,0],[1,128,0],[3,128,0],[3,128,0],[3,128,0],
    		[3,128,0],[3,128,0],[3,128,0],[1,128,0],[3,128,0],[3,128,0],[3,128,0],
    		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],
    		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0]
    	]
    }
    '''
    jsonmap = json.loads(blankmap)
    return jsonmap


# 修改地图单项信息，json为需要修改的地图文件，key为要修改的信息名，value为修改后的值，该函数返回一个json格式的地图
def changeNormalElements(mapjson: json, key: str, value: int | str) -> json:
    if key not in NORMAL_VALUE:
        raise ValueError('无效的属性名称')
    mapjson[key] = value
    return mapjson


# computer：255对应休闲，1对应普通，2对应困难，3对应疯狂
# 在地图文件中新增一个势力，json为需要修改的地图文件，name为新势力名，team为新势力队伍，
# flagnum是新势力旗帜，computer是新势力的电脑操作等级，该函数返回一个json格式的地图
def addPlayer(mapjson: json, name: str, team: int, flagnum: int, computer: int) -> json:
    player = {}
    player_num = mapjson['player']
    player.update(
        {
            'name': name,
            "team": 2 ** (team - 1),
            "computer": computer,
            "seat": player_num + 1,
            "flag": flagnum
        }
    )
    mapjson['player_list'].append(player)
    mapjson['player'] += 1
    return mapjson


# addPlayer的衍生函数，用于创建一个默认的占位玩家
# 目前只能在人数低于36时使用
def addNewPlayer(mapjson: json) -> json:
    nextseat = mapjson['player']
    mapjson = addPlayer(mapjson, 'Player', nextseat + 1, FLAGLIST_WITHOUT_NATIONAL_FLAG[nextseat], 1)
    return mapjson


# 修改现有玩家信息
# index可以是玩家序号（从0开始！）或玩家姓名
# name,team,flagnum,computer都是可选项,选择即可修改对应属性
def setPlayer(mapjson: json, index: int | str, name: str | None = None, team: int = -10, flagnum: int = -10,
              computer: int = -10) -> json:
    playerindex = -1
    if isinstance(index, str):
        for i in range(mapjson['player']):
            if mapjson['player_list'][i]['name'] == index:
                playerindex = i
    elif isinstance(index, int):
        playerindex = index
    if playerindex < 0 or playerindex >= mapjson['player']:
        raise ValueError('找不到对应玩家')

    player = {}
    player.update(
        {
            'name': name if name else mapjson['player_list'][playerindex]['name'],
            "team": 2 ** (team - 1) if not team == -10 else mapjson['player_list'][playerindex]['team'],
            "computer": computer if not computer == -10 else mapjson['player_list'][playerindex]['computer'],
            "seat": playerindex + 1,
            "flag": flagnum if not flagnum == -10 else mapjson['player_list'][playerindex]['flag']
        }
    )
    mapjson['player_list'][playerindex] = player

    return mapjson


# 删除一个势力
# index可以是玩家序号（从0开始！）或玩家姓名
def removePlayer(mapjson: json, index: int | str) -> json:
    player_num = mapjson['player']
    playerindex = -1
    if isinstance(index, str):
        for i in range(mapjson['player']):
            if mapjson['player_list'][i]['name'] == index:
                playerindex = i
    elif isinstance(index, int):
        playerindex = index
    if playerindex < 0 or playerindex >= mapjson['player']:
        raise ValueError('找不到对应玩家')
    for i in range(playerindex, player_num):
        mapjson['player_list'][i]['seat'] -= 1

    area = mapjson['length'] * mapjson['width']
    for j in range(area):
        if mapjson['battlefield'][j][1] - 1 in range(playerindex, player_num):
            print(f'HEY!{j}')
            mapjson['battlefield'][j][1] -= 1

    mapjson['player_list'].pop(playerindex)
    mapjson['player'] -= 1
    return mapjson


# 对removePlayer的衍生,删除末位玩家
def removeLastPlayer(mapjson: json) -> json:
    mapjson = removePlayer(mapjson, mapjson['player'] - 1)
    return mapjson


def changePlayerNum(mapjson: json, playernum: int) -> json:
    if playernum <= 0:
        raise ValueError('玩家数必须是正数')
    current_player_num = mapjson['player']
    if playernum < current_player_num:
        for i in range(current_player_num - playernum):
            mapjson = removeLastPlayer(mapjson)
    elif playernum > current_player_num:
        for i in range(playernum - current_player_num):
            mapjson = addNewPlayer(mapjson)

    return mapjson


# 在地图上放置一个新的兵

def addSoldier(mapjson: json, player_idx: int, position: int, strength: int) -> json:
    area = mapjson['length'] * mapjson['width']
    if position < 0 or position >= area:
        raise ValueError(f"地块坐标{position}越界！，请输入0-{area - 1}的值")
    if strength <= 0:
        raise ValueError(f"兵力{strength}必须是正数")

    mapjson['soldier'][player_idx].append([position, strength])
    return mapjson


# 移除指定兵
def removeSoldier(mapjson: json, player_idx: int, position: int) -> json:
    area = mapjson['length'] * mapjson['width']
    if position < 0 or position >= area:
        raise ValueError(f"地块坐标{position}越界！，请输入0-{area - 1}的值")

    for i in range(len(mapjson['soldier'][player_idx])):
        if mapjson['soldier'][player_idx][i][0] == position:
            mapjson['soldier'][player_idx].pop(i)
    return mapjson


__all__ = ['FLAGLIST_NATIONAL_FLAG', 'FLAGLIST_WITHOUT_NATIONAL_FLAG', 'addPlayer', 'setPlayer', 'removePlayer',
           'addSoldier', 'removeSoldier', 'changeNormalElements']
