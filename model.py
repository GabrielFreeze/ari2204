from cmath import exp
from State import State
import random

class Model:
    def __init__(self) -> None:
        self.model = {}
        self.episode = []
        
        #Used during montecarlo
        self.first_pass = True
        
    def get_all(self,s:State):
        return self.model[s]

    def get_value(self, s:State, hit:bool):
        return self.model[s][2+hit]

    def get_count(self, s:State, hit:bool):
        return self.model[s][hit]


    #TODO: WHY THE FUCK ARE THE STATES NOT BEING HASHED CORRECTLY? THE SAME STATE IS GIVING DIFFERENT FUCKING HASHES









    def update_episode(self, win:bool):
        for (s,a) in self.episode:
            key = s
            
            self.model[key][2+a] += (-1) ** (not win)

        #Reset episode
        self.episode.clear() 

    def prepare_next_episode(self):
        self.first_pass = True;



    def update_count(self, s:State, hit:bool) -> None:
        self.episode.append((s,hit))
        
        key = s
        
        if key in self.model:
            #Increment count of taking action from given state.
            self.model[key][hit] += 1
        else:
            #Create a new instance of the state action.
            #Note that initally the value of taking this state-action is 0.
            #(a,b,c,d) a -> Nō of Stands, b -> Nō of Hits, c -> q(s,STAND), d -> q(s,HIT)
            self.model[key] = [[1,0,0,0], [0,1,0,0]][hit]


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
            return self.random_policy();

        #Otherwise, select action randomly with probability ε

        if   ε == '1/k':       P = 1/k
        elif ε == '1/ek1000':  P = exp(-k/1000).real
        elif ε == '1/ek10000': P = exp(-k/10000).real

        #Select action randomly
        if random.random() <= P:
            return self.random_policy();
        
        #Or explore greedily
        else:
            #Find previous records of this state

            if s not in self.model:
                return self.random_policy()


            stand_value = self.model[s][2]/self.model[s][0] if self.model[s][0] != 0 else 0 
            hit_value   = self.model[s][3]/self.model[s][1] if self.model[s][1] != 0 else 0 


            #The action is to Stand.
            if stand_value > hit_value:
                print('.')
                return False 

            #The action is to Hit.
            elif stand_value < hit_value:
                print('.')
                return True 
            
            #Both values are equal, choose randomley.
            else:
                return self.random_policy()




            
    