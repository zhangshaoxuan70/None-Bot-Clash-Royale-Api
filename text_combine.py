from . import lang
import os
arena_en_dict = ["Arena 1", "Arena 2", "Arena 3", "Arena 4", "Arena 5", "Arena 6", "Arena 7", "Arena 8", "Arena 9",
                 "Arena 10", "Arena 11", "Arena 12", "Arena 13", "Arena 14", "Arena 15", "Arena 16", "Arena 17",
                 "Arena 18", "Arena 19", "Arena 20", "Arena 21", "Arena 22", "Arena 23"]
arena_zh_dict = ["1阶竞技场", "2阶竞技场", "3阶竞技场", "4阶竞技场", "5阶竞技场", "6阶竞技场", "7阶竞技场", "8阶竞技场",
                 "9阶竞技场", "10阶竞技场", "11阶竞技场", "12阶竞技场", "13阶竞技场", "14阶竞技场", "15阶竞技场",
                 "16阶竞技场", "17阶竞技场", "18阶竞技场", "19阶竞技场", "20阶竞技场", "21阶竞技场", "22阶竞技场",
                 "23阶竞技场"]

role_en_dict = ["leader", "coLeader", "elder", "member"]
role_zh_dict = ["首领", "副首领", "长老", "成员"]

chest_en_dict = ["Wooden Chest", "Silver Chest", "Golden Chest", "Magical Chest", "Giant Chest", "Mega Lightning Chest",
                 "Epic Chest", "Legendary Chest", "Gold Crate", "Plentiful Gold Crate", "Overflowing Gold Crate",
                 "Royal Wild Chest", "Tower Troop Chest"]
chest_zh_dict = ["木质宝箱", "白银宝箱", "黄金宝箱", "神奇宝箱", "巨型宝箱", "超级雷电宝箱", "史诗宝箱", "传奇宝箱",
                 "普通金币箱", "丰厚金币箱", "满溢金币箱", "皇室外卡宝箱", "皇家塔部队宝箱"]

card_en_dict = ["Knight", "Archers", "Goblins", "Giant", "P.E.K.K.A", "Minions", "Balloon", "Witch", "Barbarians",
                "Golem", "Skeletons", "Valkyrie", "Skeleton Army", "Bomber", ]

mainpath=os.path.split(__file__)[0]

dictionary=lang.loadfile(mainpath)
dictionary_ori=[content[0] for content in dictionary]
dictionary_replace=[content[1] for content in dictionary]

def load_dict():
    global dictionary
    dictionary=lang.loadfile(mainpath)
    global dictionary_ori
    dictionary_ori=[content[0] for content in dictionary]
    global dictionary_replace
    dictionary_replace=[content[1] for content in dictionary]

def set_multi(original):
    try:
        pos=dictionary_ori.index(original)
        return dictionary_replace[pos]
    # for i in range(len(org_list)):
    #     if original == org_list[i]:
    #         original = place_list[i]
    #         return original
    # return original
    except:
        return original

def culcate_kingLevel(expLevel: int) -> int:
    match expLevel:
        case expLevel if expLevel in range(1, 2):
            kingLevel = 1
        case expLevel if expLevel in range(2, 3):
            kingLevel = 2
        case expLevel if expLevel in range(3, 5):
            kingLevel = 3
        case expLevel if expLevel in range(5, 7):
            kingLevel = 4
        case expLevel if expLevel in range(7, 10):
            kingLevel = 5
        case expLevel if expLevel in range(10, 14):
            kingLevel = 6
        case expLevel if expLevel in range(14, 18):
            kingLevel = 7
        case expLevel if expLevel in range(18, 22):
            kingLevel = 8
        case expLevel if expLevel in range(22, 26):
            kingLevel = 9
        case expLevel if expLevel in range(26, 30):
            kingLevel = 10
        case expLevel if expLevel in range(30, 34):
            kingLevel = 11
        case expLevel if expLevel in range(34, 38):
            kingLevel = 12
        case expLevel if expLevel in range(38, 42):
            kingLevel = 13
        case expLevel if expLevel in range(42, 54):
            kingLevel = 14
        case expLevel if expLevel in range(54, 71):
            kingLevel = 15
        case _:
            kingLevel = -1
    return kingLevel


async def info(player_list: dict) -> str:
    tag = player_list["tag"]
    name = player_list.get("name", "无名称")
    expLevel = player_list.get("expLevel", 0)
    kingLevel = culcate_kingLevel(expLevel)
    trophies = player_list.get("trophies", 0)
    bestTrophies = player_list.get("bestTrophies", 0)
    wins = player_list.get("wins", 0)
    battleCount = player_list.get("battleCount", 0)
    threeCrownWins = player_list.get("threeCrownWins", 0)

    role = player_list.get("role", "无身份")  # 需格式化
    role = set_multi(role)

    donations = player_list.get("donations", 0)  # 每周捐赠
    totalDonations = player_list.get("totalDonations", 0)
    clan = player_list.get("clan")
    currentFavouriteCard = player_list.get("currentFavouriteCard")
    if type(clan) == dict:
        clan_name = clan.get("name")
        clan_tag = clan.get("tag")
    else:
        clan_name = "无部落"

    arena_name = player_list.get("arena").get("name")
    arena_name = set_multi(arena_name)

    leagueStatistics = player_list.get("leagueStatistics")
    if type(leagueStatistics) == dict:
        legacy_trophies = leagueStatistics.get("bestSeason").get("trophies")
        legacy_rank = leagueStatistics.get("bestSeason").get("rank")

    currentPathOfLegendSeasonResult = player_list.get("currentPathOfLegendSeasonResult")
    if type(currentPathOfLegendSeasonResult) == dict:
        c_leagueNumber = currentPathOfLegendSeasonResult.get("leagueNumber", 1)
        c_leagueName = f"{c_leagueNumber}级联赛"
        c_trophies = currentPathOfLegendSeasonResult.get("trophies", 0)
        c_rank = currentPathOfLegendSeasonResult.get("rank")
    lastPathOfLegendSeasonResult = player_list.get("lastPathOfLegendSeasonResult")
    if type(lastPathOfLegendSeasonResult) == dict:
        l_leagueNumber = lastPathOfLegendSeasonResult.get("leagueNumber", 1)
        l_leagueName = f"{l_leagueNumber}级联赛"
        l_trophies = lastPathOfLegendSeasonResult.get("trophies", 0)
        l_rank = lastPathOfLegendSeasonResult.get("rank")
    bestPathOfLegendSeasonResult = player_list.get("bestPathOfLegendSeasonResult")
    if type(bestPathOfLegendSeasonResult) == dict:
        b_leagueNumber = bestPathOfLegendSeasonResult.get("leagueNumber", 1)
        b_leagueName = f"{b_leagueNumber}级联赛"
        b_trophies = bestPathOfLegendSeasonResult.get("trophies", 0)
        b_rank = bestPathOfLegendSeasonResult.get("rank")
    if type(currentFavouriteCard)==dict:
        currentFavouriteCard_name=currentFavouriteCard.get("name")

    content = f"玩家数据{name}({tag})\n国王等级：{expLevel}\n"
    if kingLevel != -1:
        content += f"国王塔等级：{kingLevel}\n"
    else:
        content += "你没开挂吧？\n"
    content += f"皇室征程最高奖杯数/当前奖杯数：{bestTrophies}/{trophies}\n皇室征程所在竞技场：{arena_name}\n胜场：{wins}({wins / battleCount:.2%})\n三皇冠胜利次数：{threeCrownWins}({threeCrownWins / battleCount:.2%})\n"
    if type(leagueStatistics) == dict:
        content += f"旧版皇室征程最佳：{legacy_trophies}"
        if legacy_rank is not None:
            content += f"(#{legacy_rank})\n"
        else:
            content += "\n"
    content += f"所在部落：{clan_name}"
    if type(clan) == dict:
        content += f"({clan_tag})\n部落内身份：{role}\n"
    else:
        content += "\n"
    content += f"每周捐赠：{donations}\n捐赠总量：{totalDonations}\n"
    if type(currentPathOfLegendSeasonResult) == dict:
        content += f"当前赛季：{c_leagueName}"
        if c_leagueNumber == 10:
            content += f"(评分：{c_trophies}"
            if c_rank != None:
                content += f"/#{c_rank})\n"
            else:
                content += ")\n"
        else:
            content += "\n"
    if type(lastPathOfLegendSeasonResult) == dict:
        content += f"上一赛季：{l_leagueName}"
        if l_leagueNumber == 10:
            content += f"(评分：{l_trophies}"
            if l_rank != None:
                content += f"/#{l_rank})\n"
            else:
                content += ")\n"
        else:
            content += "\n"
    if type(bestPathOfLegendSeasonResult) == dict:
        content += f"最佳赛季：{b_leagueName}"
        if b_leagueNumber == 10:
            content += f"(评分：{b_trophies}"
            if b_rank is not None:
                content += f"/#{b_rank})\n"
            else:
                content += ")\n"
        else:
            content += "\n"
    if type(currentFavouriteCard)==dict:
        content+=f"近期常用卡牌：{currentFavouriteCard_name}"
    return content

async def clan(clan_list:dict)-> str:
    tag=clan_list["tag"]
    name=clan_list.get("name","无名称")
    clantype=clan_list["type"]
    clantype=set_multi(clantype)

    description=clan_list.get("description","无简介")
    clanScore=clan_list["clanScore"]
    clanWarTrophies=clan_list["clanWarTrophies"]
    location=clan_list.get("location")
    if type(location)==dict:
        location_name=location.get("name")
        location_name=set_multi(location_name)
    requiredTrophies=clan_list["requiredTrophies"]
    donationsPerWeek=clan_list["donationsPerWeek"]
    members=clan_list["members"]

    content=f"部落信息{name}({tag})（成员{members}/50 {members / 50:.2%}）：\n{description}\n部落战奖杯数：{clanWarTrophies}\n位置：{location_name}\n所需奖杯数：{requiredTrophies}\n每周捐赠：{donationsPerWeek}\n部落积分：{clanScore}\n类型：{clantype}"

    return content

async def chest(player_list: dict) -> str:
    chest_dict = player_list["items"]
    player_name=player_list["player_name"]
    content = f"{player_name}的箱子序列：\n"
    content += "最靠前的9个箱子：\n"
    for chest_item in chest_dict:
        index = chest_item.get("index", -1)
        chest_info = set_multi(chest_item.get("name"))
        if index in range(0, 8):
            content += f"{chest_info}，"
        elif index == 8:
            content += f"{chest_info}\n"
        else:
            content += f"{chest_info}在第{index}个箱子后\n"
    return content
