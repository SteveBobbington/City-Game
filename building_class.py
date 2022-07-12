import pygame
import menu

#this will be inherited from by the other buildings
class Building:
    """A generic building"""
    #the cost to build the building
    #this is a class attribute, as it doesn't change depending on the instance
    cost=0

    def __init__(self, Xpos, Ypos, lvl, effect):
        #creates the buildings rectangle
        self._rect=pygame.Rect(Xpos, Ypos, 50, 50)
        self._lvl=lvl
        #the function call when the button is clicked
        self._effect=effect
        #makes the rectangles faster to draw
        self._image=pygame.Surface(self._rect.size).convert()
        self._picture=None
        self._dmg_picture=None
        self._type=None
        #the costs and refunds for upgrading and destorying
        self._upgrade1_cost=0
        self._upgrade2_cost=0
        self._refund1=0
        self._refund2=0
        self._refund3=0
        #whether the building is damaged or not
        self._dmg_status=False

    #getters
    def get_rect(self):
        return self._rect

    def get_lvl(self):
        return self._lvl

    #return the cost of upgrading the building
    def get_upgrade_cost(self):
        if self.get_lvl()==1:
            return self._upgrade1_cost
        elif self.get_lvl()==2:
            return self._upgrade2_cost
        else:
            return None

    #return the money increase from destroying the building
    def get_refund(self):
        if self.get_lvl()==1:
            return self._refund1
        elif self.get_lvl()==2:
            return self._refund2
        elif self.get_lvl()==3:
            return self._refund3

    def get_type(self):
        return self._type

    def get_dmg_status(self):
        return self._dmg_status

    #setters
    def _increase_lvl(self):
        self._lvl+=1

    def change_effect(self, effect):
        self._effect=effect

    def change_dmg(self, dmg):
        self._dmg_status=dmg

    #checks when the building has been clicked
    def is_pressed(self):
        click=pygame.mouse.get_pressed()
        #if the first mouse button has been pressed
        if click[0]==1:
            #and the mouse is in the same place as the building
            if self.get_rect().collidepoint(pygame.mouse.get_pos()):
                #if the building has many effects
                if type(self._effect)==tuple:
                    #trigger every effect
                    for effect in self._effect:
                        effect()
                else:
                    #trigger effect
                    self._effect()
                #by having the option of only having one effect this makes
                #the creation on buildings easier and means you don't need
                #to write it as a list when there is only one function

    #so the building can draw itself and doesn't need the interface to do it
    def draw(self, screen):
        #load in a picture from file
        self._image=pygame.image.load(self._picture)
        #if the building is damaged load a different picture
        if self.get_dmg_status()==True:
            self._image=pygame.image.load(self._dmg_picture)
        #set any pure white to transparent (used for empties)
        self._image.set_colorkey((255, 255, 255))
        self._image=pygame.transform.scale(self._image, (self._rect[2], self._rect[3]))
        screen.blit(self._image, self._rect)

    def upgrade(self, city, interface):
        interface.remove_highlight()
        #if the player can afford it
        if city.get_money()>=self.get_upgrade_cost()-0.5:
            #reduce the players money
            city.change_money(-self.get_upgrade_cost())
            self._increase_lvl()
        else:
            #show a popup if the player can't afford the upgrade
            interface.popup("This costs %s" % self.get_upgrade_cost(), "you only have %s" % round(city.get_money()))

    def destroy(self, city, buttons, interface):
        interface.remove_highlight()
        #add an empty tile in place of the building destroyed
        city.add_building("Empty", self.get_rect()[0], self.get_rect()[1], 0, buttons, interface)
        #add the money back to the player
        city.change_money(self.get_refund())


class Empty(Building):
    """empty land mass"""

    #creates the empty land, with the right picture and type
    def __init__(self, Xpos, Ypos, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, 0, effect)
        self._picture="pictures/empty.png"
        self._type="Empty"

class Building_slot(Building):
    """Building slot for when building is being built"""

    #show the building is being built
    def __init__(self, Xpos, Ypos, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, 0, effect)
        self._picture="pictures/building slot.png"
        self._type="Building_Slot"

class Highlight(Building):
    """Drawn to screen to highlight another building"""

    #creates the highlight at the correct place
    def __init__(self, Xpos, Ypos):
        #inherit from Building
        super().__init__(Xpos, Ypos, 0, print)
        self._picture="pictures/highlight.png"
        self._type="Highlight"

class House(Building):
    """House - adds people"""
    #class attribute, which can be used without instantiating the class
    cost=2000

    #creates the house, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/house.png"
        self._dmg_picture="pictures/house_broken.png"
        self._type="House"
        self._upgrade1_cost=4000
        self._upgrade2_cost=7000
        self._refund1=500
        self._refund2=2000
        self._refund3=5000

class Shop(Building):
    """Shop - produces money"""
    #class attribute, which can be used without instantiating the class
    cost=2000

    #creates the shop, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/shop.png"
        self._dmg_picture="pictures/shop_broken.png"
        self._type="Shop"
        self._upgrade1_cost=4000
        self._upgrade2_cost=6000
        self._refund1=500
        self._refund2=2000
        self._refund3=5000

class School(Building):
    """School - unlocks other buildings"""
    #class attribute, which can be used without instantiating the class
    cost=5000

    #creates the school, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/school.png"
        self._dmg_picture="pictures/school_broken.png"
        self._type="School"
        self._upgrade1_cost=5000
        self._upgrade2_cost=5000
        self._refund1=2000
        self._refund2=4000
        self._refund3=6000

class Hospital(Building):
    """Hospital - increases QOL"""
    #class attribute, which can be used without instantiating the class
    cost=3500

    #creates the hospital, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/hospital.png"
        self._dmg_picture="pictures/hospital_broken.png"
        self._type="Hospital"
        self._upgrade1_cost=5000
        self._upgrade2_cost=7000
        self._refund1=1000
        self._refund2=3000
        self._refund3=6000

class Road(Building):
    """Road - decreases crime rates"""
    #class attribute, which can be used without instantiating the class
    cost=1000

    #creates the road, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/road.png"
        self._dmg_picture="pictures/road_broken.png"
        self._type="Road"
        self._upgrade1_cost=2000
        self._upgrade2_cost=3000
        self._refund1=400
        self._refund2=1000
        self._refund3=2000

class Factory(Building):
    """Factory - produces money"""
    #class attribute, which can be used without instantiating the class
    cost=2000

    #creates the factory, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/factory.png"
        self._dmg_picture="pictures/factory_broken.png"
        self._type="Factory"
        self._upgrade1_cost=4000
        self._upgrade2_cost=6500
        self._refund1=800
        self._refund2=2000
        self._refund3=5000

class Police_station(Building):
    """Police station - reduces crime rates"""
    #class attribute, which can be used without instantiating the class
    cost=3000

    #creates the police station, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/police_station.png"
        self._dmg_picture="pictures/police_station_broken.png"
        self._type="Police_station"
        self._upgrade1_cost=5000
        self._upgrade2_cost=8000
        self._refund1=1000
        self._refund2=3000
        self._refund3=7000

class Bank(Building):
    """Bank - increases all money earned"""
    #class attribute, which can be used without instantiating the class
    cost=4500

    #creates the bank, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/bank.png"
        self._dmg_picture="pictures/bank_broken.png"
        self._type="Bank"
        self._upgrade1_cost=7500
        self._upgrade2_cost=10000
        self._refund1=1500
        self._refund2=5000
        self._refund3=9000

class Power_station(Building):
    """Power station - increases money made by factories"""
    #class attribute, which can be used without instantiating the class
    cost=4000
    
    #creates the power station, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/power_station.png"
        self._dmg_picture="pictures/power_station_broken.png"
        self._type="Power_station"
        self._upgrade1_cost=6000
        self._upgrade2_cost=8500
        self._refund1=1500
        self._refund2=4000
        self._refund3=8000

class Leisure(Building):
    """Leisure - increases QOL"""
    #class attribute, which can be used without instantiating the class
    cost=2500
    
    #creates the entertainment, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/entertainment.png"
        self._dmg_picture="pictures/entertainment_broken.png"
        self._type="Leisure"
        self._upgrade1_cost=4000
        self._upgrade2_cost=6000
        self._refund1=1000
        self._refund2=2500
        self._refund3=5000

class Lab(Building):
    """Lab - decreases technology cost"""
    #class attribute, which can be used without instantiating the class
    cost=8000

    #creates the lab, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/lab.png"
        self._dmg_picture="pictures/lab_broken.png"
        self._type="Lab"
        self._upgrade1_cost=11000
        self._upgrade2_cost=14000
        self._refund1=3000
        self._refund2=7500
        self._refund3=13000

class Church(Building):
    """Church - will be required for some city types, gives money depending on
total people, and decreases crime rates"""
    #class attribute, which can be used without instantiating the class
    cost=5000

    #creates the lab, with the right picture and type
    def __init__(self, Xpos, Ypos, lvl, effect):
        #inherit from Building
        super().__init__(Xpos, Ypos, lvl, effect)
        self._picture="pictures/church.png"
        self._dmg_picture="pictures/church_broken.png"
        self._type="Church"
        self._upgrade1_cost=7000
        self._upgrade2_cost=10000
        self._refund1=2000
        self._refund2=6000
        self._refund3=12000
