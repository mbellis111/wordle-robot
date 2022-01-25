import string

INPUT_DICTIONARY_PATH = "input/words_v5.txt"
ALPHABET = set(string.ascii_letters)
NUM_TOP_WORDS = 10
NUM_GUESSES = 6
WORD_LENGTH = 5


# the JDHoney method to solve
# start with 3 words that maximize different combinition of popular letters
# i.e. stale, dough, briny
# then (assuming not hard mode)
# use words composed of letters from the most popular letters
# that haven't been used to eliminate as many remaining letters
# repeat 1 - 2 times?
# good luck
# cutoffs - how many letters to try to use?
# cutoffs - how many times guessing to eliminate letters (how many words left)

def main():
    print("Starting...")

    # arose trild
    # correct_word = "pygmy"

    # create listing of all allowed words
    allowed_words = create_five_word_dict(INPUT_DICTIONARY_PATH)

    # create mapping of letter to frequency seen
    letter_freq = create_letter_freq(allowed_words)

    # print(letter_freq)
    for w in sorted(letter_freq, key=letter_freq.get, reverse=True):
        print(w, letter_freq[w])

    # copy the potential words to be reduces
    words_left = allowed_words.copy()
    # keep a set of all possible letters that can be used in a given position
    pword = [set([l.lower() for l in ALPHABET]) for _ in range(5)]

    for num_guess in range(1, NUM_GUESSES + 1):
        print()
        print("Guess #{}".format(num_guess))

        # test scoring a word
        sorted_words = sorted(words_left,
                              reverse=True,
                              key=lambda word: score_word(word, letter_freq))

        print("Best Guesses | Words Left: {}".format(len(sorted_words)))
        for word in sorted_words[0:NUM_TOP_WORDS]:
            print(word, ",", score_word(word, letter_freq))

        # guess = sorted_words[0]
        guess, response = get_response()
        if not guess:
            print("Quitting...")
            return
        # response = check_guess(correct_word, guess)
        print("Wordle Response: {}".format(response))

        if response == 'GGGGG':
            print("--------------")
            print("Congrats, you've won!")
            print("--------------")
            return

        # keep track of wordle's response
        pword = reduce_set_by_feedback(guess, pword, response)

        # now filter all words remaining
        words_left = find_words_matching(pword, words_left)
    print("Done!")


def get_response():
    while True:
        print("Enter guess then response, or QUIT to exit.")
        guess = input("Enter Guessed Word: ")
        if guess == 'QUIT':
            return None, None
        if len(guess) != 5 or not set(guess.lower()) < ALPHABET:
            print("Incorrect input.\n")
            continue
        # return guess, None
        wordle_response = input("Enter Wordle Response: ")
        if not(validate_wordle_response(wordle_response)):
            print("Incorrect input.\n")
            continue
        return guess.lower(), wordle_response.upper()
    return None, None


def validate_wordle_response(response):
    if len(response) != 5:
        return False

    for letter in response:
        if letter.upper() not in ['G', 'Y', 'X']:
            return False

    return True


def find_words_matching(pword, words):
    return [word for word in words if word_matches(pword, word)]


def word_matches(pword, word):
    for pos, letter in enumerate(word):
        if letter not in pword[pos]:
            return False
    return True


def reduce_set_by_feedback(guess, pword, feedback):
    # feedback
    # G for correction position
    # Y for correct letter, wrong position
    # X for not used anywhere
    for pos, value in enumerate(feedback):
        letter = guess[pos]
        if value == 'G':
            pword[pos] = {letter}
        elif value == 'Y':
            if letter in pword[pos]:
                pword[pos].remove(letter)
        elif value == 'X':
            # remove from every spot
            for pl in pword:
                if letter in pl:
                    pl.remove(letter)
    return pword


def score_word(word, letter_freq):
    score = 0.0
    for letter in word:
        score += letter_freq[letter]
    # now divide by the number of unique letters to value them less
    score = score / (5 - len(set(word)) + 1)
    return score


def create_letter_freq(allowed_words):
    letter_count = {}
    for word in allowed_words:
        for c in word:
            if c not in letter_count:
                letter_count[c] = 1
            else:
                letter_count[c] = letter_count[c] + 1
    # now go through the each letter
    # create a dict for the ratio of letters to all letters
    total_letters = sum(letter_count.values())
    # print(letter_count)
    letter_ratio = {}
    for key, value in letter_count.items():
        letter_ratio[key] = float(value) / float(total_letters)
    return letter_ratio


def create_five_word_dict(file_path):
    allowed_words = set()
    with open(file_path, 'r') as input_file:
        for line in input_file:
            word = line.strip().lower()
            # if the length is 5 and the word is a subset of the alphabet
            if len(word) == 5 and set(word) < ALPHABET:
                allowed_words.add(word)
    return allowed_words


def check_guess(word, guess):
    response = []
    for x in range(WORD_LENGTH):
        if word[x] == guess[x]:
            response.append('G')
        elif guess[x] in word:
            response.append("Y")
        else:
            response.append('X')
    return "".join(response)


if __name__ == "__main__":
    main()
