import json
import os
import NSMC.plugins.clash_royale.api_request as api_request

path = ".\\NSMC\\plugins\\clash_royale\\player.json"
preinfo_path=".\\NSMC\\plugins\\clash_royale\\preinfo.json"

accept_prefile_args=["player_name"]

def checkfile():
    if not os.path.isfile(path):
        open(path, "w", encoding="utf-8").close()


def loadfile() -> list:
    default_dict = []

    checkfile()

    with open(path, 'r', encoding="utf-8") as file:
        try:
            loader = json.load(file)
        except:
            loader = default_dict

    return loader


def savefile(save: list):
    with open(path, 'w', encoding="utf-8") as file:
        json.dump(save, file, indent=4, ensure_ascii=False)


def load_player_id(user_id: int):
    file_list = loadfile()
    user_id_list = [content.get("user_id") for content in file_list]
    try:
        pos = user_id_list.index(user_id)
        return file_list[pos]["player_id"]
    except:
        return None


def remove_player_id(user_id: int) -> bool:
    if load_player_id(user_id) is not None:
        file_list = loadfile()
        user_id_list = [content.get("user_id") for content in file_list]
        pos = user_id_list.index(user_id)
        file_list.pop(pos)
        savefile(file_list)
        return True
    else:
        return False


def save_player_id(user_id: int, player_id: str) -> bool:
    if load_player_id(user_id) is None:
        file_list = loadfile()
        file_list.append({"user_id": user_id, "player_id": player_id})
        savefile(file_list)
        return True
    else:
        return False

def load_player_clan_id(user_id: int):
    file_list = loadfile()
    user_id_list = [content.get("user_id") for content in file_list]
    try:
        pos = user_id_list.index(user_id)
        return file_list[pos]["player_clan_id"]
    except:
        info=await api_request.get_info(load_player_id(user_id))
        if info["status_code"]==200:
            clan = info.get("clan")
            if type(clan) == dict:
                clan_tag = clan.get("tag")
            else:
                clan_tag = "NOTAG"
            return clan_tag
        else:
            return "\"Network Error\""

def save_player_clan_id(user_id: int, clan_id: str):
    file_list = loadfile()
    user_id_list = [content.get("user_id") for content in file_list]
    try:
        pos = user_id_list.index(user_id)
        file_list[pos]["player_clan_id"]=clan_id
    except:
        return None


def checkprefile():
    if not os.path.isfile(preinfo_path):
        open(preinfo_path, "w", encoding="utf-8").close()


def loadprefile() -> list:
    default_dict = []

    checkprefile()

    with open(preinfo_path, 'r', encoding="utf-8") as file:
        try:
            loader = json.load(file)
        except:
            loader = default_dict

    return loader


def saveprefile(save: list):
    with open(preinfo_path, 'w', encoding="utf-8") as file:
        json.dump(save, file, indent=4, ensure_ascii=False)

async def save_player_preinfo(player_id: str ,**kwargs):
    file_list = loadprefile()
    other_arg=kwargs
    player_id_list = [content.get("player_id") for content in file_list]
    try:
        pos = player_id_list.index(player_id)
        for arg in other_arg:
            if arg in accept_prefile_args:
                file_list[pos][arg]=other_arg[arg]
            else:
                print(f"[clash_royale] {arg} is not accept in prefile! Check config.py to change it!")
        saveprefile(file_list)
    except:
        file_list.append({"player_id": player_id})
        for arg in other_arg:
            if arg in accept_prefile_args:
                file_list[pos][arg]=other_arg[arg]
            else:
                print(f"[clash_royale] {arg} is not accept in prefile! Check config.py to change it!")
        saveprefile(file_list)

def remove_player_preinfo(player_id: str) -> bool:#I don't know why I add this. May be Ctrl-C Crtl-V?
    if load_player_name(player_id) is not None:
        file_list = loadprefile()
        player_id_list = [content.get("player_id") for content in file_list]
        pos = player_id_list.index(player_id)
        file_list.pop(pos)
        saveprefile(file_list)
        return True
    else:
        return False

async def load_player_name(player_id: str):
    file_list = loadprefile()
    player_id_list = [content.get("player_id") for content in file_list]
    try:
        pos = player_id_list.index(player_id)
        return file_list[pos].get("player_name","无名称")
    except:
        info=await api_request.get_info(player_id)
        if info["status_code"]==200:
            return info.get("name", "无名称")
        else:
            return "\"Network Error\""
