from State import State

class StateMetric:
    def __init__(self, state:State, stand_count:int, hit_count:int, stand_value:int, hit_value:int) -> None:
        self.state = state
        self.stand_count = stand_count
        self.hit_count = hit_count
        self.stand_value = stand_value
        self.hit_value = hit_value

    
    def increment_count(self, hit:bool):
        if hit:
            self.hit_count += 1
        else:
            self.stand_count += 1
        
        return self

    def update_value(self, hit:bool, win:bool):

        if hit:
            self.hit_value += (-1) ** (not win)
        else:
            self.stand_value += (-1) ** (not win)

        return self

        
