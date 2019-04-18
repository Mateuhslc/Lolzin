import glob
import json

data = './Campeoes/Data.json'
champs = './Campeoes/Campeoes.json'

picks_bans = [{
	"list": None,
	"num": -1,
	"name": "None",
	"bans": 0,
	"picks_blue": 0,
	"picks_red": 0,
	"games": 1,
	"wins": 0
}]
#{
#	"num": -1,
#	"name": "",
#	"bans": 0,
#	"picks": 0,
#	"wins": 0
#}

game_data = ''

def load_data():
	with open(champs, mode = 'r', encoding = 'utf-8') as f:
		convertido = json.loads(f.read())
		for c in convertido["data"]:
			auxbans = {
				"list": None,
				"num": None, 
				"name": None,
				"bans": 0,
				"picks_blue": 0,
				"picks_red": 0,
				"games": 1,
				"wins": 0
			}
			auxbans["list"] = (convertido["data"][c])
			auxbans["num"] = (int(convertido["data"][c]["key"]))
			auxbans["name"] = c
			picks_bans.append(auxbans)

def winsort(a):
# Swap the elements to arrange in order
	list = a
	for iter_num in range(len(list)-1,0,-1):
		for idx in range(iter_num):
			if (list[idx]["wins"]/list[idx]["games"]<list[idx+1]["wins"]/list[idx+1]["games"]):
				temp = list[idx]
				list[idx] = list[idx+1]
				list[idx+1] = temp

def bansort(list):
# Swap the elements to arrange in order
    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]["bans"]<list[idx+1]["bans"]:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp

load_data()

with open(data, mode = 'r', encoding = 'utf-8') as f:
	convertido = json.loads(f.read())
	game_data = convertido
	#Ocorrencia de bans aqui

	for k in range(len(convertido["matches"])):
		for j in range(len(convertido["matches"][k]["teams"])):
			for i in range(len(convertido["matches"][k]["teams"][j]["bans"])):
				champId = int(convertido["matches"][k]["teams"][j]["bans"][i]["championId"])
				pqp = 1
				if(champId == -1):
					picks_bans[0]["bans"] += 1
				while pqp < len(picks_bans):
					if picks_bans[pqp]["num"] == champId:
						picks_bans[pqp]["bans"] += 1
						pqp = 0
						break
					pqp += 1

	#Ocorrencia de picks aqui

	for k in range(len(convertido["matches"])):
			for i in range(len(convertido["matches"][k]["participants"])):
				champId = int(convertido["matches"][k]["participants"][i]["championId"])
				pqp = 0
				while pqp < len(picks_bans):
					if picks_bans[pqp]["num"] == champId:
						if(convertido["matches"][k]["participants"][i]["teamId"] == 100):
							picks_bans[pqp]["picks_blue"] += 1
						else:
							picks_bans[pqp]["picks_red"] += 1

						if(convertido["matches"][k]["participants"][i]["stats"]["win"]):
							picks_bans[pqp]["wins"] += 1
						picks_bans[pqp]["games"] = picks_bans[pqp]["picks_blue"] + picks_bans[pqp]["picks_red"]	
						pqp = 0
						break
					pqp += 1
winsort(picks_bans)
for p in picks_bans:
	if(p["wins"]/p["games"] >= 0.5):
		print(p["name"], ' ', p["wins"]/p["games"])
#print(game_data["matches"][0]["participants"])