
def get_word_freq(filename, split_char):
    """
    Get the frequencies of words in filename.
    :param filename: string containing the file name
    :param split_char: string containing column separation symbol
    :return: dictionary of type (word: frequency)
    """
    word_freq = {}

    with open(filename, "r") as f:
        lines = f.readline()
        for line in lines:
            word, count = line.split(split_char)
            word_freq[word] = count

    return word_freq

