import pygame
import sys

class Button:
    """button object that can be placed anywhere necessary in menus etc"""

    def __init__(self, rect, command, text):
        #sets the properties of the button
        self._font=pygame.font.SysFont("Rockwell", 18)
        self._font_colour=pygame.Color("black")
        #sets the rectangle
        self.rect=pygame.Rect(rect)
        self.image=pygame.Surface(self.rect.size).convert()
        #set the command for when the button is pressed
        self.function=command
        self._first_active=False
        self._active_time=0
        self._active=False
        #writes the text
        self._text=self._font.render(text,True,self._font_colour)
        self._text_rect=self._text.get_rect(center=self.rect.center)
        #if the button is used as a button, text box or text itself
        self.use="button"

    #will change the value for first active to the one specified
    #if the button is changing to true, then wait 3 ticks before changing it
    def make_active(self, active):
        #makes the button active or inactive meaning it can be clicked on
        #and will be drawn to the screen
        if active==False:
            self._first_active=False
        else:
            #if setting active to True wait 3 ticks first
            self._first_active=active
            self._active_time=3

    #will instantly change the active value for a button (for texts etc)
    def force_active(self, active):
        self._first_active=active
        self.change_active()

    #will count down the active time
    #then change the active value when it reaches 0
    def change_active(self):
        self._active_time-=1
        if self._active_time<=0:
            self._active=self._first_active

    #if the button is being used for something other than to be pressed
    def change_use(self, use):
        self.use=use

    #changes the buttons display text
    def change_text(self, text, size):
        #reinitialise the font
        self._font=pygame.font.SysFont("Rockwell", size)
        self._font_colour=pygame.Color("black")
        self._text=self._font.render(text,True,self._font_colour)
        self._text_rect=self._text.get_rect(center=self.rect.center)

    #changes the buttons function
    def change_function(self, command):
        self.function=command

    #checks if the button has been pressed
    def is_pressed(self):
        #if the button is used as a button
        if self.use=="button":
            #if the button is active
            if self._active:
                #if the mouse if over the button
                if self.is_hovered():
                    click=pygame.mouse.get_pressed()
                    #if the first mouse button has been pressed
                    if click[0]==1:
                        #make the button inactive for 20 ticks
                        self._active_time=20
                        self._active=False
                        #if the button has many effects
                        if type(self.function)==tuple:
                            #trigger every effect
                            for function in self.function:
                                function()
                        else:
                            #trigger effect
                            self.function()
                        #by having the option of only having one effect this
                        #makes the creation on buildings easier and means you
                        #don't need to write it as a list when there is only
                        #one function

    #checks if the button is being hovered over
    def is_hovered(self):
        #if the mouse if hovering over the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    #draw the button with the changing shade if its being hovered over
    def draw(self, screen):
        #if the button is active
        if self._active:
            #if the mouse is hovering over the button
            if self.is_hovered():
                #if the button is used as a button
                if self.use=="button":
                    self.image=pygame.image.load("pictures/pressed button.png")
                #if the button is used as a box
                elif self.use=="box":
                    self.image=pygame.image.load("pictures/button.png")
                #if the button is used as a text
                else:
                    self.image=pygame.image.load("pictures/empty.png")
                    self.image.set_colorkey((255, 255, 255))
            else:
                #if the button is used as a button or box
                if self.use=="button" or self.use=="box":
                    self.image=pygame.image.load("pictures/button.png")
                #if the button is used as a text
                else:
                    self.image=pygame.image.load("pictures/empty.png")
                    self.image.set_colorkey((255, 255, 255))
            self.image=pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))
            #draw the button to the screen
            screen.blit(self.image, self.rect)
            screen.blit(self._text, self._text_rect)

class Button_with_info(Button):
    """inherits from button
will change draw function to show information when hovered over"""

    def __init__(self, rect, command, text, info_text):
        #inherit from button
        super().__init__(rect, command, text)
        self.info_text=info_text

    def draw(self, screen):
        if self._active:
            if self.is_hovered():
                if self.use=="button":
                    self.image=pygame.image.load("pictures/pressed button.png")
                elif self.use=="box":
                    self.image=pygame.image.load("pictures/button.png")
                else:
                    self.image=pygame.image.load("pictures/empty.png")
                    self.image.set_colorkey((255, 255, 255))
                #creates another button to be displayed to the left of the
                #hovered buttton
                info_box=Button((self.rect[0]-(10+9.5*len(self.info_text)), self.rect[1], 9.5*len(self.info_text), 40), print, "")
                info_text=Button((self.rect[0]-(10+9.5*len(self.info_text)), self.rect[1]+5, 9.5*len(self.info_text), 30), print, self.info_text)
                info_box.change_use("box")
                info_text.change_use("text")
                info_box.force_active(True)
                info_text.force_active(True)
                #draw the info button to the screen
                info_box.draw(screen)
                info_text.draw(screen)
            else:
                if self.use=="button" or self.use=="box":
                    self.image=pygame.image.load("pictures/button.png")
                else:
                    self.image=pygame.image.load("pictures/empty.png")
                    self.image.set_colorkey((255, 255, 255))
            self.image=pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))
            #draw the main button to the screen
            screen.blit(self.image, self.rect)
            screen.blit(self._text, self._text_rect)

            

#commands for buttons
def button_quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
