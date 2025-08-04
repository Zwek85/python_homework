#hangman-closure

def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())  # store guesses in lowercase

        display_word = ''.join([char if char in guesses else '_' for char in secret_word])
        print("Current word: " + display_word)

        return all(char in guesses for char in secret_word)

    return hangman_closure

# --- main game loop ---

if __name__ == "__main__":
    secret = input("Enter the secret word: ").lower()
    hangman = make_hangman(secret)

    while True:
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabetical letter.")
            continue

        game_won = hangman(guess)

        if game_won:
            print("Yayy! You guessed the word correctly!")
            break
