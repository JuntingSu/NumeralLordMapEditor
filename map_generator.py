import json
import map_to_json
import random
import map_editor
blankmap='''
{
	"title": "随机地图-汪洋",
	"description": "这是一个由python程序生成的地图",
	"author": "#随机地图",
	"version": 1,
	"length": 7,
	"width": 7,
	"star_turn_three": 0,
	"star_turn_two": 0,
	"time_per_turn":120,
	"time_total":1800,
	"random_seat": 0,
	"cycle_map": 0,
	"fog_mode": 1,
	"star_mode": 0,
	"player": 2,
	"player_list": [
		{
			"name": "玩家1",
			"team": 1,
			"computer": 1,
			"seat": 1,
			"flag": 1001
		},
		{
			"name": "玩家2",
			"team": 2,
			"computer": 1,
			"seat": 2,
			"flag": 1002
		}
	],
	"battlefield": [
		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[2,128,0],
		[3,128,0],[1,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[2,128,0],
		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[2,128,0],
		[3,128,0],[3,128,0],[3,128,0],[1,128,0],[3,128,0],[3,128,0],[3,128,0],
		[3,128,0],[3,128,0],[3,128,0],[1,128,0],[3,128,0],[3,128,0],[3,128,0],
		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],
		[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0],[3,128,0]
	]
}
'''

def createNormalMap(terrain,length,width):

    jsonmap=json.loads(blankmap)
    jsonmap["length"]=length
    jsonmap["width"]=width
    jsonmap["battlefield"]=[[] for i in range(length*width)]
    for i in range(length*width):
        jsonmap["battlefield"][i].append(terrain)
        jsonmap["battlefield"][i].append(128)
        jsonmap["battlefield"][i].append(0)

    return jsonmap


def createRandomMap(length,width):
    # 生成空白模板
    jsonmap=json.loads(blankmap)
    jsonmap["length"]=length
    jsonmap["width"]=width
    jsonmap["battlefield"]=[[] for i in range(length*width)]
    #记录随机生成的据点位置
    basepointlist=[]
    # 随机生成地形
    for i in range(length*width):
        terrain=int(5*random.random())
        if terrain==2:
            basepointlist.append(i)
        jsonmap["battlefield"][i].append(terrain)
        jsonmap["battlefield"][i].append(128)
        jsonmap["battlefield"][i].append(0)
    # 给每个玩家一个随机的据点
    bases=random.sample(basepointlist,2)
    for i,b in enumerate(bases):
        jsonmap["battlefield"][b][1]=i+1
        jsonmap["battlefield"][b][2]=i+3
        print(f"b:{b},i:{i}")


    return jsonmap

def createBetterRandomMap(length,width,mode,playernum=2,computernum=2):
    jsonmap=createNormalMap(3,length,width)
    if playernum>2:
        for i in range(playernum-2):
            jsonmap=map_editor.addNewPlayer(jsonmap)
    # 各个地形出现权重
    weightlist = [0.2, 0.4, 0.6, 0.8, 1]
    if mode=='random':
        weightlist = [0.2, 0.4, 0.6, 0.8, 1]
        jsonmap=map_editor.changeNormalElements(jsonmap,'title','随机地图-破碎')
    elif mode=='plain':
        weightlist=[0,0.58,0.6,0.84,1]
        jsonmap=map_editor.changeNormalElements(jsonmap,'title','随机地图-均衡')
    elif mode == 'river':
        weightlist=[0,0.33,0.35,0.35,1]
        jsonmap=map_editor.changeNormalElements(jsonmap,'title','随机地图-河谷')

    # 记录随机生成的据点位置
    basepointlist = []
    # 随机生成地形
    for i in range(length * width):

        terr = random.random()
        terrain= 0
        for t in range(len(weightlist)):
            if terr<weightlist[t]:
                terrain=t
                break

        if terrain == 2:
            basepointlist.append(i)

        jsonmap["battlefield"][i][0]= terrain
        jsonmap["battlefield"][i][1]= 128
        jsonmap["battlefield"][i][2]= 0
    # 给每个玩家一个随机的据点
    if len(basepointlist)<2*playernum:
        for i in range(2*playernum-len(basepointlist)):
            r= int(length*width*random.random())
            jsonmap["battlefield"][r][0] = 2
            basepointlist.append(r)
    bases = random.sample(basepointlist, 2*playernum)

    for i, b in enumerate(bases):
        jsonmap["battlefield"][b][1] = int(i/2) + 1
        jsonmap["battlefield"][b][2] = int(i/2) + 3
        if i>=(playernum-computernum)*2:
            jsonmap["battlefield"][b][2] = 15

    return jsonmap

if __name__=="__main__":
    j=createBetterRandomMap(21,31,'plain',5,2)

    print(map_to_json.json2map(j))