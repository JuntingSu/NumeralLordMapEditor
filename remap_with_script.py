import json
import map_to_json as m
import map_editor as e


def readScript(mapcode:str,scriptpath:str)->str:
    jsonmap=m.map2json(mapcode)
    with open(scriptpath,'r',encoding='utf-8') as file:
        commands=file.readlines()
        count = 0
        for command in commands:
            # 拆分命令关键词
            command=command.strip('\n')
            command_set=command.split(' ')
            if '' in command_set:
                command_set.remove('')
            # print(command_set)
             # 判断指令类别

            if len(command_set)>=3:
                command_category=command_set[0]
                # 非常蠢的写法，等函数改成依靠json传参之后改
                if command_category=='修改' and command_set[1]=='玩家':
                    index=int(command_set[2])-1
                    name=command_set[3]
                    team=int(command_set[7])
                    flagnum = -10
                    computer_n = command_set[5]
                    cntoi={
                        '休闲':255,
                        '普通':1,
                        '困难':2,
                        '疯狂':3,
                    }
                    computer=cntoi[computer_n]
                    jsonmap=e.setPlayer(jsonmap,index,name,team,flagnum,computer)
                if command_category == '删除' and command_set[1] == '玩家':
                    jsonmap=e.removePlayer(jsonmap,int(command_set[2])-count)
                    count+=1



    newmap=m.json2map(jsonmap)
    return newmap

newmap="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"

print(readScript(newmap,'change01.txt'))