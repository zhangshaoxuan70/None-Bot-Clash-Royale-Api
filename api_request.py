import json
import requests
from . import config

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImRlZDgxZGNkLTVmYjItNDBlYy1iZDQ5LTMzZDJjNGJkMTFhOSIsImlhdCI6MTcxNTc4NTc0Mywic3ViIjoiZGV2ZWxvcGVyLzJjMjFkNjFmLWY1ZmItNjUxYy00Nzk3LWI1YWE2YWM0ZWM3MCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMTEuMTgwLjE5Mi4xNjgiLCIxMTEuNjcuMTkzLjg5Il0sInR5cGUiOiJjbGllbnQifV19.vJeCmsVNalyYrujzR4AYUoX3RmkCUkBvFDHMigEGEgE9Lkz8uXVIx9TuP2JjTXCm40Bpnb4h_OjseiThz6Trlw"  # this is token for server
header = {"Authorization": "Bearer " + token, "content-type": "application/json; charset=utf-8"}


async def get_info(player_id: str) -> dict:
    trans_player_id = player_id.replace("#", "%23")
    info = requests.get(f"https://api.clashroyale.com/v1/players/{trans_player_id}", headers=header)
    reply = json.loads(info.content.decode())
    reply["status_code"] = info.status_code
    if info.status_code==200:
        clan = reply.get("clan")
        if type(clan) == dict:
            clan_tag = clan.get("tag")
        else:
            clan_tag="NOTAG"
        await config.save_player_preinfo(player_id,player_name=reply.get("name", "无名称"))
    reply["clan_tag"]=clan_tag
    return reply


async def get_chest(player_id: str) -> dict:
    trans_player_id = player_id.replace("#", "%23")
    chest = requests.get(f"https://api.clashroyale.com/v1/players/{trans_player_id}/upcomingchests", headers=header)
    reply = json.loads(chest.content.decode())
    reply["status_code"] = chest.status_code
    # info = requests.get(f"https://api.clashroyale.com/v1/players/{trans_player_id}", headers=header)
    # info_reply = json.loads(info.content.decode())
    # if info.status_code==200:
    #     reply["player_name"] = info_reply.get("name", "无名称")
    # else:
    #     reply["player_name"] = trans_player_id
    reply["player_name"]=await config.load_player_name(player_id)
    return reply

async def get_clan(clan_id: str) -> dict:
    trans_clan_id = clan_id.replace("#", "%23")
    clan = requests.get(f"https://api.clashroyale.com/v1/clans/{trans_clan_id}", headers=header)
    reply = json.loads(clan.content.decode())
    reply["status_code"] = clan.status_code
    return reply