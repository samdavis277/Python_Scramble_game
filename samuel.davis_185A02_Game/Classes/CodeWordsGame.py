import random
from colorama import Fore, Style

class CodeWordsGame:
    """The class for a game that takes a line from a text file and encoded it
    then has the user guess letters to try and figure out what the game is.
    """
    def __init__(self):
        """Initializes the game with the given attributes
        """
        # Reads lines from file and selects one to encode
        self._secret_word = self.select_word()
        self._coded_word = self.encode_word()
        self._original_coded_word = self._coded_word
        self._guesses = 10
        self._guesses_used = 0
        self._hints_used = 0
        self._max_hints = 3

    def __str__(self):
        """Returns the current encoded word."""
        return f"""\nWelcome to the CodeWords Game!
Coded Word: {self._coded_word}"""

    def __repr__(self):
        """Returns a detailed representation of the game object."""
        return f"{__class__.__name__}({self._secret_word}, {self._original_coded_word}, {self._max_hints}, {self._hints_used})"

    def read_file(self, filename="codewords.txt"):
        """Reads the file and returns a list of strings.

        Args:
            filename (str, optional): The file being read. Defaults to "codewords.txt".

        Returns:
            list: A list of strings where each string is a line from the file
        """
        with open(filename, "r") as file:
            phrases = [line.strip().upper() for line in file.readlines()]
        return phrases

    def select_word(self):
        """Selects a random string from the list of phrases

        Returns:
            str: A randomly selected string from the list of phrases
        """
        phrases = self.read_file()
        return random.choice(phrases)
    
    def extra_shuffle(self, alphabet):
        """Shuffles the the alphabet string until no letter is in the same position or 100 failed shuffles

        Args:
            alphabet (str): the alphabet from A-Z

        Raises:
            ValueError: If after 100 shuffles the alphabet wasnt fully random once it gives an error

        Returns:
            str: The alphabet with no letter in the same position as before
        """
        max_attempts = 100  # Maximum number of attempts to get a valid full shuffle
        attempts = 0
        alphabet_list = list(alphabet)
        while attempts < max_attempts:
            alphabet = alphabet_list[:]
            random.shuffle(alphabet)
            # Check if no letter is in its original position
            shuffled = True
            for i in range(len(alphabet)):
                # If any letter in the original alphabet is in the same position as the shuffled one set shuffled to false and reshuffle
                if alphabet[i] == alphabet_list[i]:
                    shuffled = False
            if shuffled:
                return ''.join(alphabet)  # Return the fully shuffled alphabet
            attempts += 1

        # If a full shuffle was not found within max_attempts, raise an error
        raise ValueError("Failed to generate a deranged shuffle after several attempts.")

    def encode_word(self):
        """Encodes the secret word by substituting each letter with one from the shuffled alphabet

        Returns:
            str: The encoded word where each letter is different than the secret word
        """
        alphabet = 'abcdefghijklmnopqrstuvwxyz'.upper()
        deranged_alphabet = self.extra_shuffle(alphabet)
        # Creates a dictionary mapping a letter from the original alphabet to one from the shuffled alphabet to give each letter a new value
        letter_dict = {alphabet[i]: deranged_alphabet[i] for i in range(len(alphabet))}
        shuffled_word = [] # list to store the character of the encoded word that will be made a string
        # Loop through each letter in the secret word to apply the encoding
        for letter in self._secret_word:
            if letter == ' ': # If the character is a space add it to the encoded word without change
                shuffled_word.append(' ')
            # If the letter is alphabetic substitute it using the letter_dict mapping (search the dictionary for the letter in the secret word as the key then use the value to encode it)
            elif letter.isalpha():
                shuffled_word.append(letter_dict[letter.upper()])
            else:
                shuffled_word.append(letter) # If not a letter add it to the encoded word normally
        return "".join(shuffled_word) # Join the list of encoded letters as a single string

    def hints(self):
        """Provides a hint by revealing all instances of a letter in the encoded word.
        Returns:
            bool: True if a hint was successfully revealed False if the player has used all their hints 
        """
        if self._hints_used >= self._max_hints:
            print("\nYou've used all your hints!")
            return False
        
        print(f"Hint {self._hints_used + 1}/{self._max_hints}")
        
        # Find the first letter in the secret word that is still hidden in the coded word
        revealed_any = False
        coded_word_list = list(self._coded_word)

        # Iterate through the secret word to find a letter to reveal
        for i in range(len(self._secret_word)):
            if coded_word_list[i] != self._secret_word[i]:
                # Reveal all occurrences of this letter
                for j in range(len(self._secret_word)):
                    # If the letter at index j is the same letter as i then update the coded word to be that letter
                    # It will loop through until j has been every letter in the word and has been compared with i
                    if self._secret_word[j] == self._secret_word[i]:
                        coded_word_list[j] = self._secret_word[j]
                self._coded_word = ''.join(coded_word_list)
                self._hints_used += 1
                revealed_any = True
                if revealed_any:
                    return revealed_any

        # If no letters were revealed, return False
        return revealed_any

    def make_guess(self):
        """Asks the user for a letter substitution or a hint and will continue to ask until a valid one is given.

        Returns:
            bool: True if the game is won, False otherwise
        """
        game_won = False
        valid_guess = True

        # Checks to see if the player has used all their guesses
        if self._guesses_used >= self._guesses:
            print("\nYou've used all your guesses!")
            valid_guess = False
        else:
            print(f"\nGuesses: {self._guesses_used + 1}/{self._guesses}")
            print(f"Coded Word: {self.display_coded_word()}")  # Display the coded word with colours
        
            # Get user input for the guess or hint request
            user_input = input("Enter a letter to guess or '?' for a hint: ").upper().strip()

            if user_input == '?':
                # Provide a hint if user entered '?'
                if not self.hints():
                    print("Unable to provide a hint.")
                    valid_guess = False
            # If the user guess is not a valid letter mark the guess as invalid
            elif len(user_input) != 1 or not user_input.isalpha():
                valid_guess = False
            else:
                letter = user_input
                substitute = input(f"Enter the letter to substitue '{letter}' with: ").upper().strip()
                # If the user does not input a letter from A-Z to substitue mark it as invalid
                if len(substitute) != 1 or not substitute.isalpha():
                    valid_guess = False
                # If the user enters a letter to replace that isnt in the codded word tells them and marks it as invalid
                elif letter not in self._coded_word:
                    print(f"Letter '{letter}' not found in the coded word")
                    valid_guess = False
                else:
                    # If the guess is valid create a new coded word and makes it a list
                    new_coded_word = list(self._coded_word)
                    # Iterates through the coded word and replaces the guessed letter with the substitution
                    for i in range(len(self._coded_word)):
                        if new_coded_word[i] == letter and new_coded_word[i] != self._secret_word[i]:
                            new_coded_word[i] = substitute
                    # Updates coded word with the new substitutions
                    self._coded_word = ''.join(new_coded_word)
                    self._guesses_used += 1

            if valid_guess and self.is_won():
                print(f"\nCongratulations! You've decoded the word: {self._secret_word}.")
                game_won = True
            
            if not valid_guess:
                print("Please make a valid guess of one letter from A-Z or request a hint using ?.")
        return game_won
    
    def display_coded_word(self):
        """Display the coded word with correctly guessed letters in green.
        
        Returns:
            str: A string representation of the coded word with correct guesses in green
        """
        displayed_word = ""
        # Iterate through each character in the coded word
        for i in range(len(self._coded_word)):
            if self._coded_word[i] == self._secret_word[i]:
                # If the letter is correct (matches position in secret word) display it in green
                displayed_word += Fore.GREEN + self._coded_word[i] + Style.RESET_ALL
            else:
                # Otherwise display it as is (no colour)
                displayed_word += self._coded_word[i]
        return displayed_word
    
    def is_won(self):
        """Returns True if the game is won (coded word matches secret word).
        
        Returns:
            bool: True if the codded word matches the secret word False otherwise
        """
        return self._coded_word == self._secret_word

    def is_lost(self):
        """Returns True if the game is lost (no more guesses allowed).
        
        Returns:
            bool: True if the number of guesses used is greater than or equal to the maximum guesses, False otherwise
        """
        return self._guesses_used >= self._guesses

