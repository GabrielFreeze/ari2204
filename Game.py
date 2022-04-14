import random
from copy import deepcopy
from State import State



class Game:

    first_state = True



    def __init__(self):
        #Card:  A 2 3 4 5 6 7 8 9 10  J  Q  K 
        #Points:1 2 3 4 5 6 7 8 9 10 10 10 10
        self.deck = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4
        
        
        #By default an Ace is worth 1. If its possible (sum is 10 or less)
        #..an Ace in the player/dealer's hand can be worth 11. If the sum exceeds
        #21, then the Ace can be demoted back to 1. In any hand, only one Ace can ever be worth 11.
        
        #We won't store this variable in the agent state.
        self.dealer_ace_11 = False

        self.state = State()

        random.shuffle(self.deck)

        self.hit('player')
        self.hit('dealer')
        self.hit('player')
        
    def hit(self, who):
        
        card = self.deck.pop()
        

        if who == 'player':

            #Attempt to represent the Ace as 11.
            if card == 1 and self.state.player_hand < 11:
                self.state.player_hand += 11
                self.state.player_ace_11 = True

            #Take face value. (Ace = 1)
            else:

                self.state.player_hand += card

                #Did the new card make the sum go over 21?
                if self.state.player_hand > 21:

                    #Can we demote an 11-Ace to represent 1 in order to avoid busting?
                    if self.state.player_ace_11:
                        self.state.player_hand -= 10
                        self.state.player_ace_11 = False
                    
                    #If not, then the hand went over 21.
                    else:
                        return False
            
            return True



        if who == 'dealer':

            #Attempt to represent the Ace as 11.
            if card == 1 and self.state.dealer_hand < 11:
                self.state.dealer_hand += 11
                self.dealer_ace_11 = True

            #Take face value. (Ace = 1)
            else:

                self.state.dealer_hand += card

                #Did the new card make the sum go over 21?
                if self.state.dealer_hand > 21:

                    #Can we demote an 11-Ace to represent 1 in order to avoid busting?
                    if self.dealer_ace_11:
                        self.state.dealer_hand -= 10
                        self.dealer_ace_11 = False
                    
                    #If not, then the hand went over 21.
                    else:
                        return False
            
            return True

        raise Exception('Invalid Player')

    def getState(self):
        return deepcopy(self.state)








        