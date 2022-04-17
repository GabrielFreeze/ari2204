class State:

    def __init__(self, player_hand=0, dealer_hand=0, player_ace_11=False):
        self.player_hand = player_hand #[12..20]
        self.dealer_hand = dealer_hand #[2..11]
        self.player_ace_11 = player_ace_11 #[0,1]

        #180 total different combinations



    def evaluate(self):
        if self.player_hand > 21: return 'LOSE'
        if self.dealer_hand > 21: return 'WIN'
        if self.player_hand == self.dealer_hand: return 'DRAW'

        return ['WIN','LOSE'][self.player_hand < self.dealer_hand]



