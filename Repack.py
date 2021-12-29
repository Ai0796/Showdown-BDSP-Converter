import UnityPy
import os
import json
import traceback
import sys


#PathIDs inside Unity
#DO NOT CHANGE UNLESS GAME IS UPDATED
Trainer_Table = 676024375065692598
pathList = [Trainer_Table]

src = "masterdatas"

env = UnityPy.load(src)

trainerType = "TrainerType"
trainerData = "TrainerData"
trainerPoke = "TrainerPoke"

fileList = [trainerType, trainerData, trainerPoke]

def getAbilityList():
    
    filepath = "Resources//abilities.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().upper().splitlines()
    
def getMoveList():
    
    filepath = "Resources//moves.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().upper().splitlines()
    
def getPokemonList():
    filepath = "Resources//pokemon.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().upper().splitlines()
    
def getItemList():
    filepath = "Resources//items.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().upper().splitlines()
    
def getNatureList():
    filepath = "Resources//natures.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().upper().splitlines()
        
def formatStat(stat):
    dic = {}
    for i in stat:
        parse = i.strip().split(" ")
        if parse == ['']:
            return 
        key = japaneseStatList[statList.index(parse[1])]
        num = int(parse[0])
        dic[key] = num
    return dic

def name(name):
    return pokeList.index(name)

def ability(line2):
    ability = line2[9:].strip()
    return abilityList.index(ability)

def level(line3):
    return line3[7:]


abilityList = getAbilityList()
moveList = getMoveList()
itemList = getItemList()
natureList = getNatureList()
pokeList = getPokemonList()
    
genderList = ["", "(M)", "(F)", ""]
statList = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]
japaneseStatList = ["Hp", "Atk", "Def", "SpAtk", "SpDef", "Agi"]

for outputPath in fileList:
    if not os.path.exists(outputPath):
        print("Error, "f"{outputPath} Does not exist")
        
        print("Press enter to Exit...")
        input()
        sys.exit()

for obj in env.objects:
    if obj.path_id in pathList:
        tree = obj.read_typetree()

        #Exports Pokemon
        if tree['m_Name'] == "TrainerTable":
            for trainer in tree[trainerType]:
                fp = os.path.join(trainerType, f"{trainer['TrainerID']}.json")
                with open(fp, "r", encoding = "utf8") as f:
                    try:
                        trainer = json.loads(f.read())
                    except:
                        pass
                    
            for i in range(len(tree[trainerData])):
                trainer = tree[trainerData][i]
                fp = os.path.join(trainerData, f"{i}.json")
                with open(fp, "r", encoding = "utf8") as f:
                    try:
                        trainer = json.loads(f.read())
                    except:
                        pass
                    
            for trainer in tree[trainerPoke][1:]:
                fp = os.path.join(trainerPoke, f"{trainer['ID']}.txt")
                if os.path.isfile(fp):
                    try:
                        with open(fp, "r", encoding = "utf8") as f:
                            teamStr = f.read()
                            team = teamStr.rstrip(" \n").split("\n")
                        # print(team)
                        breakpoints = [0]
                        for i in range(len(team)):
                            team[i] = team[i].rstrip()
                            if team[i] == "":
                                # print("added point " + str(i))
                                breakpoints.append(i + 1)
                            team[i] = team[i].strip()
                        if len(breakpoints) > 0:
                            breakpoints.append(len(team))
                                
                        # print(breakpoints)
                        pokeNum = 0
                        for point in range(len(breakpoints) - 1):
                            
                            pokeNum += 1
                            hasIV = False
                            
                            ##Name and Ability are always present so we don't need to perform checks
                            firstLine = team[breakpoints[point]]
                            secondLine = team[breakpoints[point] + 1]
                            try:
                                trainer["P"f"{pokeNum}MonsNo"] = name(firstLine.split(" ")[0].upper())
                            except:
                                ##Pokemon Like Mr. Mime exist with a space in between AND IT RUINS EVERYTHING AAAAAAAAAAAAAAA
                                
                                trainer["P"f"{pokeNum}MonsNo"] = name(firstLine.split(" ")[0].upper() + " " + firstLine.split(" ")[1].upper())
                            ##Gender
                            if "(" in firstLine:
                                index = firstLine.index("(")
                                trainer["P"f"{pokeNum}Sex"] = genderList.index(firstLine[index:index + 3].upper())
                            ##Item
                            if "@" in firstLine:
                                index = firstLine.index("@")
                                trainer["P"f"{pokeNum}Item"] = itemList.index(firstLine[index + 1:].strip().upper())
                            
                            if "Level:" not in team[breakpoints[point]: breakpoints[point + 1]]:
                                trainer["P"f"{pokeNum}Level"] = 100 ##Level is 100 if not shown
                                
                            ##Sets all IVs to 31 by default
                            for key in japaneseStatList:
                                trainer["P"f"{pokeNum}Talent{key}"] = 31
                                
                            ##Sets all values to 0 by default
                            for key in japaneseStatList:
                                trainer["P"f"{pokeNum}Effort{key}"] = 0
                            
                            moveNum = 0
                            for line in range(breakpoints[point] + 1, breakpoints[point + 1]):
                                # Pokemon Showdown Format
                                # PokemonName (Gender) @ HeldItem
                                # Ability: AbilityName
                                # Level: Level
                                # Shiny: Y/N
                                # EVs: x Hp / x Atk / etc.
                                # NatureName Nature
                                # IVs: x Hp / x Atk / etc.
                                # - Move1
                                # - Move2
                                # - Move3
                                # - Move4
                                ##Move
                                pokemon = team[line].upper()
                                # print(pokemon)
                                if "-" in team[line]:
                                    moveNum += 1
                                    trainer["P"f"{pokeNum}Waza"f"{moveNum}"] = moveList.index(pokemon.strip(" -"))
                                    
                                elif "ABILITY" in pokemon:
                                    trainer["P"f"{pokeNum}Tokusei"] = ability(pokemon.upper())
                                    
                                elif "NATURE" in pokemon:
                                    trainer["P"f"{pokeNum}Seikaku"] = natureList.index(pokemon.split(" ")[0])
                                    
                                elif "SHINY" in pokemon:
                                    ##Shiny should only be present if it is, so not gonna bother checking Shiny: N
                                    trainer["P"f"{pokeNum}IsRare"] = 1
                                    
                                elif "LEVEL" in pokemon:
                                    trainer["P"f"{pokeNum}Level"] = int(pokemon.split(" ")[1])
                                    
                                elif "EVS" in pokemon:
                                    EVdic = formatStat(pokemon[4:].split("/"))
                                    for key in EVdic.keys():
                                        trainer["P"f"{pokeNum}Effort{key}"] = EVdic[key]
                                        
                                elif "IVS"  in pokemon:
                                    IVdic = formatStat(pokemon[4:].split("/"))
                                    ##Sets all values to 31 by default before setting to showdown
                                    for key in IVdic.keys():
                                        trainer["P"f"{pokeNum}Talent{key}"] = IVdic[key]
                                        
                            for moveReplace in range(moveNum + 1, 5):
                                trainer["P"f"{pokeNum}Waza"f"{moveReplace}"] = 0            
                                        
                        for pokeReplace in range(pokeNum + 1, 7):
                            trainer["P"f"{pokeReplace}MonsNo"] = 0
                            trainer["P"f"{pokeReplace}Level"] = 0
                            
                       
                                        
                    except:
                        print("An Error has occured while packing "f"{fp}")
                        print(traceback.format_exc())
                        print(trainer['ID'])
                        print(team)
                        print(teamStr)
                        print(breakpoints)
                        print(secondLine)
                                        
                else:
                    print("Error "f"{fp} not found")                     
                                    
                                    
            
            obj.save_typetree(tree)            
                            
                        
with open("masterdatasEDITED", "wb") as f:
    f.write(env.file.save(packer = (64,2)))      
    
print("Finished Repacking masterdatas into masterdatasEDITED")
print("Press enter to Exit...")
input()