import os
import re

def loadfile(path:str,lang="lang.l"):
    list_lang=[]
    filepath=os.path.join(path,lang)
    if not os.path.isfile(filepath):
        # with open(filepath, "w", encoding="utf-8") as gen:
        #     gen.write("# This is translation file. You can translate your words in here.\n"
        #               "# I Use custom pattern with regex so may  have some bugs.\n"
        #               "# Each line for a translation. Use \"#\" to comment.\n"
        #               "# Words combine like this: \"Original words\"-\"Translate words\"\n")
        # return "Couldn't find lang file. Will create \"lang.l\" file autoly. Input your translation in there."
        return list_lang#Could not find file
    with open(filepath,'r', encoding="utf-8") as file:
        content = file.readlines()
        print(len(content))
        for line in content:
            comment = line.find("#")
            text1 = line.find("\"")
            if comment != -1:
                line=line[:comment]
            words=re.findall(r"\"(.+?)\"-\"(.+?)\"",line,re.I)
            #print(words[0])
            if len(words)>0:
                list_lang.append(words[0])
        if len(list_lang)==0:
            return list_lang#No words
        else:
            return list_lang

