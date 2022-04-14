from cmath import exp
from State import State
from StateMetric import StateMetric
import random

class Model:
    def __init__(self) -> None:
        self.model = []
        self.episode = []
    
        #Used during montecarlo
        self.first_pass = True

    def update_episode(self, win:bool):

        for (_,a,index) in self.episode:
            self.model[index].update_value(a,win)
            
        #Reset episode
        self.episode.clear() 

    def prepare_next_episode(self):
        self.first_pass = True

    def seen(self, s1:State):
        # print('Matching state',s1.player_hand)
        for i,item in enumerate(self.model):
            s2 = item.state

            if  s1.player_hand   == s2.player_hand and \
                s1.dealer_hand   == s2.dealer_hand and \
                s1.player_ace_11 == s2.player_ace_11:
                return i

        return -1

    def increment_count(self, s:State, hit:bool) -> None:      

        index = self.seen(s)

        if index != -1:
            self.model[index].increment_count(hit)
        else:
            index = len(self.episode)
            self.model.append(StateMetric(s,0,0,0,0).increment_count(hit))
        
        #Keep reference to position in model for O(1) look-up time.
        self.episode.append((s,hit,index))


    def random_policy(self):
        #True  -> Hit
        #False -> Stand
        return bool(random.randint(0,1))

    def montecarlo_policy(self, s, k, ε, exploring_starts = False):
        
        if exploring_starts and ε != '1/k':
            raise Exception('Invalid Parameters in montecarlo_policy')

        if not exploring_starts and ε != '1/k' and ε != '1/ek1000' and ε != '1/ek10000':
            raise Exception('Invalid Parameters in montecarlo_policy')


        #Due to the nature of the game, the underlying blackjack MDP can never have cycles,
        #since the only time your hand value decreases, the boolean player_ace_11 is switched on.


        #If exploring_starts is True, then always take a random action in the first state.
        if exploring_starts and self.first_pass:
            self.first_pass = False
            return self.random_policy()

        #Otherwise, select action randomly with probability ε

        if   ε == '1/k':       P = 1/k
        elif ε == '1/ek1000':  P = exp(-k/1000).real
        elif ε == '1/ek10000': P = exp(-k/10000).real

        #Select action randomly
        x = random.random() 
        if x <= P:
            return self.random_policy()
        
        #Or explore greedily
        else:
            
            #If state is new pick a radom action.
            index = self.seen(s)
            if index == -1:
                return self.random_policy()

            #Otherwise choose the action with the best mean reward.
            stand_count = self.model[index].stand_count
            hit_count = self.model[index].hit_count
            stand_value = self.model[index].stand_value
            hit_value = self.model[index].hit_value

            mean_stand_value = stand_value/stand_count if stand_count != 0 else 0
            mean_hit_value   = hit_value/hit_count     if hit_count   != 0 else 0
          
            #The action is to Stand.
            if mean_stand_value > mean_hit_value:
                return False 

            #The action is to Hit.
            elif mean_stand_value < mean_hit_value:
                return True 
            
            #Both values are equal, choose randomley.
            else:
                return self.random_policy()




            
    