import json
import threading
import tkinter as tk
import map_to_json as m
import map_editor as me
from math import sqrt,log2

def drawTile(center,canvas,tilescale,color):
    canvas.create_polygon(center[0], center[1] - tilescale,
                       center[0] - tilescale * sqrt(3) / 2, center[1] - tilescale / 2,
                       center[0] - tilescale * sqrt(3) / 2, center[1] + tilescale / 2,
                       center[0], center[1] + tilescale,
                       center[0] + tilescale * sqrt(3) / 2, center[1] + tilescale / 2,
                       center[0] + tilescale * sqrt(3) / 2, center[1] - tilescale / 2,fill=color,outline='black')

def showTerrain(jsonmap:json):
    maxheight=800

    tileheight=jsonmap['length']
    tilewidth=jsonmap['width']
    tilescale = 800/(tileheight+1)*2/3
    height=tilescale*(tileheight+1)*3/2
    root=tk.Tk()
    root.title(f"预览地形信息-{jsonmap['title']}-{jsonmap['author']}")
    map=tk.Canvas(root,height=tilescale*(tileheight+1)*3/2,width=tilescale*(tilewidth+1)*sqrt(3))
    grid=[]
    for i in range(tileheight):
        for j in range(tilewidth):
            grid.append([tilescale*(j+0.5+0.5*(i%2))*sqrt(3),height-tilescale*(1.5*i+1)])
    colorlist=['black','gray','#F16B6B','#A9813D','#337AC1']
    for i in range(len(grid)):
        drawTile(grid[i],map,tilescale,colorlist[jsonmap['battlefield'][i][0]])

    map.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
    # root.update()
def showPlayer(jsonmap:json):
    root=tk.Tk()
    root.title(f"预览势力信息-{jsonmap['title']}-{jsonmap['author']}")
    maxline=24
    rows=min(jsonmap['player_num'],maxline)+1
    columns=5*int(jsonmap['player_num']/maxline+1)
    textlist=['seat','name','team','computer','flag']
    textlist_CN=['序号','势力名','队伍','电脑','flag']

    textcomputer={
        255:'休闲',
        1:'普通',
        2:'困难',
        3:'疯狂'
    }


    w=[4,14,4,4,6]
    # 创建表格抬头
    for i in range(columns):
        cell = tk.Entry(root, relief="ridge", width=w[i%5],state='readonly')
        cell.insert(tk.END, textlist_CN[i%5])
        cell.grid(row=0, column=i, sticky="nsew")
    # 写入内容
    for i in range(1,rows):
        for j in range(columns):
            # 创建一个输入框作为单元格
            cell = tk.Entry(root, relief="ridge", width=w[j%5])
            if i-1+maxline*int(j/5)<jsonmap['player_num']:
                if j%5==2:
                    cell.insert(tk.END, str(int(log2(jsonmap['player_list'][i-1+maxline*int(j/5)][textlist[j%5]])+1)))
                elif j%5==3:
                    cell.insert(tk.END, textcomputer[jsonmap['player_list'][i-1+maxline*int(j/5)][textlist[j%5]]])
                else:
                    cell.insert(tk.END, jsonmap['player_list'][i-1+maxline*int(j/5)][textlist[j%5]])
            else:
                cell.insert(tk.END, '')
            cell.grid(row=i, column=j, sticky="nsew")

    # 添加保存按钮
    save_button = tk.Button(root, text="删除末位角色", command=lambda: remove(jsonmap,root))
    save_button.grid(row=rows, column=0, columnspan=columns, sticky="nsew")

    root.update()

    root.mainloop()

def save_data():
    # 这里需要实现保存数据的逻辑
    print("保存数据逻辑待实现")




def remove(jsonmap:json,tkroot:tk):
    print("deleting")
    newmap = me.removeLastPlayer(jsonmap)
    jsonmap.update(newmap)
    tkroot.update_idletasks()
    print(jsonmap)



if __name__=="__main__":
    mapcode=input("请输入地图码")
    map=m.map2json(mapcode)
    thread_1=threading.Thread(target=showTerrain(map))
    thread_2=threading.Thread(target=showPlayer(map))

    # thread_1.start()
    thread_2.start()