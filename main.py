from Game import Game
from Model import Model
from State import State
from time import time

def run_episodes(episode_count, policy, ε='', exploring_starts=False):
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

                    if   policy == 'random':     hit = model.random_policy()
                    elif policy == 'montecarlo': hit = model.montecarlo_policy(current_state, i+1, ε, exploring_starts)
                    elif policy == 'sarsa':      hit = model.sarsa_policy()
                    elif policy == 'qlearning':  hit = model.qlearning()

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
                
            #Update finished episode values.
            outcome = game.state.evaluate()
            
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
        # for m in model.model:
        #     print(m.state.player_hand,m.state.dealer_hand,m.state.player_ace_11)
        # for key,value in model.model.items():
        #     print(key.player_hand,value)
        return (win_counter, lose_counter, draw_counter)
        


def main():
    episode_count = 100_000
    
    win,lose,draw = run_episodes(episode_count=episode_count, policy='random')
    win_rate = (win/episode_count) * 100
    print(f'Random: {win_rate}%')

    win,lose,draw = run_episodes(episode_count=episode_count, policy='montecarlo', ε='1/k', exploring_starts = True)
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 1: {win_rate}%')

    win,lose,draw = run_episodes(episode_count=episode_count, policy='montecarlo', ε='1/k')
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 2: {win_rate}%')

    win,lose,draw = run_episodes(episode_count=episode_count, policy='montecarlo', ε='1/ek1000')
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 3: {win_rate}%')

    win,lose,draw = run_episodes(episode_count=episode_count, policy='montecarlo', ε='1/ek10000')
    win_rate = (win/episode_count) * 100
    print(f'MonteCarlo 4: {win_rate}%')

    
    
    # s1 = State()
    # s1.player_hand = 1
    # s1.dealer_hand = 1
    # s1.player_ace_11 = 1

    # s2 = State()
    # s2.player_hand = 1
    # s2.dealer_hand = 1
    # s2.player_ace_11 = 1

    # x = (s1.player_hand, s1.dealer_hand, s1.player_ace_11)
    # y = (s2.player_hand, s2.dealer_hand, s2.player_ace_11)

    # # print(x,y)
    # print(hash(x),hash(y))






        


    







if __name__ == "__main__":
    main()
