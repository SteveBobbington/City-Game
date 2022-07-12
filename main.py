###build a city

import pygame
import building_class, city_class, file_work, button_class, city_class, menu
import random, time, math


class Interface:
    def __init__(self, screen):
        #the screen
        self.screen=screen
        #the lists of things to draw each tick
        self.texts_to_draw=[]
        self.text_rects_to_draw=[]
        self.boxes_to_draw=[]
        self.box_rects_to_draw=[]
        self.current_popup_box=[]
        self.current_popup_box_rect=[]
        self.current_popup_texts=[]
        self.current_popup_text_rects=[]
        self.highlight=None

    #gets an input from the user for their player name
    def get_name(self, city):
        city.player_name="Player"
        #creates the objects on the screen for the player to use
        self.quit_button=button_class.Button((20, 20, 140, 40), button_class.button_quit, "Quit")
        self.player_box, self.player_box_rect=menu.add_box((220, 150, 200, 60), "pictures/name box.png")
        self.player_text, self.player_text_rect=menu.add_text((self.player_box_rect[0]+20, self.player_box_rect[1]+10, 160, 40), "Enter player name", "white")
        self.input_box, self.input_box_rect=menu.add_box((70, 250, 500, 60), "pictures/name box.png")
        text=""
        #takes the input from the user when keys are pressed
        #and displays it on the screen until enter is pressed
        while city.player_name=="Player":
            for event in pygame.event.get():
                self.quit_button.is_pressed()
                #if the keyboard has been pressed
                if event.type==pygame.KEYDOWN:
                    #if it was return
                    if event.key==pygame.K_RETURN:
                        #set the players name
                        city.player_name=text
                    #if backspace was pressed
                    elif event.key==pygame.K_BACKSPACE:
                        #remove the most recent character
                        text=text[:-1]
                    else:
                        #if anything other than comma is pressed
                        if event.unicode!=",":
                            #add it to name
                            text+=event.unicode
            #redraws the screen so the new text inputted is shown
            background=pygame.image.load("pictures/question background.png")
            background=pygame.transform.scale(background, [640, 480])
            self.screen.blit(background, (0, 0))
            self.text_surface, self.text_surface_rect=menu.add_text((self.input_box_rect[0]+15, self.input_box_rect[1]+10, (23*len(text) if len(text)<=19 else 460), 40), text, "white")
            self.quit_button.draw(self.screen)
            self.screen.blit(self.player_box, self.player_box_rect)
            self.screen.blit(self.player_text, self.player_text_rect)
            self.screen.blit(self.input_box, self.input_box_rect)
            self.screen.blit(self.text_surface, self.text_surface_rect)
            #update the screen
            pygame.display.update()

    def create_stats(self, city):
        #adds the stats box
        stats_image, stats_rect=menu.add_box((460, 10, 160, 80), "pictures/button.png")
        #displays the money the player has
        if city.get_gains()[0]<0:
            text_gain=" ("+str(round(city.get_gains()[0]))+")"
        elif city.get_gains()[0]>0:
            text_gain=" (+"+str(round(city.get_gains()[0]))+")"
        else:
            text_gain=""
        stats_text1, stats_text_rect1=menu.add_text((stats_rect[0]+10, stats_rect[1]+5, 60+9*int((len(str(round(city.get_money())))+len(str(text_gain))/2)), 20), "Money: "+str(round(city.get_money()))+text_gain, "black")
        #displays the current population
        stats_text2, stats_text_rect2=menu.add_text((stats_rect[0]+10, stats_rect[1]+30, 90+10*len(str(city.get_population())), 20), "Population: %s" % str(city.get_population()), "black")
        #adds these to their respective lists for drawing
        self.boxes_to_draw.append(stats_image)
        self.box_rects_to_draw.append(stats_rect)
        self.texts_to_draw.append(stats_text1)
        self.text_rects_to_draw.append(stats_text_rect1)
        self.texts_to_draw.append(stats_text2)
        self.text_rects_to_draw.append(stats_text_rect2)
        #if the defficiency technology has been bought
        if city.technology[1]==True:
            #displays the population needed
            stats_text3, stats_text_rect3=menu.add_text((stats_rect[0]+10, stats_rect[1]+55, 130, 20), "People needed: "+str(city.get_gains()[1]), "black")
            self.texts_to_draw.append(stats_text3)
            self.text_rects_to_draw.append(stats_text_rect3)

    def popup(self, *texts):
        #if the list isn't empty
        if self.current_popup_box==[]:
            #add this to the end on the texts list
            texts+=("Press enter to close",)
            #find the length of the largest text
            largest_text_len=0
            for text in texts:
                if len(text)>largest_text_len:
                    largest_text_len=len(text)
            #220-5*the length of the largest text
            box_x=220-largest_text_len*5
            #180-10*the number of texts
            box_y=180-10*len(texts)
            #20+10*the length of the largest text
            box_width=20+10*largest_text_len
            #20+25*the number of texts
            box_height=20+25*len(texts)
            box_rect=(box_x, box_y, box_width, box_height)
            self.current_popup_box.append(menu.add_box(box_rect, "pictures/button.png")[0])
            self.current_popup_box_rect.append(menu.add_box(box_rect, "pictures/button.png")[1])
            for i in range(0, len(texts)):
                #x of box+half of width of box-5*the length of the text
                text_x=self.current_popup_box_rect[0][0]+self.current_popup_box_rect[0][2]/2-5*len(texts[i])
                #y of the box+10 (for the top)+25*the number of texts already written
                text_y=self.current_popup_box_rect[0][1]+10+25*i
                #10*the number of letter in the text
                text_width=10*len(texts[i])
                new_rect=(text_x, text_y, text_width, 20)
                self.current_popup_texts.append(menu.add_text(new_rect, texts[i], "black")[0])
                self.current_popup_text_rects.append(menu.add_text(new_rect, texts[i], "black")[1])

    def clear_popup(self):
        #remove all popups
        self.current_popup_box.clear()
        self.current_popup_box_rect.clear()
        self.current_popup_texts.clear()
        self.current_popup_text_rects.clear()

    #draws all texts on the screen
    def draw_text(self, city, game_end):
        #deletes the current objects needed to draw each tick from their lists
        self.boxes_to_draw.clear()
        self.box_rects_to_draw.clear()
        self.texts_to_draw.clear()
        self.text_rects_to_draw.clear()
        #if the game is being played
        if city.get_playing():
            #create the stats box
            self.create_stats(city)
        #if the game has ended create the end game box
        if game_end:
            self.draw_city_type(city, city.get_city_type())
        #draw all boxes and text
        for i in range(0, len(self.boxes_to_draw)):
            self.screen.blit(self.boxes_to_draw[i], self.box_rects_to_draw[i])
        for i in range(0, len(self.texts_to_draw)):
            self.screen.blit(self.texts_to_draw[i], self.text_rects_to_draw[i])

    #draws all buttons in the list
    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw(self.screen)

    #draw the current popup (if there is one)
    def draw_popup(self):
        #if the popup list isn't empty
        if self.current_popup_box!=[]:
            #draw the popups to the screen
            #(although it should be only possible to have one popup)
            for i in range(0, len(self.current_popup_box)):
                self.screen.blit(self.current_popup_box[i], self.current_popup_box_rect[i])
            for i in range(0, len(self.current_popup_texts)):
                self.screen.blit(self.current_popup_texts[i], self.current_popup_text_rects[i])

    def get_leaderboard(self):
        #open the leaderboard file
        file=open("leaderboard.txt", "r")
        scores=file.read().splitlines()
        file.close()
        for i in range(0, len(scores)):
            scores[i]=scores[i].split(",")
        #create a popup to show the scores
        self.popup("These are the current high scores:", str(scores[0][0])+"   "+str(scores[0][1]), str(scores[1][0])+"   "+str(scores[1][1]), str(scores[2][0])+"   "+str(scores[2][1]), str(scores[3][0])+"   "+str(scores[3][1]), str(scores[4][0])+"   "+str(scores[4][1]))

    #draws the box displaying the city type at the end of the game
    def draw_city_type(self, city, city_type):
        #deletes the current objects needed to draw each tick from their lists
        self.boxes_to_draw.clear()
        self.box_rects_to_draw.clear()
        self.texts_to_draw.clear()
        self.text_rects_to_draw.clear()
        city_type_box, city_type_rect=menu.add_box((195, 30, 230, 110), "pictures/button.png")
        city_type_text1, city_type_text_rect1=menu.add_text((205, 40, 210, 20), "End of game", "black", 18)
        city_type_text2, city_type_text_rect2=menu.add_text((205, 60, 210, 20), "You got a %s!" % city_type, "black", 16)
        city_type_text3, city_type_text_rect3=menu.add_text((205, 80, 210, 20), "Your score is %s!" % city.get_score(), "black", 16)
        city_type_text4, city_type_text_rect4=menu.add_text((205, 110, 210, 20), "Quiz:", "black", 16)
        self.boxes_to_draw.append(city_type_box)
        self.box_rects_to_draw.append(city_type_rect)
        self.boxes_to_draw.append(city_type_text1)
        self.box_rects_to_draw.append(city_type_text_rect1)
        self.boxes_to_draw.append(city_type_text2)
        self.box_rects_to_draw.append(city_type_text_rect2)
        self.boxes_to_draw.append(city_type_text3)
        self.box_rects_to_draw.append(city_type_text_rect3)
        self.boxes_to_draw.append(city_type_text4)
        self.box_rects_to_draw.append(city_type_text_rect4)

    def add_highlight(self, Xpos, Ypos):
        self.highlight=building_class.Highlight(Xpos, Ypos)

    def remove_highlight(self):
        self.highlight=None

    def draw_highlight(self):
        if self.highlight!=None:
            self.highlight.draw(self.screen)


#class to store the answers to the questions at the end
class Answers:
    def __init__(self):
        #all the questions are default option 0 for haven't been answered
        self.Q1A=self.Q2A=self.Q3A=self.Q4A=self.Q5A=0
        self.correct_globalA={1:3, 2:2, 3:1, 4:2, 5:2}
        self.correct_knowledgeA={1:4, 2:3, 3:2, 4:1, 5:0}
        self.correct_factoryA={1:3, 2:4, 3:1, 4:2, 5:0}
        self.correct_marketA={1:3, 2:3, 3:1, 4:3, 5:2}
        self.correct_urbanA={1:3, 2:3, 3:2, 4:1, 5:0}
        self.correct_favelaA={1:3, 2:2, 3:1, 4:1, 5:0}

    #will update the answer to a question
    def answer_question(self, question_no, city_type, answer):
        if question_no==1:
            self.Q1A=answer
        elif question_no==2:
            self.Q2A=answer
        elif question_no==3:
            self.Q3A=answer
        elif question_no==4:
            self.Q4A=answer
        elif question_no==5:
            self.Q5A=answer

    def check_correctA(self, city_type):
        #this defines the dictionary with the questions and answers
        #needed for the city type, meaning they can be refernced with
        #the users input, rather than creating it before the inputs are input
        self.usersA={1:self.Q1A, 2:self.Q2A, 3:self.Q3A, 4:self.Q4A, 5:self.Q5A}
        number_correct=0
        total=0
        #determine which correct answers to use
        if city_type=="Global giant":
            correctA=self.correct_globalA
        elif city_type=="Knowledge capital":
            correctA=self.correct_knowledgeA
        elif city_type=="Factory based":
            correctA=self.correct_factoryA
        elif city_type=="Market town":
            correctA=self.correct_marketA
        elif city_type=="Urban city":
            correctA=self.correct_urbanA
        elif city_type=="Favela":
            correctA=self.correct_favelaA
        #for every question that has been answered
        for question in self.usersA:
            #if the users answer is the same as the correct answer
            if self.usersA[question]==correctA[question] and correctA[question]!=0:
                #increase the nuber of correct answers
                number_correct+=1
            if correctA[question]!=0:
                #add to the questions answered
                total+=1
        return number_correct, total

def main():
    ###initialise pygame screen and variables
    pygame.init()
    #load logo
    #this is a constant
    logo=pygame.image.load("pictures/logo.png")
    pygame.display.set_icon(logo)
    #set game title
    pygame.display.set_caption("Build a city")
    #creates the screen
    #this is a constant
    screen_size=[640, 480]
    screen=pygame.display.set_mode(screen_size)
    #background
    background=pygame.image.load("pictures/grass.png")
    background=pygame.transform.scale(background, screen_size)
    #background for quiz section
    question_background=pygame.image.load("pictures/question background.png")
    question_background=pygame.transform.scale(question_background, screen_size)
    #menu box
    orange_metal=pygame.image.load("pictures/orange metal.jpg")
    orange_metal=pygame.transform.scale(orange_metal, (200, 480))
    #initialises clock
    clock=pygame.time.Clock()

    #create city
    city=city_class.City()

    #create interface
    interface=Interface(screen)
    
    #instantiate the answers class
    answers=Answers()
    
    #set buttons as an instance of the button class
    #file buttons [1][3][4]
    save_button=button_class.Button((470, 320, 140, 40), lambda:file_work.save(city), "Save")
    load_button=button_class.Button((470, 270, 140, 40), lambda:file_work.load(interface, city, buttons, "main"), "Load")
    restart_button=button_class.Button((470, 320, 140, 40), lambda:file_work.restart(city, buttons, interface), "Restart")
    #menu buttons [2][0][5]-[7][19]
    play_button=button_class.Button((470, 50, 140, 40), (lambda:city.set_playing_type("main"), lambda:menu.display_game_menu(buttons), lambda:city.add_empty(buttons, interface), lambda:city.change_playing(True)), "Play")
    menu_button=button_class.Button((470, 420, 140, 40), lambda:menu.display_main_menu(buttons, city), "Menu")
    quit_button=button_class.Button((470, 370, 140, 40), button_class.button_quit, "Quit")
    back_button=button_class.Button((470, 420, 140, 40), lambda:menu.display_main_menu(buttons, city), "Back")
    ingame_back_button=button_class.Button((470, 420, 140, 40), (interface.remove_highlight, lambda:menu.display_game_menu(buttons)), "Back")
    rename_button=button_class.Button((470, 220, 140, 40), lambda:interface.get_name(city), "Rename")
    #the prints as functions are temporary
    #building buttons [8]-[18][32]
    house_button=button_class.Button_with_info((445, 100, 90, 40), print, "House", "Will add 5 people - costs 2000")
    shop_button=button_class.Button_with_info((445, 150, 90, 40), print, "Shop", "Adds £15 per second per person - costs 2000")
    school_button=button_class.Button_with_info((445, 200, 90, 40), print, "School", "Unlocks buildings - costs 5000")
    hospital_button=button_class.Button_with_info((445, 250, 90, 40), print, "Hospital", "Decrease living costs - costs 3500")
    road_button=button_class.Button_with_info((445, 300, 90, 40), print, "Road", "Increase quality of life - costs 1000")
    factory_button=button_class.Button_with_info((445, 350, 90, 40), print, "Factory", "Adds £8 per second per person - costs 2000")
    police_station_button=button_class.Button_with_info((545, 100, 90, 40), print, "Police", "Reduces crime rates - costs 3000")
    bank_button=button_class.Button_with_info((545, 150, 90, 40), print, "Bank", "Increases money earned by 5% - costs 4500")
    power_station_button=button_class.Button_with_info((545, 200, 90, 40), print, "Power", "Increases money made by factories - costs 4000")
    entertainment_button=button_class.Button_with_info((545, 250, 90, 40), print, "Leisure", "Increases quality of life - costs 2500")
    lab_button=button_class.Button_with_info((545, 300, 90, 40), print, "Lab", "Decreases technology costs - costs 8000")
    church_button=button_class.Button_with_info((545, 350, 90, 40), print, "Church", "Adds money depending on no. of houses - costs 5000")
    #specific building buttons [20][21][33]
    upgrade_button=button_class.Button((470, 250, 140, 40), print, "Upgrade")
    destroy_button=button_class.Button((470, 300, 140, 40), print, "Destroy")
    repair_button=button_class.Button((470, 350, 140, 40), print, "Repair")
    #[22]-[26][34] aren't used as buttons but the easiest way to create them
    #at the right time is to treat them as buttons so the indiv building menu
    #can use them
    indiv_building_box=button_class.Button((460, 100, 160, 140), print, "")
    indiv_building_text1=button_class.Button((470, 105, 140, 20), print, "")
    indiv_building_text2=button_class.Button((470, 125, 140, 20), print, "")
    indiv_building_text3=button_class.Button((470, 145, 140, 20), print, "")
    indiv_building_text4=button_class.Button((470, 165, 140, 20), print, "")
    indiv_building_text5=button_class.Button((470, 185, 140, 20), print, "")
    indiv_building_box.change_use("box")
    indiv_building_text1.change_use("text")
    indiv_building_text2.change_use("text")
    indiv_building_text3.change_use("text")
    indiv_building_text4.change_use("text")
    indiv_building_text5.change_use("text")
    #technology buttons [27]-[31]
    technology_button=button_class.Button((470, 270, 140, 40), lambda:menu.display_technology_menu(buttons, city), "Technology")
    skyscraper_button=button_class.Button_with_info((470, 120, 140, 40), (lambda:city.buy_technology("skyscrapers", interface), lambda:menu.display_game_menu(buttons)), "Skyscrapers", "Level 3 houses give more people")
    deficiency_button=button_class.Button_with_info((470, 170, 140, 40), (lambda:city.buy_technology("deficiency", interface), lambda:menu.display_game_menu(buttons)), "Defficiency", "Displays how many more people are needed")
    engineers_button=button_class.Button_with_info((470, 220, 140, 40), (lambda:city.buy_technology("engineers", interface), lambda:menu.display_game_menu(buttons)), "Engineers", "Halves construction time")
    smart_buildings_button=button_class.Button_with_info((470, 270, 140, 40), (lambda:city.buy_technology("smart_buildings", interface), lambda:menu.display_game_menu(buttons)), "Smart Buildings", "Some buildings are built to level 2")
    #leaderboard button [35]
    leaderboard_button=button_class.Button((470, 170, 140, 40), interface.get_leaderboard, "Leaderboard")
    #missions button [36]
    missions_button=button_class.Button((470, 100, 140, 40), lambda:file_work.load(interface, city, buttons, "mission"), "Missions")
    #continue button [37]
    continue_button=button_class.Button((470, 100, 140, 40), lambda:menu.display_game_menu(buttons), "Continue")
    #to display the time the gme has been playing [38][39]
    time_box=button_class.Button((470, 100, 140, 40), print, "")
    time_text=button_class.Button((470, 100, 140, 40), print, "")
    time_box.change_use("box")
    time_text.change_use("text")
    #end game question buttons [1]-[7]
    globalQ1box=button_class.Button((100, 160, 440, 60), print, "")
    globalQ1text1=button_class.Button((110, 164, 420, 20), print, "What magnitude of population would you expect")
    globalQ1text2=button_class.Button((110, 190, 420, 20), print, "from the average global giant?")
    globalQ1op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(1, "Global giant", 1), lambda:menu.globalQ2(Qbuttons)), "50,000")
    globalQ1op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(1, "Global giant", 2), lambda:menu.globalQ2(Qbuttons)), "500,000")
    globalQ1op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(1, "Global giant", 3), lambda:menu.globalQ2(Qbuttons)), "5,000,000")
    globalQ1op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(1, "Global giant", 4), lambda:menu.globalQ2(Qbuttons)), "50,000,000")
    globalQ1box.change_use("box")
    globalQ1text1.change_use("text")
    globalQ1text2.change_use("text")
    #[8]-[12]
    globalQ2box=button_class.Button((120, 160, 400, 60), print, "")
    globalQ2text1=button_class.Button((130, 165, 380, 20), print, "Would you expect to find a global giant")
    globalQ2text2=button_class.Button((130, 190, 380, 20), print, "in a low income or high income country?")
    globalQ2op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(2, "Global giant", 1), lambda:menu.globalQ3(Qbuttons)), "LIC")
    globalQ2op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(2, "Global giant", 2), lambda:menu.globalQ3(Qbuttons)), "HIC")
    globalQ2box.change_use("box")
    globalQ2text1.change_use("text")
    globalQ2text2.change_use("text")
    #[13]-[18]
    globalQ3box=button_class.Button((100, 160, 440, 40), print, "")
    globalQ3text1=button_class.Button((110, 170, 420, 20), print, "Which of these is an example of a global giant?")
    globalQ3op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(3, "Global giant", 1), lambda:menu.globalQ4(Qbuttons)), "London")
    globalQ3op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(3, "Global giant", 2), lambda:menu.globalQ4(Qbuttons)), "Rio de Janeiro")
    globalQ3op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(3, "Global giant", 3), lambda:menu.globalQ4(Qbuttons)), "Beijing")
    globalQ3op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(3, "Global giant", 4), lambda:menu.globalQ4(Qbuttons)), "Stockholm")
    globalQ3box.change_use("box")
    globalQ3text1.change_use("text")
    #[19]-[25]
    globalQ4box=button_class.Button((130, 140, 360, 80), print, "")
    globalQ4text1=button_class.Button((140, 145, 340, 20), print, "Is a global giant more likely to be")
    globalQ4text2=button_class.Button((140, 170, 340, 20), print, "in a less developed, more developed,")
    globalQ4text3=button_class.Button((140, 195, 340, 20), print, "or newly industrialised country?")
    globalQ4op1=button_class.Button((100, 240, 180, 40), (lambda:answers.answer_question(4, "Global giant", 1), lambda:menu.globalQ5(Qbuttons)), "Less developed")
    globalQ4op2=button_class.Button((100, 290, 180, 40), (lambda:answers.answer_question(4, "Global giant", 2), lambda:menu.globalQ5(Qbuttons)), "More developed")
    globalQ4op3=button_class.Button((100, 340, 180, 40), (lambda:answers.answer_question(4, "Global giant", 3), lambda:menu.globalQ5(Qbuttons)), "Newly industrialised")
    globalQ4box.change_use("box")
    globalQ4text1.change_use("text")
    globalQ4text2.change_use("text")
    globalQ4text3.change_use("text")
    #[26]-[31]
    globalQ5box=button_class.Button((130, 160, 340, 60), print, "")
    globalQ5text1=button_class.Button((140, 165, 320, 20), print, "Would a global giant have a")
    globalQ5text2=button_class.Button((140, 190, 320, 20), print, "low medium or high crime rate?")
    globalQ5op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(5, "Global giant", 1), lambda:menu.globalEnd(Qbuttons, answers)), "Low")
    globalQ5op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(5, "Global giant", 2), lambda:menu.globalEnd(Qbuttons, answers)), "Medium")
    globalQ5op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(5, "Global giant", 3), lambda:menu.globalEnd(Qbuttons, answers)), "High")
    globalQ5box.change_use("box")
    globalQ5text1.change_use("text")
    globalQ5text2.change_use("text")
    #[32]-[38]
    knowledgeQ1box=button_class.Button((100, 160, 340, 60), print, "")
    knowledgeQ1text1=button_class.Button((110, 165, 320, 20), print, "What is a knowledge capital known")
    knowledgeQ1text2=button_class.Button((110, 190, 320, 20), print, "for having lots of?")
    knowledgeQ1op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(1, "Knowledge capital", 1), lambda:menu.knowledgeQ2(Qbuttons)), "Education")
    knowledgeQ1op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(1, "Knowledge capital", 2), lambda:menu.knowledgeQ2(Qbuttons)), "Population")
    knowledgeQ1op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(1, "Knowledge capital", 3), lambda:menu.knowledgeQ2(Qbuttons)), "Export")
    knowledgeQ1op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(1, "Knowledge capital", 4), lambda:menu.knowledgeQ2(Qbuttons)), "Research")
    knowledgeQ1box.change_use("box")
    knowledgeQ1text1.change_use("text")
    knowledgeQ1text2.change_use("text")
    #[39]-[44]
    knowledgeQ2box=button_class.Button((100, 160, 470, 40), print, "")
    knowledgeQ2text1=button_class.Button((110, 170, 450, 20), print, "Which of these is an example of a knowledge capital?")
    knowledgeQ2op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(2, "Knowledge capital", 1), lambda:menu.knowledgeQ3(Qbuttons)), "London")
    knowledgeQ2op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(2, "Knowledge capital", 2), lambda:menu.knowledgeQ3(Qbuttons)), "Rio de Janeiro")
    knowledgeQ2op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(2, "Knowledge capital", 3), lambda:menu.knowledgeQ3(Qbuttons)), "Stockholm")
    knowledgeQ2op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(2, "Knowledge capital", 4), lambda:menu.knowledgeQ3(Qbuttons)), "Beijing")
    knowledgeQ2box.change_use("box")
    knowledgeQ2text1.change_use("text")
    #[45]-[51]
    knowledgeQ3box=button_class.Button((140, 140, 360, 80), print, "")
    knowledgeQ3text1=button_class.Button((150, 145, 340, 20), print, "Is a knowledge capital more likely to be")
    knowledgeQ3text2=button_class.Button((150, 170, 340, 20), print, "in a less developed, more developed,")
    knowledgeQ3text3=button_class.Button((150, 195, 340, 20), print, "or newly industrialised country?")
    knowledgeQ3op1=button_class.Button((100, 240, 180, 40), (lambda:answers.answer_question(3, "Knowledge capital", 1), lambda:menu.knowledgeQ4(Qbuttons)), "Less developed")
    knowledgeQ3op2=button_class.Button((100, 290, 180, 40), (lambda:answers.answer_question(3, "Knowledge capital", 2), lambda:menu.knowledgeQ4(Qbuttons)), "More developed")
    knowledgeQ3op3=button_class.Button((100, 340, 180, 40), (lambda:answers.answer_question(3, "Knowledge capital", 3), lambda:menu.knowledgeQ4(Qbuttons)), "Newly industrialised")
    knowledgeQ3box.change_use("box")
    knowledgeQ3text1.change_use("text")
    knowledgeQ3text2.change_use("text")
    knowledgeQ3text3.change_use("text")
    #[52]-[62]
    knowledgeQ4box=button_class.Button((80, 160, 300, 40), print, "")
    knowledgeQ4text1=button_class.Button((90, 165, 280, 20), print, "Define a knowledge capital")
    knowledgeQ4op1=button_class.Button((80, 220, 340, 60), (lambda:answers.answer_question(4, "Knowledge capital", 1), lambda:menu.knowledgeEnd(Qbuttons, answers)), "")
    knowledgeQ4op2=button_class.Button((80, 290, 340, 60), (lambda:answers.answer_question(4, "Knowledge capital", 2), lambda:menu.knowledgeEnd(Qbuttons, answers)), "")
    knowledgeQ4op3=button_class.Button((80, 360, 340, 60), (lambda:answers.answer_question(4, "Knowledge capital", 3), lambda:menu.knowledgeEnd(Qbuttons, answers)), "")
    knowledgeQ4op1text1=button_class.Button((80, 215, 340, 40), print, "A city which provides valuable ideas,")
    knowledgeQ4op1text2=button_class.Button((80, 235, 340, 40), print, "methods and processes to a country")
    knowledgeQ4op2text1=button_class.Button((80, 285, 340, 40), print, "A city which provides a")
    knowledgeQ4op2text2=button_class.Button((80, 305, 340, 40), print, "high level of education")
    knowledgeQ4op3text1=button_class.Button((80, 355, 340, 40), print, "A city which is a primal node")
    knowledgeQ4op3text2=button_class.Button((80, 375, 340, 40), print, "in the economic network")
    knowledgeQ4box.change_use("box")
    knowledgeQ4text1.change_use("text")
    knowledgeQ4op1text1.change_use("text")
    knowledgeQ4op1text2.change_use("text")
    knowledgeQ4op2text1.change_use("text")
    knowledgeQ4op2text2.change_use("text")
    knowledgeQ4op3text1.change_use("text")
    knowledgeQ4op3text2.change_use("text")
    #[63]-[69]
    factoryQ1box=button_class.Button((140, 140, 360, 80), print, "")
    factoryQ1text1=button_class.Button((150, 145, 340, 20), print, "Is a factory based city more likely to be")
    factoryQ1text2=button_class.Button((150, 170, 340, 20), print, "in a less developed, more developed,")
    factoryQ1text3=button_class.Button((80, 195, 480, 20), print, "or newly industrialised country?")
    factoryQ1op1=button_class.Button((100, 240, 180, 40), (lambda:answers.answer_question(1, "Factory based", 1), lambda:menu.factoryQ2(Qbuttons)), "Less developed")
    factoryQ1op2=button_class.Button((100, 290, 180, 40), (lambda:answers.answer_question(1, "Factory based", 2), lambda:menu.factoryQ2(Qbuttons)), "More developed")
    factoryQ1op3=button_class.Button((100, 340, 180, 40), (lambda:answers.answer_question(1, "Factory based", 3), lambda:menu.factoryQ2(Qbuttons)), "Newly industrialised")
    factoryQ1box.change_use("box")
    factoryQ1text1.change_use("text")
    factoryQ1text2.change_use("text")
    factoryQ1text3.change_use("text")
    #[70]-[75]
    factoryQ2box=button_class.Button((100, 160, 470, 40), print, "")
    factoryQ2text1=button_class.Button((110, 170, 450, 20), print, "Which of these is an example of a factory based city?")
    factoryQ2op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(2, "Factory based", 1), lambda:menu.factoryQ3(Qbuttons)), "London")
    factoryQ2op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(2, "Factory based", 2), lambda:menu.factoryQ3(Qbuttons)), "Rio de Janeiro")
    factoryQ2op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(2, "Factory based", 3), lambda:menu.factoryQ3(Qbuttons)), "Stockholm")
    factoryQ2op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(2, "Factory based", 4), lambda:menu.factoryQ3(Qbuttons)), "Beijing")
    factoryQ2box.change_use("box")
    factoryQ2text1.change_use("text")
    #[76]-[81]
    factoryQ3box=button_class.Button((140, 140, 360, 60), print, "")
    factoryQ3text1=button_class.Button((150, 145, 340, 20), print, "Does a factory based city have a low,")
    factoryQ3text2=button_class.Button((150, 170, 340, 20), print, "medium, or high quality of life?")
    factoryQ3op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(3, "Factory based", 1), lambda:menu.factoryQ4(Qbuttons)), "Low")
    factoryQ3op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(3, "Factory based", 2), lambda:menu.factoryQ4(Qbuttons)), "Medium")
    factoryQ3op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(3, "Factory based", 3), lambda:menu.factoryQ4(Qbuttons)), "High")
    factoryQ3box.change_use("box")
    factoryQ3text1.change_use("text")
    factoryQ3text2.change_use("text")
    #[82]-[86]
    factoryQ4box=button_class.Button((140, 140, 360, 60), print, "")
    factoryQ4text1=button_class.Button((150, 145, 340, 20), print, "Would you expect to find a factory based")
    factoryQ4text2=button_class.Button((150, 170, 340, 20), print, "city in a low or high income country?")
    factoryQ4op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(4, "Factory based", 1), lambda:menu.factoryEnd(Qbuttons, answers)), "Low")
    factoryQ4op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(4, "Factory based", 2), lambda:menu.factoryEnd(Qbuttons, answers)), "High")
    factoryQ4box.change_use("box")
    factoryQ4text1.change_use("text")
    factoryQ4text2.change_use("text")
    #[87]-[93]
    marketQ1box=button_class.Button((130, 160, 360, 60), print, "")
    marketQ1text1=button_class.Button((140, 165, 340, 20), print, "What magnitude of population would you")
    marketQ1text2=button_class.Button((140, 190, 340, 20), print, "expect from the average market town?")
    marketQ1op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(1, "Market town", 1), lambda:menu.marketQ2(Qbuttons)), "500")
    marketQ1op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(1, "Market town", 2), lambda:menu.marketQ2(Qbuttons)), "5,000")
    marketQ1op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(1, "Market town", 3), lambda:menu.marketQ2(Qbuttons)), "50,000")
    marketQ1op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(1, "Market town", 4), lambda:menu.marketQ2(Qbuttons)), "500,000")
    marketQ1box.change_use("box")
    marketQ1text1.change_use("text")
    marketQ1text2.change_use("text")
    #[94]-[99]
    marketQ2box=button_class.Button((160, 150, 300, 60), print, "")
    marketQ2text1=button_class.Button((170, 155, 280, 20), print, "Does a market town have a low,")
    marketQ2text2=button_class.Button((170, 180, 280, 20), print, "medium, or high quality of life?")
    marketQ2op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(2, "Market town", 1), lambda:menu.marketQ3(Qbuttons)), "Low")
    marketQ2op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(2, "Market town", 2), lambda:menu.marketQ3(Qbuttons)), "Medium")
    marketQ2op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(2, "Market town", 3), lambda:menu.marketQ3(Qbuttons)), "High")
    marketQ2box.change_use("box")
    marketQ2text1.change_use("text")
    marketQ2text2.change_use("text")
    #[100]-[105]
    marketQ3box=button_class.Button((100, 160, 420, 40), print, "")
    marketQ3text1=button_class.Button((110, 167, 400, 20), print, "Where would you expect to find a market town?")
    marketQ3op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(3, "Market town", 1), lambda:menu.marketQ4(Qbuttons)), "Europe")
    marketQ3op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(3, "Market town", 2), lambda:menu.marketQ4(Qbuttons)), "South America")
    marketQ3op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(3, "Market town", 3), lambda:menu.marketQ4(Qbuttons)), "Asia")
    marketQ3op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(3, "Market town", 4), lambda:menu.marketQ4(Qbuttons)), "Africa")
    marketQ3box.change_use("box")
    marketQ3text1.change_use("text")
    #[106]-[111]
    marketQ4box=button_class.Button((140, 160, 320, 60), print, "")
    marketQ4text1=button_class.Button((150, 165, 300, 20), print, "What is the difference between")
    marketQ4text2=button_class.Button((150, 190, 300, 20), print, "a market town and a village?")
    marketQ4op1=button_class.Button((60, 250, 380, 40), (lambda:answers.answer_question(4, "Market town", 1), lambda:menu.marketQ5(Qbuttons)), "Market town holds regular markets")
    marketQ4op2=button_class.Button((60, 300, 380, 40), (lambda:answers.answer_question(4, "Market town", 2), lambda:menu.marketQ5(Qbuttons)), "Market town has more producers within it")
    marketQ4op3=button_class.Button((60, 350, 380, 40), (lambda:answers.answer_question(4, "Market town", 3), lambda:menu.marketQ5(Qbuttons)), "Market town has the right to hold a market")
    marketQ4box.change_use("box")
    marketQ4text1.change_use("text")
    marketQ4text2.change_use("text")
    #[112]-[117]
    marketQ5box=button_class.Button((140, 160, 320, 60), print, "")
    marketQ5text1=button_class.Button((150, 165, 300, 20), print, "Does a market town have a low,")
    marketQ5text2=button_class.Button((150, 190, 300, 20), print, "medium, or high population density?")
    marketQ5op1=button_class.Button((100, 250, 140, 40), (lambda:answers.answer_question(5, "Market town", 1), lambda:menu.marketEnd(Qbuttons, answers)), "Low")
    marketQ5op2=button_class.Button((100, 300, 140, 40), (lambda:answers.answer_question(5, "Market town", 2), lambda:menu.marketEnd(Qbuttons, answers)), "Medium")
    marketQ5op3=button_class.Button((100, 350, 140, 40), (lambda:answers.answer_question(5, "Market town", 3), lambda:menu.marketEnd(Qbuttons, answers)), "High")
    marketQ5box.change_use("box")
    marketQ5text1.change_use("text")
    marketQ5text2.change_use("text")
    #[118]-[124]
    urbanQ1box=button_class.Button((130, 160, 360, 60), print, "")
    urbanQ1text1=button_class.Button((140, 165, 340, 20), print, "What magnitude of population would you")
    urbanQ1text2=button_class.Button((140, 190, 340, 20), print, "expect from the average Urban city?")
    urbanQ1op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(1, "Urban city", 1), lambda:menu.urbanQ2(Qbuttons)), "2,000")
    urbanQ1op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(1, "Urban city", 2), lambda:menu.urbanQ2(Qbuttons)), "20,000")
    urbanQ1op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(1, "Urban city", 3), lambda:menu.urbanQ2(Qbuttons)), "200,000")
    urbanQ1op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(1, "Urban city", 4), lambda:menu.urbanQ2(Qbuttons)), "2,000,000")
    urbanQ1box.change_use("box")
    urbanQ1text1.change_use("text")
    urbanQ1text2.change_use("text")
    #[125]-[130]
    urbanQ2box=button_class.Button((140, 160, 320, 60), print, "")
    urbanQ2text1=button_class.Button((150, 165, 300, 20), print, "Does a urban city have a low,")
    urbanQ2text2=button_class.Button((150, 190, 300, 20), print, "medium, or high population density?")
    urbanQ2op1=button_class.Button((100, 250, 140, 40), (lambda:answers.answer_question(2, "Urban city", 1), lambda:menu.urbanQ3(Qbuttons)), "Low")
    urbanQ2op2=button_class.Button((100, 300, 140, 40), (lambda:answers.answer_question(2, "Urban city", 2), lambda:menu.urbanQ3(Qbuttons)), "Medium")
    urbanQ2op3=button_class.Button((100, 350, 140, 40), (lambda:answers.answer_question(2, "Urban city", 3), lambda:menu.urbanQ3(Qbuttons)), "High")
    urbanQ2box.change_use("box")
    urbanQ2text1.change_use("text")
    urbanQ2text2.change_use("text")
    #[131]-[136]
    urbanQ3box=button_class.Button((180, 160, 260, 60), print, "")
    urbanQ3text1=button_class.Button((190, 165, 240, 20), print, "What % of land in an")
    urbanQ3text2=button_class.Button((190, 190, 240, 20), print, "urban city is residential?")
    urbanQ3op1=button_class.Button((100, 250, 140, 40), (lambda:answers.answer_question(3, "Urban city", 1), lambda:menu.urbanQ4(Qbuttons)), "20%")
    urbanQ3op2=button_class.Button((100, 300, 140, 40), (lambda:answers.answer_question(3, "Urban city", 2), lambda:menu.urbanQ4(Qbuttons)), "40%")
    urbanQ3op3=button_class.Button((100, 350, 140, 40), (lambda:answers.answer_question(3, "Urban city", 3), lambda:menu.urbanQ4(Qbuttons)), "60%")
    urbanQ3box.change_use("box")
    urbanQ3text1.change_use("text")
    urbanQ3text2.change_use("text")
    #[137]-[142]
    urbanQ4box=button_class.Button((160, 160, 300, 60), print, "")
    urbanQ4text1=button_class.Button((190, 165, 240, 20), print, "What type of commercial buildings")
    urbanQ4text2=button_class.Button((190, 190, 240, 20), print, "are more frequent in urban cities?")
    urbanQ4op1=button_class.Button((100, 250, 140, 40), (lambda:answers.answer_question(4, "Urban city", 1), lambda:menu.urbanEnd(Qbuttons, answers)), "Industrial")
    urbanQ4op2=button_class.Button((100, 300, 140, 40), (lambda:answers.answer_question(4, "Urban city", 2), lambda:menu.urbanEnd(Qbuttons, answers)), "Retail")
    urbanQ4op3=button_class.Button((100, 350, 140, 40), (lambda:answers.answer_question(4, "Urban city", 3), lambda:menu.urbanEnd(Qbuttons, answers)), "Offices")
    urbanQ4box.change_use("box")
    urbanQ4text1.change_use("text")
    urbanQ4text2.change_use("text")
    #[143]-[148]
    favelaQ1box=button_class.Button((140, 160, 320, 60), print, "")
    favelaQ1text1=button_class.Button((150, 165, 300, 20), print, "Does a favela have a low, medium,")
    favelaQ1text2=button_class.Button((150, 190, 300, 20), print, "or high population density?")
    favelaQ1op1=button_class.Button((100, 250, 140, 40), (lambda:answers.answer_question(1, "Favela", 1), lambda:menu.favelaQ2(Qbuttons)), "Low")
    favelaQ1op2=button_class.Button((100, 300, 140, 40), (lambda:answers.answer_question(1, "Favela", 2), lambda:menu.favelaQ2(Qbuttons)), "Medium")
    favelaQ1op3=button_class.Button((100, 350, 140, 40), (lambda:answers.answer_question(1, "Favela", 3), lambda:menu.favelaQ2(Qbuttons)), "High")
    favelaQ1box.change_use("box")
    favelaQ1text1.change_use("text")
    favelaQ1text2.change_use("text")
    #[149]-[154]
    favelaQ2box=button_class.Button((120, 160, 360, 40), print, "")
    favelaQ2text1=button_class.Button((130, 170, 340, 20), print, "Which of these is an example of a favela?")
    favelaQ2op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(2, "Favela", 1), lambda:menu.favelaQ3(Qbuttons)), "London")
    favelaQ2op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(2, "Favela", 2), lambda:menu.favelaQ3(Qbuttons)), "Rio de Janeiro")
    favelaQ2op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(2, "Favela", 3), lambda:menu.favelaQ3(Qbuttons)), "Stockholm")
    favelaQ2op4=button_class.Button((100, 390, 140, 40), (lambda:answers.answer_question(2, "Favela", 4), lambda:menu.favelaQ3(Qbuttons)), "Beijing")
    favelaQ2box.change_use("box")
    favelaQ2text1.change_use("text")
    #[155]-[159]
    favelaQ3box=button_class.Button((160, 140, 320, 60), print, "")
    favelaQ3text1=button_class.Button((170, 145, 300, 20), print, "Would you expect to find a favela")
    favelaQ3text2=button_class.Button((170, 170, 300, 20), print, "in a low or high income country?")
    favelaQ3op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(3, "Favela", 1), lambda:menu.favelaQ4(Qbuttons)), "Low")
    favelaQ3op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(3, "Favela", 2), lambda:menu.favelaQ4(Qbuttons)), "High")
    favelaQ3box.change_use("box")
    favelaQ3text1.change_use("text")
    favelaQ3text2.change_use("text")
    #[160]-[165]
    favelaQ4box=button_class.Button((160, 150, 300, 60), print, "")
    favelaQ4text1=button_class.Button((170, 155, 280, 20), print, "Does a favela have a low,")
    favelaQ4text2=button_class.Button((170, 180, 280, 20), print, "medium, or high quality of life?")
    favelaQ4op1=button_class.Button((100, 240, 140, 40), (lambda:answers.answer_question(4, "Favela", 1), lambda:menu.favelaEnd(Qbuttons, answers)), "Low")
    favelaQ4op2=button_class.Button((100, 290, 140, 40), (lambda:answers.answer_question(4, "Favela", 2), lambda:menu.favelaEnd(Qbuttons, answers)), "Medium")
    favelaQ4op3=button_class.Button((100, 340, 140, 40), (lambda:answers.answer_question(4, "Favela", 3), lambda:menu.favelaEnd(Qbuttons, answers)), "High")
    favelaQ4box.change_use("box")
    favelaQ4text1.change_use("text")
    favelaQ4text2.change_use("text")
    #to show how many questions are correct [166][167]
    Qcorrectbox=button_class.Button((200, 200, 220, 40), print, "")
    Qcorrecttext=button_class.Button((210, 210, 200, 20), print, "")
    Qcorrectbox.change_use("box")
    Qcorrecttext.change_use("text")
    #save score button [168]
    save_score_button=button_class.Button_with_info((470, 320, 140, 40), lambda:file_work.save_score(city), "Save score", "Put your score on the leaderboard")
    #list of all buttons in the game to be parsed when they are used
    buttons=[menu_button, save_button, play_button, load_button,\
             restart_button, quit_button, back_button, ingame_back_button,\
             house_button, shop_button, school_button,  hospital_button,\
             road_button, factory_button, police_station_button, bank_button,\
             power_station_button, entertainment_button, lab_button,\
             rename_button, upgrade_button, destroy_button,\
             indiv_building_box, indiv_building_text1, indiv_building_text2,\
             indiv_building_text3, indiv_building_text4, technology_button,\
             skyscraper_button, deficiency_button, engineers_button,\
             smart_buildings_button, church_button, repair_button,\
             indiv_building_text5, leaderboard_button, missions_button,\
             continue_button, time_box, time_text]
    #This is a seperate buttons list for the question buttons
    #I seperated them so i can only itterate through half the total which will
    #speed the game up. Quit button is in both as it is needed in both
    Qbuttons=[quit_button, globalQ1box, globalQ1text1, globalQ1text2,\
              globalQ1op1, globalQ1op2, globalQ1op3, globalQ1op4, globalQ2box,\
              globalQ2text1, globalQ2text2, globalQ2op1, globalQ2op2,\
              globalQ3box, globalQ3text1, globalQ3op1, globalQ3op2,\
              globalQ3op3, globalQ3op4, globalQ4box, globalQ4text1,\
              globalQ4text2, globalQ4text3, globalQ4op1, globalQ4op2,\
              globalQ4op3, globalQ5box, globalQ5text1, globalQ5text2,\
              globalQ5op1, globalQ5op2, globalQ5op3, knowledgeQ1box,\
              knowledgeQ1text1, knowledgeQ1text2, knowledgeQ1op1,\
              knowledgeQ1op2, knowledgeQ1op3, knowledgeQ1op4, knowledgeQ2box,\
              knowledgeQ2text1, knowledgeQ2op1, knowledgeQ2op2,\
              knowledgeQ2op3, knowledgeQ2op4, knowledgeQ3box, knowledgeQ3text1,\
              knowledgeQ3text2, knowledgeQ3text3, knowledgeQ3op1, knowledgeQ3op2,\
              knowledgeQ3op3, knowledgeQ4box, knowledgeQ4text1, knowledgeQ4op1,\
              knowledgeQ4op2, knowledgeQ4op3, knowledgeQ4op1text1,\
              knowledgeQ4op1text2, knowledgeQ4op2text1, knowledgeQ4op2text2,\
              knowledgeQ4op3text1, knowledgeQ4op3text2, factoryQ1box,\
              factoryQ1text1, factoryQ1text2, factoryQ1text3, factoryQ1op1,\
              factoryQ1op2, factoryQ1op3, factoryQ2box, factoryQ2text1,\
              factoryQ2op1, factoryQ2op2, factoryQ2op3, factoryQ2op4,\
              factoryQ3box, factoryQ3text1, factoryQ3text2, factoryQ3op1,\
              factoryQ3op2, factoryQ3op3, factoryQ4box, factoryQ4text1,\
              factoryQ4text2, factoryQ4op1, factoryQ4op2, marketQ1box,\
              marketQ1text1, marketQ1text2, marketQ1op1, marketQ1op2,\
              marketQ1op3, marketQ1op4, marketQ2box, marketQ2text1,\
              marketQ2text2, marketQ2op1, marketQ2op2, marketQ2op3,\
              marketQ3box, marketQ3text1, marketQ3op1, marketQ3op2,\
              marketQ3op3, marketQ3op4, marketQ4box, marketQ4text1,\
              marketQ4text2, marketQ4op1, marketQ4op2, marketQ4op3, marketQ5box,\
              marketQ5text1, marketQ5text2, marketQ5op1, marketQ5op2,\
              marketQ5op3, urbanQ1box, urbanQ1text1, urbanQ1text2, urbanQ1op1,\
              urbanQ1op2, urbanQ1op3, urbanQ1op4, urbanQ2box, urbanQ2text1,\
              urbanQ2text2, urbanQ2op1, urbanQ2op2, urbanQ2op3, urbanQ3box,\
              urbanQ3text1, urbanQ3text2, urbanQ3op1, urbanQ3op2, urbanQ3op3,\
              urbanQ4box, urbanQ4text1, urbanQ4text2, urbanQ4op1, urbanQ4op2,\
              urbanQ4op3, favelaQ1box, favelaQ1text1, favelaQ1text2, favelaQ1op1,\
              favelaQ1op2, favelaQ1op3, favelaQ2box, favelaQ2text1, favelaQ2op1,\
              favelaQ2op2, favelaQ2op3, favelaQ2op4, favelaQ3box, favelaQ3text1,\
              favelaQ3text2, favelaQ3op1, favelaQ3op2, favelaQ4box,\
              favelaQ4text1, favelaQ4text2, favelaQ4op1, favelaQ4op2,\
              favelaQ4op3, Qcorrectbox, Qcorrecttext, save_score_button]
    ###diagram of function calls

    #check the stored values for player level and name
    try:
        file=open("save file.txt", "r")
        save=file.read().splitlines()
        file.close()
        file_lvl=save[73]
        file_name=save[74]
        #update the level
        city.set_lvl(int(file_lvl))
        #if the name is the same
        if file_name==city.player_name:
            #get the players name
            interface.get_name(city)
        else:
            #set the players name from file
            city.player_name=file_name
    except FileNotFoundError:
        pass
    
    #display the main menu
    menu.display_main_menu(buttons, city)

    #whether the game has ended or not
    game_end=False
    #loop for the game to run on
    running = True


    #the number of seconds that the loop starts running at
    start_secs=math.floor(time.time())
    #the current time of the game rounded down
    current_secs=math.floor(time.time())
    #the number of seconds that have passed
    secs=0
    new_second=False
    while running:
        #check if a new second has passed
        if math.floor(time.time())>current_secs:
            current_secs=math.floor(time.time())
            new_second=True
            if city.get_playing():
                secs+=1
        #update the timer display
        if secs%60<10:
            mod_time="0"+str(round(secs%60))
        else:
            mod_time=str(round(secs%60))
        time_text=str(secs//60)+":"+mod_time
        buttons[39].change_text(time_text, 18)
        #this is so after the game has ended menus can't be clicked
        #and it gives the game 1 tick open the end screen
        if secs==600 and city.get_playing()==False and city.get_playing_type()=="main":
            interface.remove_highlight()
            city_type=city.get_city_type()
            menu.create_end_screen(buttons, Qbuttons, city_type)
            secs+=1
        #if 600 seconds have passed end the game
        if secs==600 and city.get_playing_type()=="main":
            game_end=True
            city.change_playing(False)
        #if the player is playing a mission
        if city.get_playing_type()=="mission" and city.check_mission_end():
            #restart the game
            start_secs=math.floor(time.time())
            current_secs=math.floor(time.time())
            secs=0
            #save the players name and level
            name=city.player_name
            lvl=city.get_player_lvl()
            city=city_class.City()
            city.player_name=name
            #increment the level
            city.set_lvl(lvl+1)
            #increase the players level
            file_work.update_lvl(city)
            #display the main menu
            menu.display_main_menu(buttons, city)
            #display that the mission has been completed
            interface.popup("You have completed the mission!", "You have leveled up!", "You are now level %s" % city.get_player_lvl())
        gain, people_needed, crime_chance, birth_chance, QOL=city.get_gains()
        if city.get_playing():
            if new_second:
                city.change_money(gain)
        #gets event from event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        interface.clear_popup()
        #if the game hasn't ended check main buttons
        if not game_end:
            for button in buttons:
                #if there is a popup on the screen no buttons can be pressed
                if interface.current_popup_box==[]:
                    button.is_pressed()
                button.change_active()
        #if game has ended check end buttons
        else:
            for button in Qbuttons:
                button.is_pressed()
                button.change_active()
        #if theres a popup on the screen buildings can't be pressed either
        if interface.current_popup_box==[]:
            if city.get_playing():
                for building in city.get_buildings_list():
                    building.is_pressed()
        if not game_end:
            #draw widgets onto screen
            screen.blit(background, (0, 0))
            screen.blit(orange_metal, (440, 0))
        else:
            screen.blit(question_background, (0, 0))
        if city.get_playing():
            #draw buildings to screen
            city.draw_buildings(screen)
            if new_second:
                #counts down until building something
                city.reduce_building_time(buttons, interface)
        #draw the highlight if there is one
        interface.draw_highlight()
        #gives a random chance to execute the crime function
        #the chance is measured in per second
        if city.get_playing():
            if new_second:
                if random.random()<crime_chance:
                    city.crime(interface)
        #the random chance for new people being added
        if city.get_playing():
            if new_second:
                if random.random()<birth_chance:
                    city.increase_population()
        interface.draw_popup()
        #only tries to draw the main buttons if the game hasn't ended
        if not game_end:
            interface.draw_buttons(buttons)
        #only checks to draw the end buttons if the game has ended
        else:
            interface.draw_buttons(Qbuttons)
        #draw all the texts
        interface.draw_text(city, game_end)
        #update the screen and set the max fps
        pygame.display.update()
        clock.tick(10)
        new_second=False
    

if __name__=="__main__":
    main()
