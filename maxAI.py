import UnityPy
import os
import json
import sys


#PathIDs inside Unity
#DO NOT CHANGE UNLESS GAME IS UPDATED
Trainer_Table = 676024375065692598
pathList = [Trainer_Table]

src = "masterdatasEDITED"

env = UnityPy.load(src)

trainerType = "TrainerType"
trainerData = "TrainerData"
trainerPoke = "TrainerPoke"

if not os.path.exists(src):
    print("Error, masterdatas not found")
    print("Press enter to Exit...")
    input()
    sys.exit()

for obj in env.objects:
    if obj.path_id in pathList:
        tree = obj.read_typetree()

        for trainer in tree[trainerData]:
            trainer["AIBit"] = 111
            
        obj.save_typetree(tree)
                    
with open("masterdatasMAXAI", "wb") as f:
    f.write(env.file.save(packer = (64,2)))   