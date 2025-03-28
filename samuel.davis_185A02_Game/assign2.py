"""Imports the CodeWords game so it can be played.
"""
import Classes.CodeWordsGame as cwg

def play_game():
    """Function to run the game. If a game is won or lost asks the user if they'd like to continue
    """
    play_again = 'y'
    while play_again != 'n':
        game = cwg.CodeWordsGame()
        game_over = False
        print(game)
        while not game.is_lost() and not game_over:

            # Make the guess and check the game status
            if game.make_guess():
                game_over = True # Exits the loop if guess ends the game status

            if game.is_lost():
                print("\nYou've lost the game! Better luck next time.")
                print(f"The secret word was: {game._secret_word}")
                game_over = True
        
        # Ask if the player wants to play again
        print(repr(game))
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again == 'n':
            print("\nThank you for playing!")

# Run the game
if __name__ == "__main__":
    play_game()