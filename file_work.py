import building_class, menu

def save(city):
    #finds the save file
    save_file=open("save file.txt", "w")
    for building in city.get_buildings_list():
        #writes all the buildings properties to the file
        save_file.write(building.get_type()+",")
        save_file.write(str(building.get_rect()[0])+",")
        save_file.write(str(building.get_rect()[1])+",")
        save_file.write(str(building.get_lvl())+",")
        if building.get_dmg_status()==True:
            save_file.write(str("D\n"))
        else:
            save_file.write(str("\n"))
    #writes the money and player level to the file
    save_file.write(str(city.get_money())+"\n")
    save_file.write(str(city.get_player_lvl())+"\n")
    save_file.write(str(city.player_name)+"\n")
    for i in range(0, len(city.technology)):
        if i==len(city.technology)-1:
            save_file.write(str(city.technology[i]))
        else:
            save_file.write(str(city.technology[i])+",")
    save_file.close()

def load(interface, city, buttons, load_type):
    #if the main game is being loaded
    if load_type=="main":
        #reads the save file
        try:
            save_file=open("save file.txt", "r")
            city.set_playing_type("main")
            found=True
        except FileNotFoundError:
            interface.popup("There is no save file", "try saving one first")
            found=False
    else:
        try:
            #draw a popup describing the students aim in the mission
            if city.get_player_lvl()==1:
                save_file=open("missions/mission_1.txt", "r")
                interface.popup("Your aim is to build a level 3 lab")
            elif city.get_player_lvl()==2:
                save_file=open("missions/mission_2.txt", "r")
                interface.popup("Your aim is to reach 20 quality of life")
            else:
                interface.popup("There arent any missions left!")
                city.set_playing_type("main")
                return
            city.set_playing_type("mission")
            found=True
        except FileNotFoundError:
            interface.popup("The mission file cannot be found", "try re-downloading it")
            found=False
    if found:
        save=save_file.read().splitlines()
        save_file.close()
        buildings_list=[]
        #reads money and player level, then takes them out the list
        technology=[]
        money=save[72]
        player_lvl=save[73]
        player_name=save[74]
        save[75]=save[75].split(",")
        for item in save[75]:
            if item=="True":
                technology.append(True)
            else:
                technology.append(False)
        #so only the buildings are left in the list
        del save[72]
        del save[72]
        del save[72]
        del save[72]
        #creates all the building objects
        for item in save:
            #find the position on the city to place the building
            item=item.split(",")
            X=int(item[1])
            Y=int(item[2])
            X+=30
            X/=50
            Y+=35
            Y/=50
            list_value=int((Y-1)*8+(X-1))
            if item[0]=="Empty":
                buildings_list.append(building_class.Empty(int(item[1]), int(item[2]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda buildingX=int(item[1]), buildingY=int(item[2]):menu.display_build_menu(interface, buttons, city, (buildingX, buildingY)))))
            elif item[0]=="House":
                buildings_list.append(building_class.House(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Shop":
                buildings_list.append(building_class.Shop(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="School":
                buildings_list.append(building_class.School(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Hospital":
                buildings_list.append(building_class.Hospital(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Road":
                buildings_list.append(building_class.Road(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Factory":
                buildings_list.append(building_class.Factory(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Police_station":
                buildings_list.append(building_class.Police_station(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Bank":
                buildings_list.append(building_class.Bank(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Power_station":
                buildings_list.append(building_class.Power_station(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Leisure":
                buildings_list.append(building_class.Leisure(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            elif item[0]=="Lab":
                buildings_list.append(building_class.Lab(int(item[1]), int(item[2]), int(item[3]), (lambda X2=int(item[1]), Y2=int(item[2]):interface.add_highlight(X2, Y2), lambda list_value=list_value:menu.display_indiv_building_menu(interface, buttons, city, list_value))))
            if item[4]=="D":
                buildings_list[len(buildings_list)-1].change_dmg(True)
        #load the buildings list
        city.load_buildings_list(buildings_list)
        #if a building was being built before load, then reset this as it
        #wont match the city that has just been loaded
        city.reset_buildings_to_add()
        #set the cities attributes to the ones in the save file
        city.set_money(float(money))
        city.set_lvl(int(player_lvl))
        city.player_name=player_name
        city.technology=technology
        city.reset_population()
        menu.display_game_menu(buttons)
        city.change_playing(True)

def restart(city, buttons, interface):
    #find the save file and a clean file
    save_file=open("save file.txt", "w")
    clean_file=open("clean save.txt", "r")
    #copies the clean files contents into the save file
    clean_file_lines=clean_file.read().splitlines()
    for line in clean_file_lines:
        save_file.write(line+"\n")
    save_file.close()
    clean_file.close()
    #re-enter the players name
    interface.get_name(city)

def insert_newscore(scores, newscore):
    #if there are no items left in scores return the newscore by itself
    if scores==[]:
        return newscore
    #if the newscore if more than the first item in the scores list
    if newscore[1]>scores[0][1]:
        #return the newscore added onto the front of the scores list
        return [newscore]+scores
    #recurse the function with one less item in the scores list
    return [scores[0]]+insert_newscore(scores[1:], newscore)

def save_score(city):
    #open the text file leaderboard
    file=open("leaderboard.txt", "r")
    scores=file.read().splitlines()
    for i in range(0, len(scores)):
        #spilt the scores into name and score
        scores[i]=scores[i].split(",")
        #change the score to an integer so they can be compared
        scores[i][1]=int(scores[i][1])
    file.close()
    done=False
    #check if the score has already been saved
    if city.player_name+","+str(city.get_score()) in scores:
        done=True
    if not done:
        newscore=[city.player_name, int(city.get_score())]
        #insert the new score to the list with the sort
        scores=insert_newscore(scores, newscore)
        #remove the 6th score as it will not be displayed anyway and removing
        #it will reduce the space the file and list when read in takes up
        del scores[-1]
        file=open("leaderboard.txt", "w")
        for score in scores:
            file.write(str(score[0])+","+str(score[1])+"\n")
        file.close()

def update_lvl(city):
    #open the save file
    save_file=open("save file.txt", "r")
    save=save_file.read().splitlines()
    save_file.close()
    #update the level variable
    save[73]=city.get_player_lvl()
    #write the updated version of the save to the file
    save_file=open("save file.txt", "w")
    for item in save:
        save_file.write(str(item)+"\n")
    save_file.close()
