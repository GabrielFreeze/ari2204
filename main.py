from Game import Game
from Model import Model
from State import State
from time import time

def run_episodes_montecarlo(episode_count, ε='', exploring_starts=False):
        start = time()
        
        win_counter  = 0
        lose_counter = 0
        draw_counter = 0

        model = Model()
       

        for i in range(episode_count):
            lost = False

            game = Game()
            
            #Player's moves
            while True:

                #The optimal strategy is to always hit 
                #when less than 12 and stand when equal to 21.
                if game.state.player_hand  < 12:
                    #The player cannot lose if sum is less than 12
                    game.hit('player') 
                        
                    
                elif game.state.player_hand == 21:
                    break #Stand
                
                else: #Choose an action based on the policy
                    
                    current_state = game.getState()

                    hit = model.montecarlo_policy(current_state, i+1, ε, exploring_starts)

                    #Keep track of state-action.
                    model.increment_count(current_state, hit)

                    #If the action was to hit
                    if hit:

                        #If player went over 21
                        if not game.hit('player'):
                            lost = True
                            break

                    else: 
                        break #Stand
                    

            #If the while loop exited then the (player's) episode is finished.

            #If the player lost, set the sum to 22 so game.state.evaluate would return LOST.
            if lost: game.state.player_hand = 22
            
            #Dealer's moves
            while not lost and game.state.dealer_hand < 17:

                if not game.hit('dealer'):
                    break             
                
            outcome = game.state.evaluate()
            
            #Update finished episode values if in montecarlo.

            if outcome == 'WIN':
                model.update_episode(win=True)
                win_counter += 1
            
            elif outcome == 'LOSE':
                model.update_episode(win=False)
                lose_counter += 1
            
            else:
                draw_counter += 1

            model.prepare_next_episode()
        
        print(f'Time: {round(time()-start,2)}s')

        return (win_counter, lose_counter, draw_counter)

def run_episodes_random(episode_count):
        start = time()
        
        win_counter  = 0
        lose_counter = 0
        draw_counter = 0

        model = Model()
       

        for i in range(episode_count):
            lost = False

            game = Game()
            
            #Player's moves
            while True:

                #The optimal strategy is to always hit 
                #when less than 12 and stand when equal to 21.
                if game.state.player_hand  < 12:
                    #The player cannot lose if sum is less than 12
                    game.hit('player') 
                        
                    
                elif game.state.player_hand == 21:
                    break #Stand
                
                else: #Choose an action based on the policy
                    
                    current_state = game.getState()

                    hit = model.random_policy()

                    #Keep track of state-action.
                    model.increment_count(current_state, hit)

                    #If the action was to hit
                    if hit:

                        #If player went over 21
                        if not game.hit('player'):
                            lost = True
                            break

                    else: 
                        break #Stand
                    

            #If the while loop exited then the (player's) episode is finished.

            #If the player lost, set the sum to 22 so game.state.evaluate would return LOST.
            if lost: game.state.player_hand = 22
            
            #Dealer's moves
            while not lost and game.state.dealer_hand < 17:

                if not game.hit('dealer'):
                    break             
                
            outcome = game.state.evaluate()
            
            #Update finished episode values if in montecarlo.

            if outcome == 'WIN':
                model.update_episode(win=True)
                win_counter += 1
            
            elif outcome == 'LOSE':
                model.update_episode(win=False)
                lose_counter += 1
            
            else:
                draw_counter += 1


            model.prepare_next_episode()
        
        print(f'Time: {round(time()-start,2)}s')

        return (win_counter, lose_counter, draw_counter)

def run_episodes_sarsa(episode_count, ε=''):
    start = time()
        
    win_counter  = 0
    lose_counter = 0
    draw_counter = 0

    model = Model()
    

    for i in range(episode_count):
        lost = False

        game = Game()
        
        #Player's moves
        while True:

            #The optimal strategy is to always hit 
            #when less than 12 and stand when equal to 21.
            if game.state.player_hand < 12: game.hit('player') 
            
            elif game.state.player_hand == 21: break #Stand
            
            else: #Choose an action based on the policy
                
                current_state = game.getState()

                #Choose action with best value.
                hit = model.montecarlo_policy(current_state, i+1, ε)

                #Keep track of state-action.
                model.increment_count(current_state, hit)

                #If the action was to hit
                if hit:
                    if not game.hit('player'): #Player went over 21
                        lost = True
                        break
                else: break # Stand
                    
                #Update the previous state using the current one
                if model.previous_state_action is not None:
                    
                    previous_state = model.previous_state_action[0]
                    previous_hit = model.previous_state_action[0]

                    #The reward will always be 0 as the current_state is not terminal.
                    R = 0

                    #We know that the previous state_action is seen.
                    previous_index = model.seen(previous_state)
                    previous_q_sa = model.model[previous_index].hit_value if previous_hit else model.model[previous_index].stand_value

                    previous_hit_count   = model.model[previous_index].hit_count
                    previous_stand_count = model.model[previous_index].stand_count

                    current_index = model.seen(current_state)
                    current_q_sa = model.model[current_index].hit_value if hit else model.model[current_index].stand_value

                    if previous_hit: model.model[previous_index].hit_value   += (R + current_q_sa - previous_q_sa)/(1+previous_hit_count)    
                    else:            model.model[previous_index].stand_value += (R + current_q_sa - previous_q_sa)/(1+previous_stand_count)

                    
                #Update previous state_action.
                model.previous_state_action = (current_state,hit)
                

        #If the while loop exited then the (player's) episode is finished.

        #If the player lost, set the sum to 22 so game.state.evaluate would return LOST.
        if lost: game.state.player_hand = 22
        
        #Dealer's moves.
        while not lost and game.state.dealer_hand < 17:
            if not game.hit('dealer'): break   

            
        #Evaluate outcome.
        outcome = game.state.evaluate()

        #Update previous state-action value using the current state-action and outcome.
        if model.previous_state_action is not None:
            if lost: R = -1
            elif outcome == 'WIN': R = +1
            else: R = 0

            #Previous state-action
            previous_state = model.previous_state_action[0]
            previous_hit = model.previous_state_action[0]

            #We know that the previous state_action is seen.
            previous_index = model.seen(previous_state)
            previous_q_sa = model.model[previous_index].hit_value if previous_hit else model.model[previous_index].stand_value

            previous_hit_count   = model.model[previous_index].hit_count
            previous_stand_count = model.model[previous_index].stand_count

            current_index = model.seen(current_state)
            current_q_sa = model.model[current_index].hit_value if hit else model.model[current_index].stand_value

            if previous_hit: model.model[previous_index].hit_value   += (R + current_q_sa - previous_q_sa)/(1+previous_hit_count)    
            else:            model.model[previous_index].stand_value += (R + current_q_sa - previous_q_sa)/(1+previous_stand_count)



        if outcome == 'WIN':
                model.update_episode(win=True)
                win_counter += 1
            
        elif outcome == 'LOSE':
            model.update_episode(win=False)
            lose_counter += 1
        
        else:
            draw_counter += 1    


    print(f'Time: {round(time()-start,2)}s')



    return (win_counter, lose_counter, draw_counter)

def main():
    episode_count = 100_000

    win,lose,draw = run_episodes_random(episode_count=episode_count)
    win_rate = (win/episode_count) * 100
    print(f'Random: {round(win_rate,2)}%')

    win,lose,draw = run_episodes_montecarlo(episode_count=episode_count, ε='1/k', exploring_starts = True)
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 1: {round(win_rate,2)}%')

    win,lose,draw = run_episodes_montecarlo(episode_count=episode_count, ε='1/k')
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 2: {round(win_rate,2)}%')

    win,lose,draw = run_episodes_montecarlo(episode_count=episode_count, ε='1/ek1000')
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 3: {round(win_rate,2)}%')

    win,lose,draw = run_episodes_montecarlo(episode_count=episode_count, ε='1/ek10000')
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 4: {round(win_rate,2)}%')
    
    win,lose,draw = run_episodes_sarsa(episode_count=episode_count, ε='0.1')
    win_rate = (win/episode_count) * 100
    print(f'SARSA 1: {round(win_rate,2)}%')

    win,lose,draw = run_episodes_sarsa(episode_count=episode_count, ε='1/k')
    win_rate = (win/episode_count) * 100
    print(f'SARSA 2: {round(win_rate,2)}%')

    win,lose,draw = run_episodes_sarsa(episode_count=episode_count, ε='1/ek1000')
    win_rate = (win/episode_count) * 100
    print(f'SARSA 3: {round(win_rate,2)}%')

    win,lose,draw = run_episodes_sarsa(episode_count=episode_count, ε='1/ek10000')
    win_rate = (win/episode_count) * 100
    print(f'SARSA 4: {round(win_rate,2)}%')




        


    







if __name__ == "__main__":
    main()
