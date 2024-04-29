import requests
from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent,MessageSegment

import NSMC.plugins.clash_royale.api_request as api_request
import NSMC.plugins.clash_royale.config as config
import NSMC.plugins.clash_royale.text_combine as text_combine
import NSMC.plugins.clash_royale.lang as lang

player_token = "#C8CL8CV0Q"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjI5NzE1MzM4LTBmOTQtNDJmMy1iYWMwLWQ0MWIxM2ZjOTAyYyIsImlhdCI6MTY5NTEzOTY1NCwic3ViIjoiZGV2ZWxvcGVyLzJjMjFkNjFmLWY1ZmItNjUxYy00Nzk3LWI1YWE2YWM0ZWM3MCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMTEuMTgwLjE5Mi4xNjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.0UFkl5hTw0daqYCamF1jG9_jKWG25DhzPuQ4CSlF0t26W5Ro5VnOLG1B2Ght719icHSvABer-yqpDp0CoqJiTQ"  # this is token for server
header = {"Authorization": "Bearer " + token, "content-type": "application/json; charset=utf-8"}

replace_token = player_token.replace("#", "%23")


async def is_user(event: PrivateMessageEvent) -> bool:
    return event.user_id == 1055450040


async def command(event: GroupMessageEvent | PrivateMessageEvent) -> bool:
    return str(event.message).startswith("/cr")


get_msg = on_message(rule=is_user)
cmd = on_message(rule=command)


@get_msg.handle()
async def _(event: PrivateMessageEvent):
    if str(event.message) == "获取宝箱列表":
        chest = requests.get("https://api.clashroyale.com/v1/players/" + replace_token + "/upcomingchests",
                             headers=header)
        if chest.status_code == 200:
            await get_msg.finish(chest.text)
        else:
            await get_msg.finish(str(chest.status_code))


def check_has_id(user_id: int):
    if config.load_player_id(user_id) is None:
        return False
    else:
        return True


@cmd.handle()
async def _(event: GroupMessageEvent | PrivateMessageEvent):
    msg = str(event.message)
    msg_dict = msg.split(' ')
    if len(msg_dict) > 1:
        if len(msg_dict) > 2:
            if msg_dict[-1] == "-help":
                dict1 = msg_dict[1]
                main_text = f"/cr {dict1}：\n"
                match msg_dict[1]:
                    case "check" | "检查":
                        await cmd.finish(f"{main_text}本指令用于检查您绑定的玩家标签。\n使用方法：/cr {dict1}")
                    case "bind" | "绑定":
                        await cmd.finish(
                            f"{main_text}本指令用于将玩家标签绑定至您的QQ账户（可以跨群使用）。\n使用方法：/cr {dict1} 玩家标签\n例：/cr {dict1} #12345678")
                    case "unbind" | "解绑":
                        await cmd.finish(f"{main_text}本指令用于将玩家标签解除绑定您的QQ账户。\n使用方法：/cr {dict1}")
                    case "info" | "信息":
                        await cmd.finish(f"{main_text}本指令用于查看您或他人的玩家数据。\n使用方法：/cr {dict1}或/cr {dict1} #12345678")
                    case "chest" | "宝箱列表" | "箱子列表" | "箱子" | "宝箱":
                        await cmd.finish(
                            f"{main_text}本指令用于查看您或他人之后的宝箱列表（包含最近的8个宝箱和稀有宝箱的次数）。\n使用方法：/cr {dict1}或/cr {dict1} #12345678")
                    case "clan" | "部落":
                        await cmd.finish(
                            f"{main_text}本指令用于查看您或他人的所在部落信息。\n使用方法：/cr {dict1}或/cr {dict1} #12345678")
                    case "help" | "帮助":
                        await cmd.finish(f"{main_text}本指令用于展示本插件的使用说明。\n使用方法：/cr {dict1}")
                    case _:
                        await cmd.finish("本指令不存在，请使用/cr help或/cr 帮助")
            if msg_dict[-1] == "-json":
                dict1 = msg_dict[1]
                main_text = f"/cr {dict1}：\n"
                match msg_dict[1]:
                    case "check" | "检查" | "bind" | "绑定" | "unbind" | "解绑" | "help" | "帮助":
                        await cmd.finish("本指令没有json返回")
                    case "info" | "信息":
                        get = config.load_player_id(event.user_id)
                        request = await api_request.get_info(get)
                        request.pop("status_code")
                        request.pop("clan_tag")
                        await cmd.finish(f"{request}")
                    case "chest" | "宝箱列表" | "箱子列表" | "箱子" | "宝箱":
                        get = config.load_player_id(event.user_id)
                        request = await api_request.get_chest(get)
                        request.pop("status_code")
                        request.pop("player_name")
                        await cmd.finish(f"{request}")
                    case _:
                        await cmd.finish("本指令不存在，请使用/cr help或/cr 帮助")
        match msg_dict[1]:
            case "check" | "检查":
                if not check_has_id(event.user_id):
                    await cmd.finish("您还未绑定玩家标签！\n使用/cr bind 玩家标签 或/cr 绑定 玩家标签 来绑定！")
                else:
                    await cmd.finish("已绑定玩家" + await config.load_player_name(config.load_player_id(event.user_id))+config.load_player_id(event.user_id))
            case "bind" | "绑定":
                if len(msg_dict) >= 3:
                    player_id = msg_dict[2]
                    if player_id.startswith('#'):
                        player_name = await api_request.get_info(player_id)
                        match player_name["status_code"]:
                            case 200:
                                if config.save_player_id(event.user_id, player_id):
                                    config.save_player_clan_id(event.user_id, player_name["clan_tag"])
                                    await cmd.finish("标签验证成功！\n已绑定" + str(player_name["name"]) + "！")
                                else:
                                    await cmd.finish("标签验证成功！\n您已经绑定标签或者数据存储出现问题！")
                            case _:
                                await cmd.finish(str(player_name["status_code"]) + "错误！\n标题：" + str(
                                    player_name.get("reason", "Error")) + "\n内容：" + str(
                                    player_name.get("message", "None")))
                    else:
                        await cmd.finish("玩家标签不合法！")
                else:
                    await cmd.finish("绑定指令为/cr bind 玩家标签 或/cr 绑定 玩家标签")
            case "unbind" | "解绑":
                if config.remove_player_id(event.user_id):
                    await cmd.finish("标签解绑成功！")
                else:
                    await cmd.finish("解绑出现问题！")
            case "info" | "信息":
                if len(msg_dict)==2:
                    if check_has_id(event.user_id):
                        get = config.load_player_id(event.user_id)
                        player_name = await api_request.get_info(get)
                        match player_name["status_code"]:
                            case 200:
                                config.save_player_clan_id(event.user_id, player_name["clan_tag"])
                                await cmd.finish(await text_combine.info(player_name))
                            case _:
                                await cmd.finish(str(player_name["status_code"]) + "错误！\n标题：" + str(
                                    player_name.get("reason", "Error")) + "\n内容：" + str(
                                    player_name.get("message", "None")))
                    else:
                        await cmd.finish("您还未绑定玩家标签！\n使用/cr bind 玩家标签 或/cr 绑定 玩家标签 来绑定！\n您也可以直接添加玩家标签查询玩家数据！")
                elif len(msg_dict)>=3:
                    player_id=msg_dict[2]
                    if player_id.startswith('#'):
                        player_name = await api_request.get_info(player_id)
                        match player_name["status_code"]:
                            case 200:
                                await cmd.finish(await text_combine.info(player_name))
                            case _:
                                await cmd.finish(str(player_name["status_code"]) + "错误！\n标题：" + str(
                                    player_name.get("reason", "Error")) + "\n内容：" + str(
                                    player_name.get("message", "None")))
                    else:
                        await cmd.finish("玩家标签不合法！")
            case "chest" | "宝箱列表" | "箱子列表" | "箱子" | "宝箱":
                if len(msg_dict)==2:
                    if check_has_id(event.user_id):
                        get = config.load_player_id(event.user_id)
                        player_name = await api_request.get_chest(get)
                        match player_name["status_code"]:
                            case 200:
                                await cmd.finish(await text_combine.chest(player_name))
                            case _:
                                await cmd.finish(str(player_name["status_code"]) + "错误！\n标题：" + str(
                                    player_name.get("reason", "Error")) + "\n内容：" + str(
                                    player_name.get("message", "None")))
                    else:
                        await cmd.finish("您还未绑定玩家标签！\n使用/cr bind 玩家标签 或/cr 绑定 玩家标签 来绑定！\n您也可以直接添加玩家标签查询玩家宝箱列表！")
                elif len(msg_dict)>=3:
                    player_id = msg_dict[2]
                    if player_id.startswith("#"):
                        player_info = await api_request.get_chest(player_id)
                        match player_info["status_code"]:
                            case 200:
                                await cmd.finish(await text_combine.chest(player_info))
                            case _:
                                await cmd.finish(str(player_info["status_code"]) + "错误！\n标题：" + str(
                                    player_info.get("reason", "Error")) + "\n内容：" + str(
                                    player_info.get("message", "None")))
                    else:
                        await cmd.finish("玩家标签不合法！")
            case "clan" | "部落":#Finally I add this! FINALLY!!!
                if len(msg_dict) == 2:
                    if check_has_id(event.user_id):
                        get = config.load_player_clan_id(event.user_id)
                        if get=="NOTAG":
                            cmd.finish("无部落\n加入部落，收获奖励和欢乐！")
                        clan_info = await api_request.get_clan(get)
                        match clan_info["status_code"]:
                            case 200:
                                await cmd.finish(await text_combine.clan(clan_info))
                            case _:
                                await cmd.finish(str(clan_info["status_code"]) + "错误！\n标题：" + str(
                                    clan_info.get("reason", "Error")) + "\n内容：" + str(
                                    clan_info.get("message", "None")))
                    else:
                        await cmd.finish(
                            "您还未绑定玩家标签！\n使用/cr bind 玩家标签 或/cr 绑定 玩家标签 来绑定！\n您也可以直接添加部落标签查询部落数据！")
                elif len(msg_dict) >= 3:
                    clan_id = msg_dict[2]
                    if clan_id.startswith("#"):
                        clan_info = await api_request.get_clan(clan_id)
                        match clan_info["status_code"]:
                            case 200:
                                await cmd.finish(await text_combine.clan(clan_info))
                            case _:
                                await cmd.finish(str(clan_info["status_code"]) + "错误！\n标题：" + str(
                                    clan_info.get("reason", "Error")) + "\n内容：" + str(
                                    clan_info.get("message", "None")))
                    else:
                        await cmd.finish("部落标签不合法！")

            case "help" | "帮助":
                help_text = "皇室战争信息查询工具 by 钢铁小草（zhangshaoxuan70）\n绑定标签：/cr bind 玩家标签（/cr 绑定 玩家标签）\n检查绑定：/cr check（/cr 检查）\n解除绑定：/cr unbind（/cr 解绑）\n查询信息：/cr info（/cr 信息）（可加他人标签）\n查询宝箱：/cr chest（/cr 宝箱列表/箱子列表/箱子/宝箱）（可加他人标签）\n查询部落信息：/cr clan（/cr 部落）（可加部落标签）\n可在任意指令后添加-help获取该指令的详细说明"
                if event.message_type == "private" and event.user_id == 1055450040:
                    help_text += "\n/cr lang\n"
                help_text += "Github：https://github.com/zhangshaoxuan70/None-Bot-Clah-Royale-Api\nQQ：1055450040"
                await cmd.finish(help_text)
            case "lang":
                if event.message_type == "private" and event.user_id == 1055450040:
                    text_combine.load_dict()
                    await cmd.finish(str(len(text_combine.dictionary)))
            case _:
                await cmd.finish("参数错误，请查看/cr help或/cr 帮助")
    else:
        await cmd.finish("请查看/cr help或/cr 帮助 以查看参数说明")
