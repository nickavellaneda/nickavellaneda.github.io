'''Project Name: Solitaire
   Names: Ajay Bahl & Nicholas Avellaneda
'''

# Imports

import math
import random

from Tkinter import *
from Canvas import Rectangle, CanvasText, Group, Window


#subclass to fix bug in Group import from Canvas

class Group(Group):
    def bind(self, sequence=None, command=None):
        return self.canvas.tag_bind(self.id, sequence, command)

#properties and layout of the playing cards with offset to create multiple decks

CARDWIDTH = 100
CARDHEIGHT = 150
MARGIN = 10
XSPACING = CARDWIDTH + 2*MARGIN
YSPACING = CARDHEIGHT + 4*MARGIN
OFFSET = 5

#background color of the table which the game is played on 

BACKGROUND = 'Red'

#assign colors to the different cards suits for gameplay

hearts = 'Heart'
diamonds = 'Diamond'
clubs = 'Club'
spades = 'Spade'

red = 'red'
black = 'black'

color = {}
for s in (hearts, diamonds):
    color[s] = red
for s in (clubs, spades):
    color[s] = black

allsuits = color.keys()
nsuits = len(allsuits)

#cards assigned values 1-13 to simplify gameplay of odering card values from greatest to least

ace = 1
jack = 11
queen = 12
king = 13
allvalues = range(1, 14) 
nvalues = len(allvalues)


#list to match card value to the string displayed

valnames = ["", "A"] + map(str, range(2, 11)) + ["J", "Q", "K"]


#number of rows of cards in solitaires

nrows = 7


#class definitions


class Card:
    '''cards are constructed based on sui, value, and color. Decks are made
       and card values are only shown when face up'''
       
    #construct cards based on value and suit and determine position in deck based on stack properties
    def __init__(self, suit, value, canvas):
       
        self.suit = suit
        self.value = value
        self.color = color[suit]
        self.face_shown = 0

        self.x = self.y = 0
        self.group = Group(canvas)

        text = "%s  %s" % (valnames[value], suit)
        self.__text = CanvasText(canvas, CARDWIDTH//2, 0,
                               anchor=N, fill=self.color, text=text)
        self.group.addtag_withtag(self.__text)

        self.__rect = Rectangle(canvas, 0, 0, CARDWIDTH, CARDHEIGHT,
                              outline='black', fill='white')
        self.group.addtag_withtag(self.__rect)

        self.__back = Rectangle(canvas, MARGIN, MARGIN,
                              CARDWIDTH-MARGIN, CARDHEIGHT-MARGIN,
                              outline='black', fill='blue')
        self.group.addtag_withtag(self.__back)
        
        
    #prints card values/suits
    def __repr__(self):
        
        return "Card(%r, %r)" % (self.suit, self.value)
        
        
    #move card to absolution posiiton
    def moveto(self, x, y):
        
        self.moveby(x - self.x, y - self.y)
        
    #move card by offset (dx, dy)
    def moveby(self, dx, dy):
        #move card by offset (dx, dy)
        self.x = self.x + dx
        self.y = self.y + dy
        self.group.move(dx, dy)
        
    #raise card above all obkects on canvas
    def tkraise(self):
        self.group.tkraise()
        
    #cards are faced up
    def showface(self):
        self.tkraise()
        self.__rect.tkraise()
        self.__text.tkraise()
        self.face_shown = 1
        
    #cards are face down
    def showback(self):
        self.tkraise()
        self.__rect.tkraise()
        self.__back.tkraise()
        self.face_shown = 0


class Stack:
    '''class used to develop base for each stack in the game based on card
       values and card movement, with user overridde
    '''
    
    #constructs stacks based on position and game object
    def __init__(self, x, y, game=None):
        self.x = x
        self.y = y
        self.game = game
        self.cards = []
        self.group = Group(self.game.canvas)
        self.group.bind('<1>', self.clickhandler)
        self.group.bind('<Double-1>', self.doubleclickhandler)
        self.group.bind('<B1-Motion>', self.motionhandler)
        self.group.bind('<ButtonRelease-1>', self.releasehandler)
        self.makebottom()

    def makebottom(self):
        pass

    def __repr__(self):
        #return string values of stack
        return "%s(%d, %d)" % (self.__class__.__name__, self.x, self.y)
 
    #add a card to the stack
    def add(self, card):
        self.cards.append(card)
        card.tkraise()
        self.position(card)
        self.group.addtag_withtag(card.group)
             
    #delete a card from the stack
    def delete(self, card):
        self.cards.remove(card)
        card.group.dtag(self.group)
        
    #place top card on deck face up
    def showtop(self):
        if self.cards:
            self.cards[-1].showface()
            
    #delete and return top card
    def deal(self):
        if not self.cards:
            return None
        card = self.cards[-1]
        self.delete(card)
        return card

    # stack class override methods

    def position(self, card):
        card.moveto(self.x, self.y)

    def userclickhandler(self):
        self.showtop()

    def userdoubleclickhandler(self):
        self.userclickhandler()

    def usermovehandler(self, cards):
        for card in cards:
            self.position(card)

    #event handlers

    def clickhandler(self, event):
        #if event is lost
        self.finishmoving()             
        self.userclickhandler()
        self.startmoving(event)

    def motionhandler(self, event):
        self.keepmoving(event)

    def releasehandler(self, event):
        self.keepmoving(event)
        self.finishmoving()

    def doubleclickhandler(self, event):
        #if event is lost
        self.finishmoving()             
        self.userdoubleclickhandler()
        self.startmoving(event)

    #methods in which the cards move on canvas

    moving = None

    def startmoving(self, event):
        self.moving = None
        tags = self.game.canvas.gettags('current')
        for i in range(len(self.cards)):
            card = self.cards[i]
            if card.group.tag in tags:
                break
        else:
            return
        if not card.face_shown:
            return
        self.moving = self.cards[i:]
        self.lastx = event.x
        self.lasty = event.y
        for card in self.moving:
            card.tkraise()

    def keepmoving(self, event):
        if not self.moving:
            return
        dx = event.x - self.lastx
        dy = event.y - self.lasty
        self.lastx = event.x
        self.lasty = event.y
        if dx or dy:
            for card in self.moving:
                card.moveby(dx, dy)

    def finishmoving(self):
        cards = self.moving
        self.moving = None
        if cards:
            self.usermovehandler(cards)


class Deck(Stack):

    #stack deck to allow shuffling
    
    #visual card properties
    def makebottom(self):
        bottom = Rectangle(self.game.canvas,
                           self.x, self.y,
                           self.x+CARDWIDTH, self.y+CARDHEIGHT,
                           outline='black', fill=BACKGROUND)
        self.group.addtag_withtag(bottom)
        
   #create the card
    def fill(self):
        for suit in allsuits:
            for value in allvalues:
                self.add(Card(suit, value, self.game.canvas))

    #shuffle the cards in stack
    def shuffle(self):
        n = len(self.cards)
        newcards = []
        for i in randperm(n):
            newcards.append(self.cards[i])
        self.cards = newcards

   #user can select card ontop of stack to show value (face up)
   #if out of cards moves faceup cards back to deck
    def userclickhandler(self):
        opendeck = self.game.opendeck
        card = self.deal()
        if not card:
            while 1:
                card = opendeck.deal()
                if not card:
                    break
                self.add(card)
                card.showback()
        else:
            self.game.opendeck.add(card)
            card.showface()

#returns random card value in specified range
def randperm(n):
    r = range(n)
    x = []
    while r:
        i = random.choice(r)
        x.append(i)
        r.remove(i)
    return x


class OpenStack(Stack):
    '''On open stack user can move card and place based on value, user will not 
       be able to place card if values are not descending
    '''

    def acceptable(self, cards):
        return 0

    def usermovehandler(self, cards):
        card = cards[0]
        stack = self.game.closeststack(card)
        if not stack or stack is self or not stack.acceptable(cards):
            Stack.usermovehandler(self, cards)
        else:
            for card in cards:
                self.delete(card)
                stack.add(card)
            self.game.wincheck()

    def userdoubleclickhandler(self):
        if not self.cards:
            return
        card = self.cards[-1]
        if not card.face_shown:
            self.userclickhandler()
            return
        for s in self.game.suits:
            if s.acceptable([card]):
                self.delete(card)
                s.add(card)
                self.game.wincheck()
                break


class SuitStack(OpenStack):
    '''On open stack, when user places card, suck and color must be opposite in 
       order for card to be placed or user cannot place card
    '''

    def makebottom(self):
        bottom = Rectangle(self.game.canvas,
                           self.x, self.y,
                           self.x+CARDWIDTH, self.y+CARDHEIGHT,
                           outline='black', fill='')

    def userclickhandler(self):
        pass

    def userdoubleclickhandler(self):
        pass

    def acceptable(self, cards):
        if len(cards) != 1:
            return 0
        card = cards[0]
        if not self.cards:
            return card.value == ace
        topcard = self.cards[-1]
        return card.suit == topcard.suit and card.value == topcard.value + 1


class RowStack(OpenStack):
    '''user can place cards not being used in row on top left of canvas for later
       use or placement
    '''
    def acceptable(self, cards):
        card = cards[0]
        if not self.cards:
            return card.value == king
        topcard = self.cards[-1]
        if not topcard.face_shown:
            return 0
        return card.color != topcard.color and card.value == topcard.value - 1

    def position(self, card):
        y = self.y
        for c in self.cards:
            if c == card:
                break
            if c.face_shown:
                y = y + 2*MARGIN
            else:
                y = y + OFFSET
        card.moveto(self.x, y)


class Solitaire:
    '''user can play the game solitaire based on the rules specified and card 
       properties in the classes above
    '''

    '''Canvas is established for user based on color, and window format with deal
       button in bottom left corner. Random cards are placed in open stacks and deck
       is ready to be played with
    '''
    def __init__(self, master):
        self.master = master

        self.canvas = Canvas(self.master,
                             background=BACKGROUND,
                             highlightthickness=0,
                             width=nrows*XSPACING,
                             height=3*YSPACING + 20 + MARGIN)
        self.canvas.pack(fill=BOTH, expand=TRUE)

        self.dealbutton = Button(self.canvas,
                                 text="Deal",
                                 highlightthickness=0,
                                 background=BACKGROUND,
                                 activebackground="green",
                                 command=self.deal)
        Window(self.canvas, MARGIN, 3*YSPACING + 20,
               window=self.dealbutton, anchor=SW)

        x = MARGIN
        y = MARGIN

        self.deck = Deck(x, y, self)

        x = x + XSPACING
        self.opendeck = OpenStack(x, y, self)

        x = x + XSPACING
        self.suits = []
        for i in range(nsuits):
            x = x + XSPACING
            self.suits.append(SuitStack(x, y, self))

        x = MARGIN
        y = y + YSPACING

        self.rows = []
        for i in range(nrows):
            self.rows.append(RowStack(x, y, self))
            x = x + XSPACING

        self.openstacks = [self.opendeck] + self.suits + self.rows

        self.deck.fill()
        self.deal()

    #check to determine if user won game
    def wincheck(self):
        for s in self.suits:
            if len(s.cards) != nvalues:
                return
        self.win()
        self.deal()
        
    #winning animation
    def win(self):
        
        cards = []
        for s in self.openstacks:
            cards = cards + s.cards
        while cards:
            card = random.choice(cards)
            cards.remove(card)
            self.animatedmoveto(card, self.deck)
            
    #animated motion of cards
    def animatedmoveto(self, card, dest):
        for i in range(10, 0, -1):
            dx, dy = (dest.x-card.x)//i, (dest.y-card.y)//i
            card.moveby(dx, dy)
            self.master.update_idletasks()
            
    #places the card to the stack closest to user input
    def closeststack(self, card):
        closest = None
        cdist = 999999999
        for stack in self.openstacks:
            dist = (stack.x - card.x)**2 + (stack.y - card.y)**2
            if dist < cdist:
                closest = stack
                cdist = dist
        return closest

    #when deal button is pressed the deck reshuffles and resets
    def deal(self):
        self.reset()
        self.deck.shuffle()
        for i in range(nrows):
            for r in self.rows[i:]:
                card = self.deck.deal()
                r.add(card)
        for r in self.rows:
            r.showtop()
    
    #position of card resets if placement does not comply with game rules
    def reset(self):
        for stack in self.openstacks:
            while 1:
                card = stack.deal()
                if not card:
                    break
                self.deck.add(card)
                card.showback()



#main function to run game
def main():
    root = Tk()
    game = Solitaire(root)
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()

if __name__ == '__main__':
    main()