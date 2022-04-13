from Game import Game
from Model import Model
from State import State

def run_episodes(episode_count, policy, ε='', exploring_starts=False):
        win_counter  = 0
        lose_counter = 0
        draw_counter = 0

        model = Model()

        for i in range(episode_count):
            lost = False

            game = Game()
            
            # print(f'Player Hand: {game.state.player_hand}')

            #PLayer's moves
            while True:

                #The optimal strategy is to always hit 
                #when less than 12 and stand when equal to 21.
                if game.state.player_hand  < 12:
                    #The player cannot lose if sum is less than 12
                    game.hit('player') 
                        
                    
                elif game.state.player_hand == 21:
                    break #Stand
                
                else: #Choose an action based on the policy

                    if   policy == 'random':     hit = model.random_policy()
                    elif policy == 'montecarlo': hit = model.montecarlo_policy(game.getState(), i+1, ε, exploring_starts)
                    elif policy == 'sarsa':      hit = model.sarsa_policy()
                    elif policy == 'qlearning':  hit = model.qlearning()

                    
                    #Keep track of state-action.
                    model.update_count(game.getState(), hit)


                    #If the action was to hit
                    if hit:

                        #If player went over 21
                        if not game.hit('player'):
                            # print(f'Player Hand: {game.state.player_hand}')
                            lost = True
                            
                            break

                    else: 
                        break #Stand
                    

                # print(f'Player Hand: {game.state.player_hand}')

            #If the while loop exited then the (player's) episode is finished.
            #Set the sum to 22 so game.state.evaluate would say the player lost
            if lost: game.state.player_hand = 22
            # print('\n')
            
            #Dealer's moves
            while not lost and game.state.dealer_hand < 17:
                x = game.hit('dealer')

                # print(f'Dealer Hand: {game.state.dealer_hand}')
                # print('\n')

                if not x:
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
        
        print(len(model.model))
        # for key,value in model.model.items():
        #     print(key.player_hand,value)
        return (win_counter, lose_counter, draw_counter)
        


def main():

    episode_count = 500

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

    win,lose,draw = run_episodes(episode_count=episode_count, policy='random')
    win_rate = (win/episode_count) * 100
    print(f'Random: {win_rate}%')
    
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
