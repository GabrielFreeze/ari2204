from Game import Game


# e = EnvironmentState()

def main():

    game = Game()
    while True:
        print(f'Your Hand: {game.state.player_hand}')
        print(f'Ace-11:    {game.state.player_ace_11}')
        print('\n')
        print(f'Dealer Hand: {game.state.dealer_hand}')
        
        print('\n')
        x = input('Hit? (Y/N):')
        print('\n')

        if x == 'N': break
        if x != 'Y': raise Exception('?')
        
        if not game.hit('player'):
            print(f'Your Hand: {game.state.player_hand}')
            print(f'Ace-11:    {game.state.player_ace_11}')
            print('You Died')
            return
    
    while game.state.dealer_hand < 17:
        x = game.hit('dealer')

        print(f'Dealer Hand: {game.state.dealer_hand}')
        print('\n')

        if not x:
            print('You Won')
            return
    
    print(game.state.evaluate())




if __name__ == "__main__":
    main()
