import building_class, file_work, menu
import random, math

class City:
    """Simulate a city to contain the buildings"""

    #give the city the basic variables and make them private
    def __init__(self):
        #the list of buildings in the city
        self._buildings_list=[]
        #the distionary of buildings that will be added
        #and the time until they are built
        self._buildings_to_add={}
        #the list of technologies, and which are owned
        #0 is the skyscraper technology
        #1 is deficiency technology
        #2 is engineers technology
        #3 is smart buildings technology
        self.technology=[0, 0, 0, 0]
        #the money the player has
        self._money=10000
        #the population of the city
        self._population=0
        #the players level
        self._player_lvl=1
        #whether the game is being played
        self._playing=False
        #what type of game is being played
        self._playing_type=None
        #the players name
        self.player_name="Player"

    #getters
    def get_money(self):
        return self._money

    def get_player_lvl(self):
        return self._player_lvl

    def get_buildings_list(self):
        return self._buildings_list

    def get_playing(self):
        return self._playing

    def get_playing_type(self):
        return self._playing_type

    #to find out what the highest level of school is
    def get_school_lvl(self):
        lvl=0
        #for every building in the list
        for building in self.get_buildings_list():
            #if the building is a school
            if isinstance(building, building_class.School):
                #if building is not damaged
                if building.get_dmg_status()==False:
                    if building.get_lvl()>lvl:
                        lvl=building.get_lvl()
        return lvl

    def get_population(self):
        return self._population

    def reset_population(self):
        self._population=0

    def increase_population(self):
        #if the max population is above the current, increase
        if self.get_max_people()>self.get_population():
            self.change_population(1)
        #if max population is below current, decrease
        elif self.get_max_people()<self.get_population():
            self.change_population(-1)

    #calculates the total people from the number of housess
    def get_max_people(self):
        people=0
        for building in self.get_buildings_list():
            #calculates how many houses there are in total
            if isinstance(building, building_class.House):
                #if building is not damaged
                if building.get_dmg_status()==False:
                    lvl=building_class.House.get_lvl(building)
                    #if skyscrapers have been bought
                    if lvl==3 and self.technology[0]==True:
                        people+=5
                    #finds the lvl of the house and adds it onto people
                    people+=5*lvl
        return people

    #return the maximum number of roads placed in a row in the city
    def roads_in_row(self):
        max_in_row=0
        rows_down=0
        columns_across=0
        #for every building in the city
        for i in range(0, len(self.get_buildings_list())):
            #the column i is on
            columns_across+=1
            if i%8==0:
                #the row i is on
                rows_down+=1
                columns_across=1
            #if its a road
            if isinstance(self.get_buildings_list()[i], building_class.Road):
                if self.get_buildings_list()[i].get_dmg_status()==False:
                    #there is 1 in a row
                    if 1>max_in_row:
                        max_in_row=1
                    #repeat for as many in a row there can be horizontal
                    for j in range(2, 10-columns_across):
                        #if theres another road to the right of it
                        if isinstance(self.get_buildings_list()[i+j-1], building_class.Road):
                            #there are j in a row
                            if j>max_in_row:
                                max_in_row=j
                        else:
                            break
                    #repeat for as many in a row there can be vertical
                    for k in range(2, 11-rows_down):
                        #if theres another road below it
                        if isinstance(self.get_buildings_list()[i+8*(k-1)], building_class.Road):
                            #there are k in a row
                            if k>max_in_row:
                                max_in_row=k
                        else:
                            break
        return max_in_row

    #calculates how much money is to be gained per tick
    #calculates the people needed to be at full production
    #calculates the % chance of a crime occurring
    #calculates the % chance of new births
    def get_gains(self):
        gain=0
        people_needed=0
        crime_chance=0
        birth_chance=0
        working_people=self.get_population()
        houses=0
        house_lvls=0
        road_lvls=0
        shop_lvls=0
        hospital_lvls=0
        hospital_maxlvl=0
        factory_lvls=0
        police_stations=0
        police_station_lvls=0
        bank_lvls=0
        power_stations=0
        power_station_lvls=0
        entertainments=0
        entertainment_lvls=0
        labs=0
        church_maxlvl=0
        #for every building in the list
        for building in self.get_buildings_list():
            #if the building is not damaged
            if building.get_dmg_status()==False:
                #calculates how many of each building there is
                if isinstance(building, building_class.House):
                    houses+=1
                    house_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Road):
                    road_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Shop):
                    shop_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Hospital):
                    hospital_lvls+=building.get_lvl()
                    if building.get_lvl()>hospital_maxlvl:
                        hospital_maxlvl=building.get_lvl()
                elif isinstance(building, building_class.Factory):
                    factory_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Police_station):
                    police_stations+=1
                    police_station_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Bank):
                    bank_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Power_station):
                    power_stations+=1
                    power_station_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Leisure):
                    entertainments+=1
                    entertainment_lvls+=building.get_lvl()
                elif isinstance(building, building_class.Lab):
                    labs+=1
                elif isinstance(building, building_class.Church):
                    if building.get_lvl()>church_maxlvl:
                        church_maxlvl=building.get_lvl()
        #the money made from shops
        for i in range(0, shop_lvls):
            for j in range(0, 10):
                people_needed+=1
                if working_people>0:
                    working_people+=-1
                    gain+=15
        #the money made from factories
        for i in range(0, factory_lvls):
            for j in range(0, 20):
                people_needed+=1
                if working_people>0:
                    working_people+=-1
                    #power stations increase money made by factories
                    gain+=8*(1.1+0.1*power_station_lvls)
        #the cost each person takes
        gain+=self.get_population()*(-4+hospital_maxlvl)
        #the cost of each level of hospital
        gain+=hospital_lvls*(-8)
        #the cost of police stations
        gain+=police_stations*(-5)
        #power station gains
        gain+=power_stations*10
        #entertainment buildings cost to keep running
        gain+=entertainments*(-10)
        #lab gains
        gain+=labs*50
        #church gains
        gain+=(church_maxlvl**2)*houses*0.05
        #to display a message if more people are needed to get full profit
        people_needed-=self.get_population()
        #banks increase total money made
        gain*=(1.05+0.05*bank_lvls)
        #the crime chance
        crime_chance=0.0035*houses-0.0005*road_lvls-0.006*police_station_lvls
        if self.roads_in_row()>2:
            crime_chance-=0.0025*(self.roads_in_row()-2)
        birth_chance=0.002*math.ceil(self.get_population()/3)*math.ceil(hospital_lvls*2.5+0.1)+0.2
        QOL=-houses*2+house_lvls+(max(0, shop_lvls-5)*3)-factory_lvls+entertainment_lvls*5+hospital_lvls
        return gain, people_needed, crime_chance, birth_chance, QOL

    def check_mission_end(self):
        mission1=False
        mission2=False
        for building in self.get_buildings_list():
            if isinstance(building, building_class.Lab) and building.get_lvl()==3:
                mission1=True
        #if quality is life is 20 or above
        if self.get_gains()[4]>=20:
            mission2=True
        if self.get_player_lvl()==1:
            return mission1
        elif self.get_player_lvl()==2:
            return mission2

    #calculates the players score from the total people and money
    def get_score(self):
        #works out the score from the total people and money
        score=self._money+(self.get_population()*500)
        return round(score)

    #this will run when a crime occurs
    def crime(self, interface):
        #picks a random crime type
        ctype=random.randint(1, 3)
        if ctype==1:
            #the amount of money lost
            camo=random.randint(100, 3000)
            self.change_money(-camo)
            #creates a popup
            interface.popup("A crime has occurred!", "You have lost %s money" % camo)
        elif ctype==2:
            if self.get_population()>3:
                #picks a random number 1-3 with a bias
                camolist=[1, 1, 1, 2, 2, 3]
                camo=random.choice(camolist)
                #reduces the population by that number
                self.change_population(-camo)
                #creates a popup
                if camo==1:
                    text="person has"
                else:
                    text="people have"
                interface.popup("A crime has occurred!", "%s %s been killed" % (camo, text))
        elif ctype==3:
            #finds a random building
            random_building=random.choice(self.get_buildings_list())
            while isinstance(random_building, building_class.Empty) or isinstance(random_building, building_class.Building_slot) or random_building.get_dmg_status():
                random_building=random.choice(self.get_buildings_list())
            #damages the building
            random_building.change_dmg(True)
            #creates a popup
            interface.popup("A crime has occurred!", "One of your %ss has been damaged" % random_building.get_type().lower())

    def get_city_type(self):
        possible_types=["Global giant", "Knowledge capital",\
                        "Factory based", "Market town",\
                        "Urban city", "Favela"]
        shop=False
        max_church_lvl=0
        lab=False
        factory_lvls=0
        for building in self.get_buildings_list():
            if isinstance(building, building_class.Shop):
                    shop=True
            if isinstance(building, building_class.Church):
                if building.get_lvl()>max_church_lvl:
                    max_church_lvl=building.get_lvl()
            if isinstance(building, building_class.Lab):
                lab=True
            if isinstance(building, building_class.Factory):
                factory_lvls+=building.get_lvl()
        #defines the requirements for each city type
        #if the reuirements are not met, remove the city type from the list
        if (not self.technology[0]) or self.get_gains()[0]<500 or self.get_population()<150 or max_church_lvl<3:
            possible_types.remove("Global giant")
        if not lab or not (self.technology[3] or self.technology[1]) or self.get_population()<70 or self.get_gains()[4]<5:
            possible_types.remove("Knowledge capital")
        if self.get_gains()[0]<500 or self.get_money()<30000 or factory_lvls<7:
            possible_types.remove("Factory based")
        if self.get_gains()[2]>0.02 or self.get_population()>100 or not shop or self.get_gains()[4]<10:
            possible_types.remove("Market town")
        if self.get_gains()[0]<100 or self.get_school_lvl()<1 or max_church_lvl<1:
            possible_types.remove("Urban city")
        #return the first city type left in the list
        return possible_types[0]

    #setters
    def set_money(self, amount):
        self._money=amount
    
    def change_money(self, amount):
        self._money+=amount

    def change_population(self, amount):
        self._population+=amount

    def change_playing(self, playing):
        self._playing=playing

    def set_playing_type(self, ptype):
        self._playing_type=ptype

    def set_lvl(self, lvl):
        self._player_lvl=lvl

    def load_buildings_list(self, new):
        self._buildings_list=new

    def reset_buildings_to_add(self):
        self._buildings_to_add={}

    def buy_technology(self, technology, interface):
        #check the type of technology to be bought
        #then check if the player has enough money
        #if they do then remove that much money and buy the technology
        if technology=="skyscrapers":
            if self.get_money()>25000:
                self.change_money(-25000)
                self.technology[0]=1
            else:
                interface.popup("This costs %s" % 25000, "you only have %s" % round(self.get_money()))
        if technology=="deficiency":
            if self.get_money()>10000:
                self.change_money(-10000)
                self.technology[1]=1
            else:
                interface.popup("This costs %s" % 10000, "you only have %s" % round(self.get_money()))
        if technology=="engineers":
            if self.get_money()>15000:
                self.change_money(-15000)
                self.technology[2]=1
            else:
                interface.popup("This costs %s" % 15000, "you only have %s" % round(self.get_money()))
        if technology=="smart_buildings":
            if self.get_money()>30000:
                self.change_money(-30000)
                self.technology[3]=1
            else:
                interface.popup("This costs %s" % 30000, "you only have %s" % round(self.get_money()))

    #building based methods
    def reduce_building_time(self, buttons, interface):
        #for each key in the dictionary
        for item in self._buildings_to_add.keys():
            self._buildings_to_add[item]-=1
            if self._buildings_to_add[item]<=0:
                new_building=item
                self.add_building(new_building[0], new_building[1], new_building[2], new_building[3], buttons, interface)
        #if there were no buildings with 0 or under ticks left delete won't be
        #assigned so delete won't work
        #the limitation of this is if multiple buildings are added to the list
        #in one tick only one will be deleted, but its not possible to do that
        #as then 2 buttons and 3 screen changes would need to occur in the same
        #tick, so its fine to assume there will only be one with 0 each loop
        try:
            del self._buildings_to_add[new_building]
        except UnboundLocalError:
            pass

    def add_empty(self, buttons, interface):
        self._buildings_list=[]
        #create building lists starting objects
        buildingX=20
        buildingY=15
        for i in range(1, 73):
            self._buildings_list.append(building_class.Empty(buildingX, buildingY, (lambda buildingX=buildingX, buildingY=buildingY:interface.add_highlight(buildingX, buildingY), lambda buildingX=buildingX, buildingY=buildingY:menu.display_build_menu(interface, buttons, self, (buildingX, buildingY)))))
            buildingX+=50
            if i%8==0:
                #when the loop has been done 8 times,
                #it will add them 50 down, but start back at 20 X position
                buildingX=20
                buildingY+=50

    #adds a new building of any type
    def add_building(self, building, Xpos, Ypos, lvl, buttons, *interface):
        #find which position the building should be in the list
        X2=Xpos
        Y2=Ypos
        Xpos+=30
        Xpos/=50
        Ypos+=35
        Ypos/=50
        list_value=(Ypos-1)*8+(Xpos-1)
        del self._buildings_list[int(list_value)]
        #works out what position in the list the co-ordinates are
        if building=="Empty":
            #interface is refrenced as interface[0]
            #as interface is stored as a 1 item list because of *args
            self._buildings_list.insert(int(list_value), (building_class.Empty(X2, Y2, ((lambda:interface[0].add_highlight(X2, Y2), lambda X2=X2, Y2=Y2:menu.display_build_menu(interface[0], buttons, self, (X2, Y2)))))))
        if building=="Building_slot":
            self._buildings_list.insert(int(list_value), (building_class.Building_slot(X2, Y2, (print))))
        if building=="House":
            self._buildings_list.insert(int(list_value), (building_class.House(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Shop":
            self._buildings_list.insert(int(list_value), (building_class.Shop(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="School":
            self._buildings_list.insert(int(list_value), (building_class.School(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Hospital":
            self._buildings_list.insert(int(list_value), (building_class.Hospital(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Road":
            self._buildings_list.insert(int(list_value), (building_class.Road(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Factory":
            self._buildings_list.insert(int(list_value), (building_class.Factory(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Police station":
            self._buildings_list.insert(int(list_value), (building_class.Police_station(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Bank":
            self._buildings_list.insert(int(list_value), (building_class.Bank(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Power station":
            self._buildings_list.insert(int(list_value), (building_class.Power_station(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Leisure":
            self._buildings_list.insert(int(list_value), (building_class.Leisure(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Lab":
            self._buildings_list.insert(int(list_value), (building_class.Lab(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))
        if building=="Church":
            self._buildings_list.insert(int(list_value), (building_class.Church(X2, Y2, lvl, (lambda:interface[0].add_highlight(X2, Y2), lambda:menu.display_indiv_building_menu(interface[0], buttons, self, int(list_value))))))

    def start_building(self, building, Xpos, Ypos, lvl, time, cost, buttons, interface):
        interface.remove_highlight()
        #if the player can afford the building
        if self.get_money()>=(cost-0.5):
            self.change_money(-cost)
            #add the building in the future, which the time taken as the value
            self._buildings_to_add[(building, Xpos, Ypos, lvl)]=time
            #add a building slot to the screen until that point
            self.add_building("Building_slot", Xpos, Ypos, 0, buttons)
        else:
            #if the player can't afford the building make a popup to say this
            interface.popup("This costs %s" % cost, "you only have %s" % round(self.get_money()))

    #draws all the buildings on the list onto the screen
    def draw_buildings(self, screen):
        for building in self.get_buildings_list():
            building.draw(screen)
