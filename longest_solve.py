import string
import time

INPUT_DICTIONARY_PATH = "input/words_v5.txt"
ALPHABET = set(string.ascii_letters)
NUM_TOP_WORDS = 10
WORD_LENGTH = 5
# use for memoization of word scoring
WORD_SCORE = {}


def main():
    print("Starting...")

    start = time.time()

    # create listing of all allowed words
    allowed_words = create_five_word_dict(INPUT_DICTIONARY_PATH)

    # create mapping of letter to frequency seen
    letter_freq = create_letter_freq(allowed_words)

    guess_counts = {}
    for word in allowed_words:
        num_guesses = run_trial(allowed_words, letter_freq, word)
        # if num_guesses >= 9:
        #     print(word)
        #     print(num_guesses)
        #     return
        if num_guesses in guess_counts:
            guess_counts[num_guesses] += 1
        else:
            guess_counts[num_guesses] = 1
    print(guess_counts)
    failed = 0
    for key, value in guess_counts.items():
        if key >= 7:
            failed += value
    total = sum(guess_counts.values())
    success_rate = (1 - (float(failed) / float(total))) * 100

    end = time.time()

    print("Execution Time (seconds):", end - start)
    print("Total Words:", total)
    print("Failed Guesses:", failed)
    print("Success Rate:", success_rate)


def run_trial(all_words, letter_freq, correct_word):

    num_guess = 1
    # copy the potential words to be reduces
    words_left = all_words.copy()
    # keep a set of all possible letters that can be used in a given position
    pword = [set([l.lower() for l in ALPHABET]) for _ in range(5)]
    while True:

        # test scoring a word
        sorted_words = sorted(words_left,
                              reverse=True,
                              key=lambda word: score_word(word, letter_freq))

        # for guesses 1 to 3 use johns method
        # if num_guess == 1:
        #     guess = "stale"
        # elif num_guess == 2:
        #     guess = "dough"
        # elif num_guess == 3:
        #     guess = "briny"
        # else:
        #     guess = sorted_words[0]

        guess = sorted_words[0]
        response = check_guess(correct_word, guess)

        if response == 'GGGGG':
            return num_guess

        # keep track of wordle's response
        pword = reduce_set_by_feedback(guess, pword, response)

        # now filter all words remaining
        words_left = find_words_matching(pword, words_left)
        num_guess += 1


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
    # memoization
    if word in WORD_SCORE:
        return WORD_SCORE[word]
    # calculate score
    score = 0.0
    for letter in word:
        score += letter_freq[letter]
    # now divide by the number of unique letters to value them less
    score = score / (5 - len(set(word)) + 1)
    WORD_SCORE[word] = score
    return score


def create_letter_freq(allowed_words):
    letter_count = {}
    for word in allowed_words:
        for c in word:
            if c not in letter_count:
                letter_count[c] = 1
            else:
                letter_count[c] = letter_count[c] + 1
    # now go through each letter
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
