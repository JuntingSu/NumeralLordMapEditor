import json
import zlib
import base64
from map_editor import TEXT_VALUE, INT_VALUE, BOOL_VALUE


def str_to_bytes(strs):
    newbyte = strs.encode('utf-8')
    byte_length = len(newbyte).to_bytes(1, "little")
    return byte_length + newbyte


def decodemap(mapcode):
    decoded_data = base64.b64decode(mapcode)
    bstr = zlib.decompress(decoded_data)
    return bstr


def readstr(data, index):
    length = data[index]
    if length >= 128:
        index += 1
        if data[index] == 2:
            length = 256
    content = data[index + 1:length + index + 1]
    # print(content.decode('utf-8', 'ignore'))
    # print(f"index:{index}")
    # print(f"length:{length}")
    return [content.decode('utf-8', 'ignore'), index + length + 1]


def readint(data, length, index):
    content = data[index:length + index]
    value = int.from_bytes(content, byteorder='little')
    return [value, index + length]


def generate(mapsettings) -> str:
    # 读取原始数据
    version = mapsettings['version']
    title = mapsettings['title']
    description = mapsettings['description']
    author = mapsettings['author']
    length = mapsettings['length']
    width = mapsettings['width']
    random_seat = mapsettings['random_seat']
    cycle_map = mapsettings['cycle_map']
    fog_mode = mapsettings['fog_mode']
    star_mode = mapsettings['star_mode']
    star_turn_three = mapsettings['star_turn_three']
    star_turn_two = mapsettings['star_turn_two']
    time_per_turn = mapsettings['time_per_turn']
    time_total = mapsettings['time_total']
    player = mapsettings['player_num']
    battlefield = mapsettings['battlefield']
    player_list = mapsettings['player_list']

    # 基本信息
    version_byte = version.to_bytes(4, byteorder="little")
    title_byte = str_to_bytes(title)
    description_byte = str_to_bytes(description)
    author_byte = str_to_bytes(author)

    # 时间有问题,暂时使用0填充
    date = int(365 * 86400 * 1e7)
    date_byte = date.to_bytes(8, byteorder="little")

    # 也没研究明白,先保留
    magic_number1 = 3
    magic_number1_byte = magic_number1.to_bytes(4, byteorder="little")

    # 长宽
    length_byte = length.to_bytes(4, byteorder="little")
    width_byte = width.to_bytes(4, byteorder="little")

    # 也没研究明白,先保留
    magic_number2 = 0
    magic_number2_byte = magic_number2.to_bytes(4, byteorder="little")

    # 随机出生和循环地图
    random_seat_byte = random_seat.to_bytes(1, byteorder="little")
    cycle_map_byte = cycle_map.to_bytes(1, byteorder="little")

    # 星星模式,太杂了单独写一下
    blank1 = 0
    blank1_byte = blank1.to_bytes(1, byteorder="little")
    star_turn_three_byte = star_turn_three.to_bytes(1, byteorder="little")
    star_turn_two_byte = star_turn_two.to_bytes(1, byteorder="little")
    star_mode_byte = star_mode.to_bytes(1, byteorder="little")

    star_mode_final_byte = blank1_byte + star_turn_three_byte + star_turn_two_byte + star_mode_byte

    # 也没研究明白,先保留
    magic_number3 = 2
    magic_number3_byte = magic_number3.to_bytes(4, byteorder="little")

    # 面积
    area = length * width
    area_byte = area.to_bytes(4, byteorder="little")

    # 地图信息
    map_array = bytearray(area * 4)
    for i in range(area):
        map_array[i * 4] = battlefield[i][0]
        map_array[i * 4 + 1] = battlefield[i][1]
        map_array[i * 4 + 2] = battlefield[i][2]
        map_array[i * 4 + 3] = 0
    # for i in range(player):
    #     for position in soldier[i]:
    #         map_array[position[0] * 4 + 1] = i + 1
    #         map_array[position[0] * 4 + 2] = position[1]
    map_byte = bytes(map_array)

    # 也没研究明白,先保留
    magic_number4 = bytearray(24)
    magic_number4[12] = 255
    magic_number4[13] = 3
    magic_number4[20] = 1
    magic_number4_byte = bytes(magic_number4)

    # 迷雾
    fog_byte = fog_mode.to_bytes(1, byteorder="little")

    # 步时和局时
    time_per_turn_byte = time_per_turn.to_bytes(4, byteorder="little")
    time_total_byte = time_total.to_bytes(4, byteorder="little")

    # 玩家数量
    player_num_byte = player.to_bytes(4, byteorder="little")

    # 玩家信息
    player_byte = bytes()
    for players in player_list:
        player_seat_byte = players['seat'].to_bytes(1, byteorder="little")
        player_team_byte = players['team'].to_bytes(4, byteorder="little")
        player_name_byte = str_to_bytes(players['name'])
        player_compu_byte = players['computer'].to_bytes(4, byteorder="little")
        player_flag_byte = players['flag'].to_bytes(4, byteorder="little")
        player_byte += player_seat_byte + player_team_byte + player_name_byte + player_compu_byte \
                       + player_flag_byte

    # show(player_byte)
    modified_byte = version_byte + title_byte + description_byte + author_byte + \
                    date_byte + player_num_byte + width_byte + length_byte + \
                    magic_number2_byte + random_seat_byte + cycle_map_byte + \
                    star_mode_final_byte + magic_number3_byte + area_byte + \
                    map_byte + magic_number4_byte + fog_byte + time_per_turn_byte + \
                    time_total_byte + player_num_byte + player_byte

    compressed_data = zlib.compress(modified_byte)
    base_data = base64.b64encode(compressed_data)
    return base_data.decode('utf-8')


def read(bstr) -> json:
    index = 0
    [version, index] = readint(bstr, 4, index)
    [title, index] = readstr(bstr, index)
    [description, index] = readstr(bstr, index)

    [author, index] = readstr(bstr, index)
    [time, index] = readint(bstr, 8, index)
    [player_num, index] = readint(bstr, 4, index)
    [width, index] = readint(bstr, 4, index)
    [length, index] = readint(bstr, 4, index)
    [blank, index] = readint(bstr, 4, index)
    [randon_seat, index] = readint(bstr, 1, index)
    [cycle_map, index] = readint(bstr, 1, index)
    [blank, index] = readint(bstr, 1, index)
    [star_3, index] = readint(bstr, 1, index)
    [star_2, index] = readint(bstr, 1, index)
    [star_mode, index] = readint(bstr, 1, index)
    [blank, index] = readint(bstr, 4, index)
    [area, index] = readint(bstr, 4, index)

    battlefield = [[] for _ in range(area)]
    # terrain = [None for _ in range(area)]
    # soldiers = []
    for i in range(area):
        [terr, index] = readint(bstr, 1, index)
        [belonging, index] = readint(bstr, 1, index)
        [strength, index] = readint(bstr, 1, index)
        [blank, index] = readint(bstr, 1, index)
        # terrain[i] = terr
        # if belonging <= player_num:
        #     soldier={
        #         "position":i,
        #         "belonging":belonging,
        #         "strength":strength
        #     }
        #     soldiers.append(soldier)

        battlefield[i].append(terr)
        battlefield[i].append(belonging)
        battlefield[i].append(strength)

        # print(i)

    [blank, index] = readint(bstr, 24, index)
    [fog_mode, index] = readint(bstr, 1, index)
    [time_per_turn, index] = readint(bstr, 4, index)
    [time_total, index] = readint(bstr, 4, index)
    [blank, index] = readint(bstr, 4, index)

    player_list = [{} for _ in range(player_num)]

    for j in range(player_num):
        [seat, index] = readint(bstr, 1, index)
        [team, index] = readint(bstr, 4, index)
        [name, index] = readstr(bstr, index)
        [computer, index] = readint(bstr, 4, index)
        [flag, index] = readint(bstr, 4, index)
        player_list[j].update({"name": name, "team": team, "computer": computer, "seat": seat, "flag": flag})

    mapfile = {}
    mapfile.update(
        {
            "version": version,
            "title": title,
            "description": description,
            "author": author,
            "length": length,
            "width": width,
            "random_seat": randon_seat,
            "cycle_map": cycle_map,
            "fog_mode": fog_mode,
            "star_mode": star_mode,
            "star_turn_three": star_3,
            "star_turn_two": star_2,
            "time_per_turn": time_per_turn,
            "time_total": time_total,
            "player_num": player_num,
            "player_list": player_list,
            "battlefield": battlefield
        }
    )
    mapjson = json2str(mapfile)
    return mapjson


def json2str(dict: dict) -> str:
    player_int_elements = ['team', 'computer', 'seat', 'flag']
    jsonstr = ""
    jsonstr += "{\n"
    for item in TEXT_VALUE:
        jsonstr += f"\t\"{item}\": \"{dict[item]}\",\n"
    for item in INT_VALUE:
        jsonstr += f"\t\"{item}\": {dict[item]},\n"
    for item in BOOL_VALUE:
        jsonstr += f"\t\"{item}\": {dict[item]},\n"

    jsonstr += f"\t\"player_num\": {dict['player_num']},\n"
    jsonstr += "\t\"player_list\": [\n"
    for i in range(dict['player_num']):
        jsonstr += "\t\t{\n"
        jsonstr += f"\t\t\t\"name\": \"{dict['player_list'][i]['name']}\",\n"
        for item in player_int_elements:
            jsonstr += f"\t\t\t\"{item}\": {dict['player_list'][i][item]}"
            if not item == player_int_elements[-1]:
                jsonstr += ","
            jsonstr += "\n"
        jsonstr += "\t\t}"
        if i == dict['player_num'] - 1:
            jsonstr += "\n"
        else:
            jsonstr += ",\n"
    jsonstr += "\t],\n"

    jsonstr += "\t\"battlefield\": [\n"
    for l in range(dict['length']):
        jsonstr += "\t\t"
        for w in range(dict['width']):
            jsonstr += f"["
            jsonstr += f"{dict['battlefield'][l * dict['width'] + w][0]},"
            jsonstr += f"{dict['battlefield'][l * dict['width'] + w][1]},"
            jsonstr += f"{dict['battlefield'][l * dict['width'] + w][2]}]"
            if not (l == dict['length'] - 1 and w == dict['width'] - 1):
                jsonstr += ","
        jsonstr += "\n"
    jsonstr += "\t]\n"

    jsonstr += "}"

    return jsonstr


def showbindata(mapcode):
    bina = decodemap(mapcode)
    print(len(bina))
    for i in range(len(bina)):
        print("%.3d" % bina[i], end=" ")
        if i % 8 == 7:
            print("|", end="")
        if i % 32 == 31:
            print()
    # print(bina)


def json2map(jsonmap: json) -> str:
    mapstr = generate(jsonmap)
    return mapstr


def map2json(mapcode: str) -> json:
    bcode = decodemap(mapcode)
    strmap = read(bcode)
    jsonmap = json.loads(strmap)
    return jsonmap


def savemap(jsonmap: json, filepath: str):
    strmap = json2str(jsonmap)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(strmap)


def readmap(filepath: str) -> json:
    with open(filepath, 'r', encoding='utf-8') as file:
        jsonmap = json.load(file)
    return jsonmap


__all__ = ['json2map', 'map2json', 'json2str', 'savemap', 'readmap']

if __name__ == "__main__":
    pass
