class State:

    def __init__(self):
        self.player_hand = 0 #[12..20]
        self.dealer_hand = 0 #[2..11]
        self.player_ace_11 = False #[0,1]

        #180 total different combinations


    def evaluate(self):
        if self.player_hand > 21: return 'LOSE'
        if self.dealer_hand > 21: return 'WIN'
        if self.player_hand == self.dealer_hand: return 'DRAW'

        return ['WIN','LOSE'][self.player_hand < self.dealer_hand]

