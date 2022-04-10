from Game import Game
model = {}


def main():

    lost = False

    game = Game()
    print(f'Player Hand: {game.state.player_hand}')

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
            hit = game.policy()
            key = hash(game.getState())
            
            if key in model:
                #Increment count of taking action from given state.
                model[key][hit] += 1 
            else:
                #Create a new instance of the state action.
                #Note that initally the value of taking this state-action is 0.
                #(a,b,c) a -> Nō of Stands, b -> Nō of Hits, c -> q(s,a)
                model[key] = [(1,0,0), (0,1,0)][hit] 




            #If the action was to hit
            if hit:

                #If player went over 21
                if not game.hit('player'):
                    print(f'Player Hand: {game.state.player_hand}')
                    lost = True
                    
                    break

            else: 
                break #Stand
            

        print(f'Player Hand: {game.state.player_hand}')

    #If the while loop exited then the (player's) episode is finished.
    #Set the sum to 22 so game.state.evaluate would say the player lost
    if lost: game.state.player_hand = 22
    print('\n')
    

    #Dealer's moves
    while not lost and game.state.dealer_hand < 17:
        x = game.hit('dealer')

        print(f'Dealer Hand: {game.state.dealer_hand}')
        print('\n')

        if not x:
            break



    print(game.state.evaluate())





if __name__ == "__main__":
    main()
