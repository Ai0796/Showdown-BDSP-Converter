import UnityPy
import os
import json
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
        return f.read().splitlines()
    
def getMoveList():
    
    filepath = "Resources//moves.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().splitlines()
    
def getPokemonList():
    filepath = "Resources//pokemon.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().splitlines()
    
def getItemList():
    filepath = "Resources//items.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().splitlines()
    
def getNatureList():
    filepath = "Resources//natures.txt"
    with open(filepath, "r", encoding = "utf8") as f:
        return f.read().splitlines()
        
def formatStat(stat, name):
    returnString = ""
    returnString += str(stat) + " " + name + " / "
    return returnString
    

abilityList = getAbilityList()
moveList = getMoveList()
itemList = getItemList()
natureList = getNatureList()
pokeList = getPokemonList()
genderList = ["", "(M) ", "(F) ", ""]
statList = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
japaneseStatList = ["Hp", "Atk", "Def", "SpAtk", "SpDef", "Agi"]

if not os.path.exists(src):
    print("Error, masterdatas not found")
    print("Press enter to Exit...")
    input()
    sys.exit()

for outputPath in fileList:
    if not os.path.exists(outputPath):
        os.makedirs(outputPath, 0o666)

for obj in env.objects:
    if obj.path_id in pathList:
        tree = obj.read_typetree()

        #Exports Pokemon
        if tree['m_Name'] == "TrainerTable":
            for trainer in tree[trainerType]:
                fp = os.path.join(trainerType, f"{trainer['TrainerID']}.json")
                with open(fp, "wt", encoding = "utf8") as f:
                    json.dump(trainer, f, ensure_ascii = False, indent = 4)
                    
            for i in range(len(tree[trainerData])):
                trainer = tree[trainerData][i]
                fp = os.path.join(trainerData, f"{i}.json")
                with open(fp, "wt", encoding = "utf8") as f:
                    json.dump(trainer, f, ensure_ascii = False, indent = 4)
                    
            for trainer in tree[trainerPoke]:
                evList = []
                ivList = []
                pokeString = ""
                for pokeNum in range(1, 7):
                    # print(dic["P"f"{pokeNum}Level"])
                    level = trainer["P"f"{pokeNum}Level"]
                    if level > 0:
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
                        monsno = pokeList[trainer["P"f"{pokeNum}MonsNo"]]
                        gender = genderList[trainer["P"f"{pokeNum}Sex"]]
                        item = ""
                        if trainer["P"f"{pokeNum}Item"] > 0:
                            item = "@ " + itemList[trainer["P"f"{pokeNum}Item"]]
                        
                        ability = abilityList[trainer["P"f"{pokeNum}Tokusei"]]
                        level = str(level)
                        
                        shiny = trainer["P"f"{pokeNum}IsRare"]
                        
                        evList = []
                        ivList = []
                        for i in range(len(japaneseStatList)):
                            ##IVs aren't shown if they're 31
                            if trainer["P"f"{pokeNum}Talent"f"{japaneseStatList[i]}"] < 31:
                                ivList.append(formatStat(trainer["P"f"{pokeNum}Talent"f"{japaneseStatList[i]}"], statList[i]))
                            ##EVs aren't shown if they're 0
                            if trainer["P"f"{pokeNum}Effort"f"{japaneseStatList[i]}"] > 0:
                                evList.append(formatStat(trainer["P"f"{pokeNum}Effort"f"{japaneseStatList[i]}"], statList[i]))
                        
                        nature = natureList[trainer["P"f"{pokeNum}Seikaku"]]
                        
                        trainerMoveList = []
                        for i in range(1, 5):
                            if trainer["P"f"{pokeNum}Waza"f"{i}"] > 0:
                                trainerMoveList.append(moveList[trainer["P"f"{pokeNum}Waza"f"{i}"]])
                        
                        pokeString += monsno + " "
                        pokeString += gender
                        pokeString += item + "\n" #\n is newline
                        
                        pokeString += "Ability: " + ability + "\n"
                        
                        pokeString += "Level: " + level + "\n"
                        
                        if shiny == 1:
                            pokeString += "Shiny: Yes\n" 
                        
                        if len(evList) > 0:
                            pokeString += "EVs: "
                            for ev in evList:
                                pokeString += ev
                            pokeString = pokeString[:-2] #Removes the extra backslash
                            pokeString += "\n"
                        
                        pokeString += nature + " Nature\n"
                        
                        if len(ivList) > 0:
                            pokeString += "IVs: "
                            for iv in ivList:
                                pokeString += iv
                            pokeString = pokeString[:-2] #Removes the extra backslash
                            pokeString += "\n"
                        
                        for move in trainerMoveList:
                            pokeString += "- " + move + "\n"
                            
                        pokeString += "\n"
                
                pokeString = pokeString[:-1] ##Removes the extra newline
                fp = os.path.join(trainerPoke, f"{trainer['ID']}.txt")
                with open(fp, "wt", encoding = "utf8") as f:
                    f.write(pokeString)        
                    
                    
print("Finished Extracting masterdatas")
print("Press enter to Exit...")
input()