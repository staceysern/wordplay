import re
import string

re_q_without_u = re.compile(r".*(Q[^U]).*|.*Q$")
re_vowels_in_order = re.compile(r"[^AEIOUY]*A[^EIOUY]*E[^IOUY]"
                                "*I[OUY]*O[^UY]*U[^Y]*Y.*")


def words(filename):
    """
    Generator function which yields each line of a file stripped of
    the newline characters.
    """
    for line in open(filename):
        word = line.strip('\r\n')
        yield word


def uu(word):
    """
    Returns a boolean indicating whether the string 'UU' appears in a word.
    """
    return 'UU' in word


def q_but_not_u(word):
    """
    Returns a boolean indicating whether a word contains a 'Q" not immediately
    followed by a 'U'.
    """
    return bool(re_q_without_u.match(word))


def double_letters(word):
    """
    Return a set of letters which appear two times in a row in a word.
    """
    results = set()
    for i in range(len(word)-1):
        if word[i] == word[i+1]:
            results.add(word[i])
    return results


def not_doubled(filename):
    """
    Return a list of letters which do not appear as double letters in any word
    a file.
    """
    alphabet = set(string.ascii_uppercase)

    doubled = reduce(set.union,
                     [double_letters(word) for word in words(filename)])

    return list(alphabet.difference(doubled))


def palindrome(word):
    """
    Return a boolean indicating whether a word is a palindrome.
    """
    for i in range(0, len(word)/2):
        if not word[i] == word[-i-1]:
            return False
    return True


def contains_vowels_in_order(word):
    """
    Return a boolean indicating whether a word contains the letters 'A','E','I'
    'O', 'U' and 'Y' in alphabetical order.
    """
    return bool(re_vowels_in_order.match(word))


def contains_vowels(word):
    """
    Return a boolean indicating whether a word contains the letters 'A','E','I'
    'O', 'U' and 'Y' in any order
    """
    return len(set(word).intersection("AEIOUY")) == 6


def char_frequencies(word):
    """
    Return a dictionary mapping each character in a word to the number of
    occurrences of that character in the word.
    """
    return {c: word.count(c) for c in set(word)}


def most_frequent_letter(word):
    """
    Return a tuple containing the letter which appears most frequently in a
    word and the number of times it appears.
    """
    return max(char_frequencies(word).items(), key=lambda (k, v): v)


def most_appearances(filename):
    """
    Return a tuple of the letter which appears most often in a single word in
    a file, the word, and the number of occurrences in that word.
    """
    most = [(word, most_frequent_letter(word))
            for word in words(filename)]

    word, (letter, occurrences) = max(most,
                                      key=lambda (word, (letter, occurrences)):
                                      occurrences)

    return letter, word, occurrences


def most_frequent_letters(word):
    """
    Return a tuple containing a list of the letter or letters which appear most
    frequently in a word and the number of occurrences.
    """
    frequencies = char_frequencies(word)
    occurrences = max(frequencies.values())
    letters = [k for k, v in frequencies.items() if v == occurrences]
    return letters, occurrences


def most_appearances_by_letter(filename):
    """
    Return a dictionary mapping letter to a tuple of the most times that letter
    is found in a word or words and the list of those words.
    """
    appearances = {c: (0, []) for c in string.ascii_uppercase}

    for word in words(filename):
        letters, occurrences = most_frequent_letters(word)
        for letter in letters:
            if occurrences > appearances[letter][0]:
                appearances[letter] = (occurrences, [word])
            elif occurrences == appearances[letter][0]:
                appearances[letter][1].append(word)
    return appearances


def longest_anagram(filename):
    """
    Return the set of words from a file which are the longest anagrams of
    each other.
    """
    bins = {}

    for word in words(filename):
        letters = ''.join(sorted(word))
        matches = bins.get(letters, [])
        matches.append(word)
        bins[letters] = matches

    anagrams = {k: v for k, v in bins.iteritems() if len(v) > 1}
    longest = max(anagrams.keys(), key=len)
    return anagrams[longest]


def wordplay(filename):
    print "Words containing 'UU':"
    print filter(uu, words(filename))

    print "\nWords containing a 'Q' which is not followed by a 'U':"
    print filter(q_but_not_u, words(filename))

    print "\nLetters which do not appear doubled:"
    print not_doubled(filename)

    print "\nLongest palindrome:",
    print max(filter(palindrome, words(filename)), key=len)

    print "\nWords containing all the vowels and 'Y' in order:"
    print filter(contains_vowels_in_order, words(filename))

    print "\nWords containing all the vowels and 'Y' in any order:"
    print filter(contains_vowels, words(filename))

    letter, word, occurrences = most_appearances(filename)
    print "\nMost appearances: Letter {} appears {} times in word {}".format(
        letter, occurrences, word)

    print "\nLongest anagrams:"
    print longest_anagram(filename)

    print "\nWords in which each letter appears most frequently:"
    appearances = most_appearances_by_letter(filename)
    for letter, (occurrences, wrds) in appearances.items():
        print "{} ({}): {}".format(letter, occurrences, wrds)


if __name__ == "__main__":
    wordplay('sowpods.txt')
