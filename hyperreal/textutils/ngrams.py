from collections import Counter

from hyperreal.textutils.utils import tokenize


def build_ngrams(tokens,  length=1):
    """
    Build ngrams from tokens.
    :param tokens: string to build ngrams from
    :param length: int length of created ngrams
    :return: string list of ngrams in tokens
    """
    assert length > 0, "Length of ngram is negative!"

    ngrams = []

    for ti in range(len(tokens) - length + 1):
        ngram = []
        for i in range(length):
            ngram.append(str(tokens[ti + i]))

        if length == 1:
            ngrams.append(ngram[0])
        else:
            ngrams.append(tuple(ngram))

    return ngrams


def ngram_dict(docs, length=1):
    """
    Create a dictionary with ngrams and their number of occurences within given docs
    :param docs: list of strings containing texts to analise
    :param length: int length of ngrams to create
    :return: dictionary of ngrams and their total number of occurrences and dictionary of ngrams and number of docs in which they occurred
    """
    assert length > 0, "Length of ngram is negative!"

    ngrams = []
    ngrams_df = []

    for doc in docs:
        tokens = list(tokenize(str(doc)))
        ns = build_ngrams(tokens, length)
        nsdf = list(set(ns))
        ngrams.extend(ns)
        ngrams_df.extend(nsdf)

    return dict(Counter(ngrams)), dict(Counter(ngrams_df))


def distinctive_ngrams(ngrams, base_ngrams, metric):
    """
    Find the most distinctive ngrams when comparing them to another ngram dictionary using a specified metric.
    :param ngrams: dictionary of ngrams and their total number of occurences
    :param base_ngrams: dictionary of ngrams and their total number of occurences
    :param metric: function comparing two ngram counts
    :return: list of tuples containing ngram and the result of their comparison
    """
    results = []

    for ngram, count in ngrams.items():
        base_count = base_ngrams[ngram]
        results.append((ngram, metric(count, base_count)))

    return sorted(results, key=lambda x: x[1], reverse=True)
