from Game import Game, State

class Model:
    def __init__(self) -> None:
        self.model = {}
        self.sequence = []    
        
    def get_all(self,s:State):
        return self.model[hash(s)]

    def get_value(self, s:State, hit:bool):
        return self.model[hash(s)][2+hit]

    def get_count(self, s:State, hit:bool):
        return self.model[hash(s)][hit]

    def update_value(self, s:State, hit:bool, new_value:float):        
        key = hash(s)
        self.model[key][2+hit] = new_value

    def update_count(self, s:State, hit:bool) -> None:
        key = hash(s)
        
        if key in self.model:
            #Increment count of taking action from given state.
            self.model[key][hit] += 1 
        else:
            #Create a new instance of the state action.
            #Note that initally the value of taking this state-action is 0.
            #(a,b,c,d) a -> Nō of Stands, b -> Nō of Hits, c -> q(s,STAND), d -> q(s,HIT)
            self.model[key] = [(1,0,0,0), (0,1,0,0)][hit]
    