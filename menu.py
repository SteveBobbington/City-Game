import pygame
import building_class

#to make all buttons inactive
def inactivate_buttons(buttons):
    for i in range(0, len(buttons)):
        buttons[i].make_active(False)

#to define the box to be drawn to the screen when needed
def add_box(rect, image):
    rect=pygame.Rect(rect)
    image=pygame.transform.scale(pygame.image.load(image), (rect[2], rect[3]))
    return image, rect

#to define a new text image
def add_text(rect, text, colour, *font_size):
    text_surface=pygame.font.SysFont("Rockwell", 72).render(text, True, pygame.Color(colour))
    text_rect=pygame.Rect(rect)
    text_surface=pygame.transform.scale(text_surface, (rect[2], rect[3]))
    try:
        text_surface=pygame.font.SysFont("Rockwell", font_size[0]).render(text, True, pygame.Color(colour))
        text_rect=text_surface.get_rect(center=text_rect.center)
    #if the font size wasn't given
    except IndexError:
        pass
    return text_surface, text_rect

def display_game_menu(buttons):
    #make all buttons inactive
    inactivate_buttons(buttons)
    #buttons[0] is the menu button etc
    buttons[0].make_active(True)
    buttons[1].make_active(True)
    buttons[27].make_active(True)
    buttons[38].make_active(True)
    buttons[39].make_active(True)

def display_main_menu(buttons, city):
    #make all buttons inactive
    inactivate_buttons(buttons)
    #these are other buttons in the list
    if city.get_playing_type()==None:
        buttons[2].make_active(True)
        buttons[36].make_active(True)
    else:
        buttons[37].make_active(True)
    buttons[3].make_active(True)
    buttons[4].make_active(True)
    buttons[5].make_active(True)
    buttons[19].make_active(True)
    buttons[35].make_active(True)

def display_build_menu(interface, buttons, city, empty_rect):
    #make all buttons inactive
    inactivate_buttons(buttons)
    #the back button
    buttons[7].make_active(True)
    #if the building speed is faster
    speed_multiplier=1
    if city.technology[2]:
        speed_multiplier*=0.5
    #the buttons for each building
    buttons[8].make_active(True)
    buttons[8].change_function((lambda:city.start_building("House", empty_rect[0], empty_rect[1], 1+city.technology[3], 5*speed_multiplier, building_class.House.cost, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[9].make_active(True)
    buttons[9].change_function((lambda:city.start_building("Shop", empty_rect[0], empty_rect[1], 1+city.technology[3], 8*speed_multiplier, building_class.Shop.cost, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[10].make_active(True)
    buttons[10].change_function((lambda:city.start_building("School", empty_rect[0], empty_rect[1], 1+city.technology[3], 15*speed_multiplier, building_class.School.cost, buttons, interface), lambda:display_game_menu(buttons)))
    #if there is a school
    if city.get_school_lvl()>0:
        buttons[11].make_active(True)
        buttons[11].change_function((lambda:city.start_building("Hospital", empty_rect[0], empty_rect[1], 1+city.technology[3], 20*speed_multiplier, building_class.Hospital.cost, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[12].make_active(True)
    buttons[12].change_function((lambda:city.start_building("Road", empty_rect[0], empty_rect[1], 1+city.technology[3], 2*speed_multiplier, building_class.Road.cost, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[13].make_active(True)
    buttons[13].change_function((lambda:city.start_building("Factory", empty_rect[0], empty_rect[1], 1+city.technology[3], 10*speed_multiplier, building_class.Factory.cost, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[14].make_active(True)
    buttons[14].change_function((lambda:city.start_building("Police station", empty_rect[0], empty_rect[1], 1+city.technology[3], 8*speed_multiplier, building_class.Police_station.cost, buttons, interface), lambda:display_game_menu(buttons)))
    #if there is a school at level 2 or more
    if city.get_school_lvl()>1:
        buttons[15].make_active(True)
        buttons[15].change_function((lambda:city.start_building("Bank", empty_rect[0], empty_rect[1], 1+city.technology[3], 12*speed_multiplier, building_class.Bank.cost, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[16].make_active(True)
    buttons[16].change_function((lambda:city.start_building("Power station", empty_rect[0], empty_rect[1], 1+city.technology[3], 15*speed_multiplier, building_class.Power_station.cost, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[17].make_active(True)
    buttons[17].change_function((lambda:city.start_building("Leisure", empty_rect[0], empty_rect[1], 1+city.technology[3], 8*speed_multiplier, building_class.Leisure.cost, buttons, interface), lambda:display_game_menu(buttons)))
    #if there is a level 3 school
    if city.get_school_lvl()==3:
        buttons[18].make_active(True)
        buttons[18].change_function((lambda:city.start_building("Lab", empty_rect[0], empty_rect[1], 1, 25*speed_multiplier, building_class.Lab.cost, buttons, interface), lambda:display_game_menu(buttons)))
    #if there are more than 50 people
    if city.get_population()>50:
        buttons[32].make_active(True)
        buttons[32].change_function((lambda:city.start_building("Church", empty_rect[0], empty_rect[1], 1, 12*speed_multiplier, building_class.Church.cost, buttons, interface), lambda:display_game_menu(buttons)))

def display_indiv_building_menu(interface, buttons, city, list_value):
    selected_building=city.get_buildings_list()[list_value]
    #make all buttons inactive
    inactivate_buttons(buttons)
    #the back button
    buttons[7].make_active(True)
    #the upgrade button
    if selected_building.get_lvl()==1 or selected_building.get_lvl()==2:
        #if a church has been selected
        if isinstance(selected_building, building_class.Church):
            #if there is more than 75 people for each level of the church selected
            if city.get_population()>75*selected_building.get_lvl():
                buttons[20].make_active(True)
                buttons[20].change_function((lambda:selected_building.upgrade(city, interface), lambda:display_game_menu(buttons)))
        else:
            buttons[20].make_active(True)
            buttons[20].change_function((lambda:selected_building.upgrade(city, interface), lambda:display_game_menu(buttons)))
    buttons[21].make_active(True)
    buttons[21].change_function((lambda:selected_building.destroy(city, buttons, interface), lambda:display_game_menu(buttons)))
    buttons[22].make_active(True)
    buttons[23].make_active(True)
    buttons[23].change_text("Type: "+selected_building.get_type(), 16)
    buttons[24].make_active(True)
    buttons[24].change_text("Level: "+str(selected_building.get_lvl()), 16)
    buttons[25].make_active(True)
    buttons[25].change_text("Upgrade cost: "+str(selected_building.get_upgrade_cost()), 16)
    buttons[26].make_active(True)
    buttons[26].change_text("Refund: "+str(selected_building.get_refund()), 16)
    if selected_building.get_dmg_status()==True:
        buttons[33].make_active(True)
        buttons[33].change_function((lambda:selected_building.change_dmg(False), lambda:city.change_money(-1.5*selected_building.get_refund()), lambda:display_game_menu(buttons)))
        buttons[34].make_active(True)
        buttons[34].change_text("Repair cost: "+str(round(1.5*selected_building.get_refund())), 16)

def display_technology_menu(buttons, city):
    inactivate_buttons(buttons)
    buttons[7].make_active(True)
    #if the factors needed to unlock the technology are true, show the button
    if not city.technology[0] and city.get_school_lvl()==3:
        buttons[28].make_active(True)
    if not city.technology[1] and city.get_gains()[0]*10>300:
        buttons[29].make_active(True)
    if not city.technology[2] and city.get_school_lvl()>1 and city.get_population()>40:
        buttons[30].make_active(True)
    if not city.technology[3] and city.get_school_lvl()==3 and city.technology[2]:
        buttons[31].make_active(True)

#the screen displayed at the end of the game
def create_end_screen(buttons, Qbuttons, city_type):
        inactivate_buttons(buttons)
        Qbuttons[168].make_active(True)
        #depending on the city type show the correct set of end questions
        if city_type=="Global giant":
            globalQ1(Qbuttons)
        elif city_type=="Knowledge capital":
            knowledgeQ1(Qbuttons)
        elif city_type=="Factory based":
            factoryQ1(Qbuttons)
        elif city_type=="Market town":
            marketQ1(Qbuttons)
        elif city_type=="Urban":
            urbanQ1(Qbuttons)
        elif city_type=="Favela":
            favelaQ1(Qbuttons)

#these are the menus for the end game questions
def globalQ1(Qbuttons):
    #make the question 1 buttons inactive
    for i in range(1, 8):
        Qbuttons[i].make_active(True)

def globalQ2(Qbuttons):
    #make the question 1 buttons inactive
    for i in range(1, 8):
        Qbuttons[i].make_active(False)
    #make the question 2 buttons active
    for i in range(8, 13):
        Qbuttons[i].make_active(True)

def globalQ3(Qbuttons):
    #make the question 2 buttons inactive
    for i in range(8, 13):
        Qbuttons[i].make_active(False)
    #make the question 3 buttons active
    for i in range(13, 19):
        Qbuttons[i].make_active(True)

def globalQ4(Qbuttons):
    #make the question 3 buttons inactive
    for i in range(13, 19):
        Qbuttons[i].make_active(False)
    #make the question 4 buttons active
    for i in range(19, 26):
        Qbuttons[i].make_active(True)

def globalQ5(Qbuttons):
    #make the question 4 buttons inactive
    for i in range(19, 26):
        Qbuttons[i].make_active(False)
    #make the question 5 buttons active
    for i in range(26, 32):
        Qbuttons[i].make_active(True)

def globalEnd(Qbuttons, answers):
    #make the question 5 buttons inactive
    for i in range(26, 32):
        Qbuttons[i].make_active(False)
    #make quit button active
    Qbuttons[0].make_active(True)
    #check number of correct answers
    number_correct, total=answers.check_correctA("Global giant")
    Qbuttons[167].change_text("You got %s out of %s!" % (number_correct, total), 18)
    Qbuttons[166].make_active(True)
    Qbuttons[167].make_active(True)

def knowledgeQ1(Qbuttons):
    #make the question 1 buttons active
    for i in range(32, 39):
        Qbuttons[i].make_active(True)

def knowledgeQ2(Qbuttons):
    #make the question 1 buttons inactive
    for i in range(32, 39):
        Qbuttons[i].make_active(False)
    #make the question 2 buttons active
    for i in range(39, 45):
        Qbuttons[i].make_active(True)

def knowledgeQ3(Qbuttons):
    #make the question 2 buttons inactive
    for i in range(39, 45):
        Qbuttons[i].make_active(False)
    #make the question 3 buttons active
    for i in range(45, 52):
        Qbuttons[i].make_active(True)

def knowledgeQ4(Qbuttons):
    #make the question 3 buttons inactive
    for i in range(45, 52):
        Qbuttons[i].make_active(False)
    #make the question 4 buttons active
    for i in range(52, 63):
        Qbuttons[i].make_active(True)

def knowledgeEnd(Qbuttons, answers):
    #make the question 4 buttons inactive
    for i in range(52, 63):
        Qbuttons[i].make_active(False)
    #make quit button active
    Qbuttons[0].make_active(True)
    #check number of correct answers
    number_correct, total=answers.check_correctA("Knowledge capital")
    Qbuttons[167].change_text("You got %s out of %s!" % (number_correct, total), 18)
    Qbuttons[166].make_active(True)
    Qbuttons[167].make_active(True)

def factoryQ1(Qbuttons):
    #make the question 1 buttons active
    for i in range(63, 70):
        Qbuttons[i].make_active(True)

def factoryQ2(Qbuttons):
    #make the question 1 buttons inactive
    for i in range(63, 70):
        Qbuttons[i].make_active(False)
    #make the question 2 buttons active
    for i in range(70, 76):
        Qbuttons[i].make_active(True)

def factoryQ3(Qbuttons):
    #make the question 2 buttons inactive
    for i in range(70, 76):
        Qbuttons[i].make_active(False)
    #make the question 3 buttons active
    for i in range(76, 82):
        Qbuttons[i].make_active(True)

def factoryQ4(Qbuttons):
    #make the question 3 buttons inactive
    for i in range(76, 82):
        Qbuttons[i].make_active(False)
    #make the question 4 buttons active
    for i in range(82, 87):
        Qbuttons[i].make_active(True)

def factoryEnd(Qbuttons, answers):
    #make the question 4 buttons inactive
    for i in range(82, 87):
        Qbuttons[i].make_active(False)
    #makes the quit button active
    Qbuttons[0].make_active(True)
    #check the number of correct answers
    number_correct, total=answers.check_correctA("Factory based")
    Qbuttons[167].change_text("You got %s out of %s!" % (number_correct, total), 18)
    Qbuttons[166].make_active(True)
    Qbuttons[167].make_active(True)

def marketQ1(Qbuttons):
    #make the question 1 buttons active
    for i in range(87, 94):
        Qbuttons[i].make_active(True)

def marketQ2(Qbuttons):
    #make the question 1 buttons inactive
    for i in range(87, 94):
        Qbuttons[i].make_active(False)
    #make the question 2 buttons active
    for i in range(94, 100):
        Qbuttons[i].make_active(True)

def marketQ3(Qbuttons):
    #make the question 2 buttons inactive
    for i in range(94, 100):
        Qbuttons[i].make_active(False)
    #make the question 3 buttons active
    for i in range(100, 106):
        Qbuttons[i].make_active(True)

def marketQ4(Qbuttons):
    #make the question 3 buttons inactive
    for i in range(100, 106):
        Qbuttons[i].make_active(False)
    #make the question 4 buttons active
    for i in range(106, 112):
        Qbuttons[i].make_active(True)

def marketQ5(Qbuttons):
    #make the question 4 buttons inactive
    for i in range(106, 112):
        Qbuttons[i].make_active(False)
    #make the question 5 buttons active
    for i in range(112, 118):
        Qbuttons[i].make_active(True)

def marketEnd(Qbuttons, answers):
    #make the question 5 buttons inactive
    for i in range(112, 118):
        Qbuttons[i].make_active(False)
    #makes the quit button active
    Qbuttons[0].make_active(True)
    #check the number of correct answers
    number_correct, total=answers.check_correctA("Market town")
    Qbuttons[167].change_text("You got %s out of %s!" % (number_correct, total), 18)
    Qbuttons[166].make_active(True)
    Qbuttons[167].make_active(True)

def urbanQ1(Qbuttons):
    #make the question 1 buttons active
    for i in range(118, 125):
        Qbuttons[i].make_active(True)

def urbanQ2(Qbuttons):
    #make the question 1 buttons inactive
    for i in range(118, 125):
        Qbuttons[i].make_active(False)
    #make the question 2 buttons active
    for i in range(125, 131):
        Qbuttons[i].make_active(True)

def urbanQ3(Qbuttons):
    #make the question 2 buttons inactive
    for i in range(125, 131):
        Qbuttons[i].make_active(False)
    #make the question 3 buttons active
    for i in range(131, 137):
        Qbuttons[i].make_active(True)

def urbanQ4(Qbuttons):
    #make the question 3 buttons inactive
    for i in range(131, 137):
        Qbuttons[i].make_active(False)
    #make the question 4 buttons active
    for i in range(137, 143):
        Qbuttons[i].make_active(True)

def urbanEnd(Qbuttons, answers):
    #make the question 4 buttons inactive
    for i in range(137, 143):
        Qbuttons[i].make_active(False)
    #makes the quit button active
    Qbuttons[0].make_active(True)
    #check the number of correct answers
    number_correct, total=answers.check_correctA("Urban city")
    Qbuttons[167].change_text("You got %s out of %s!" % (number_correct, total), 18)
    Qbuttons[166].make_active(True)
    Qbuttons[167].make_active(True)

def favelaQ1(Qbuttons):
    #make the question 1 buttons active
    for i in range(143, 149):
        Qbuttons[i].make_active(True)

def favelaQ2(Qbuttons):
    #make the question 1 buttons inactive
    for i in range(143, 149):
        Qbuttons[i].make_active(False)
    #make the question 2 buttons active
    for i in range(149, 155):
        Qbuttons[i].make_active(True)

def favelaQ3(Qbuttons):
    #make the question 2 buttons inactive
    for i in range(149, 155):
        Qbuttons[i].make_active(False)
    #make the question 3 buttons active
    for i in range(155, 160):
        Qbuttons[i].make_active(True)

def favelaQ4(Qbuttons):
    #make the question 3 buttons inactive
    for i in range(155, 160):
        Qbuttons[i].make_active(False)
    #make the question 4 buttons active
    for i in range(160, 166):
        Qbuttons[i].make_active(True)

def favelaEnd(Qbuttons, answers):
    #make the question 4 buttons inactive
    for i in range(160, 166):
        Qbuttons[i].make_active(False)
    #makes the quit button active
    Qbuttons[0].make_active(True)
    #check the number of correct answers
    number_correct, total=answers.check_correctA("Favela")
    Qbuttons[167].change_text("You got %s out of %s!" % (number_correct, total), 18)
    Qbuttons[166].make_active(True)
    Qbuttons[167].make_active(True)
