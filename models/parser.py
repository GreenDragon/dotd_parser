import os
import itertools
import locale
locale.setlocale(locale.LC_ALL, '')

def parser(input):
	obtained_items = {}
	proc_items = {}
	found_items = {}
	general_translation = {}
	mount_translation = {}
	item_translation = {}
	experience = {"user":"", "critical": 0, "regular":0, "crit_damage": 0, "damage": 0, "health": 0, "gold":0, "exp": 0}
	glist= db().select(db.general.name,db.general.proc_name)
	mlist = db().select(db.mount.name,db.mount.proc_name)
	ilist = db().select(db.item.name,db.item.proc_name)
	for row in glist:
		general_translation[row.proc_name] = row.name
	for row in mlist:
		mount_translation[row.proc_name] = row.name
	for row in ilist:	
		item_translation[row.proc_name] = row.name
	translation = [ general_translation, mount_translation, item_translation]
	log_file = {}
	hit_list = {}
	experience_lines = []
	highest_damage_lines = []
	max_hit = ""
	listing = [ obtained_items, proc_items, found_items, experience ]
	log_file = input.split('\n')
	enumerate_hit = list(log_file)	
	best_hit = list(log_file)
#	for num, line in enumerate(enumerate_hit):
#		if "experience!" in line:
#			object = line.split()
#			amount = int(object[2].replace(',', ''))
#			hit_list[num] = amount
#	for a in sorted(hit_list.keys()):
#		experience_lines.append(a)
#		end_line = max(hit_list, key=hit_list.get)
#		element = experience_lines.index(end_line) - 1
#		beginning_line = sorted(hit_list.keys())[element] + 1
#		for i in range(beginning_line, end_line + 1):
#			highest_damage_lines.append(best_hit[i])
#		max_hit =  highest_damage_lines

	for line in log_file:
		        if "Found" in line:
        		        object = line.split('Found')[1][:-2]
                		if not object in found_items:
	                        	found_items[object] = 1
		                else:
        		                found_items[object] += 1

		        if "obtained" in line:
        		        object = line.split('obtained:')[1][:-2]
	
        		        if not object in obtained_items:
                		        obtained_items[object] = 1
		                else:
        		                obtained_items[object] += 1
	        	if "contributed" in line:
        	        	object,amount = line.split('contributed')
	                	object = object.strip()
				for translist in translation:
					if object in translist:
						object=translist[str(object)]
		                amount = int(amount.split()[0].replace(',', ''))
        		        if not object in proc_items:
					for translist in translation:
						if object in translist:
							object=translist[str(object)]
                		        proc_items[object] = { 'count' : 1, 'damage' : amount }
		                else:
        		                proc_items[object]['count'] += 1
                		        proc_items[object]['damage'] = proc_items[object]['damage'] + amount
		        if "experience!" in line:
        		        object = line.split()
                		experience["user"] = object[0]
	                	if "crit" in object[1]:
	        	                experience["critical"] += 1
        	        	        amount = int(object[2].replace(',', ''))
                	        	experience["crit_damage"] = experience["crit_damage"] + amount
	                	else:
	        	                experience["regular"] +=1
        	        	for item in 2,5,8,11:
                	        	amount = int(object[item].replace(',', ''))
	                	        if item == 2:
        	                	        experience["damage"] = experience["damage"] + amount
		                        elif item == 5:
        		                        experience["health"] = experience["health"] + amount
                		        elif item == 8:
                        		        experience["gold"] = experience["gold"] + amount
		                        else:
        		                        experience["exp"] = experience["exp"] + amount
	return experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list
