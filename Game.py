import random


class State:

    def __init__(self):
        self.player_hand = 0
        self.dealer_hand = 0    

        self.player_aces = 0
        self.dealer_aces = 0


    def evaluate(self):
        print(f'PLAYER:{self.player_hand}\t DEALER:{self.dealer_hand}')
        
        if self.player_hand == self.dealer_hand: return 'DRAW'        
        return ['WIN','LOSE'][self.player_hand < self.dealer_hand]



class Game:

    def __init__(self):
        #Card:  2 3 4 5 6 7 8 9 10  J  Q  K  A 
        #Points:2 3 4 5 6 7 8 9 10 10 10 10 11
        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]*4
        
        #By default an Ace is worth 11. When a hand exceeds 21, 
        #any aces are reduced to 1 in order to attempt to avoid a bust.

        self.state = State()

        random.shuffle(self.deck)

        self.hit('player')
        self.hit('dealer')
        self.hit('player')
        
        

    def hit(self, who):
        
        card = self.deck.pop()

        if who == 'player':

            #Increment ace count if ace is envountered
            if card == 11: self.state.player_aces += 1

            #Add card to 
            self.state.player_hand += card

            #If the hand is over 21, attempt to reduce aces to avoid a bust.
            if self.state.player_hand > 21:
                
                #Use the least number of aces (if any) in order to avoid a bust.
                while self.state.player_aces != 0:
                    self.state.player_hand -= 10
                    self.state.player_aces -= 1

                    if self.state.player_hand <= 21: return True

            #Otherwise, the hand is valid.
            else: return True

            #The hand was not lowered to 21 or less because 
            #otherwise it would have been returned in the loop.
            return False  

        elif who == 'dealer':
            #Increment ace count if ace is envountered
            if card == 11: self.state.dealer_aces += 1

            #Add card to 
            self.state.dealer_hand += card

            #If the hand is over 21, attempt to reduce aces to avoid a bust.
            if self.state.dealer_hand > 21:
                
                #Use the least number of aces (if any) in order to avoid a bust.
                while self.state.dealer_aces != 0:
                    self.state.dealer_hand -= 10
                    self.state.dealer_aces -= 1

                    if self.state.dealer_hand <= 21: return True

            #Otherwise, the hand is valid.
            else: return True

            #The hand was not lowered to 21 or less because 
            #otherwise it would have been returned in the loop.
            return False

        raise Exception('Invalid Player')


    def getState(self):
        return self.state




        