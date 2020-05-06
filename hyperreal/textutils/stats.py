from math import log


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


def compute_tf_idf(term, terms_freq, docs_terms, docs_count):
    """
    Compute the product of term frequency and inverse data frequency.
    :param docs_count: int with the number of docs
    :param term: string for which we compute the tf-idf
    :param terms_freq: dictionary (str: int) with term frequencies
    :param docs_terms: dictionary (str: int) with number of documents containing term
    :return: float with the tf-idf
    """
    tf = terms_freq[term]
    #TODO: wzór nie jest prawidłowy?
    idf = log((1 + docs_count) / (1 + docs_terms[term])) + 1
    return tf * idf
