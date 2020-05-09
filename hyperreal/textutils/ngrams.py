import re
from collections import Counter

from hyperreal.textutils.stats import get_tf_idf
from hyperreal.textutils.utils import tokenize, search, term_filter


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


def ngrams_describing_drug(drug_names, posts, doc_freq, sp_tokens=None, filter_numeric=False, length=1, top=10, metric="tfidf"):
    """
    Get ngrams that are most associated with given drugs.
    :param drug_names: list of strings containing drug names (i.e. drug name and it's alternatives)
    :param posts: list of strings to search for drug names
    :param doc_freq: dictionary containing ngrams and the number of docs in which they appeared
    :param sp_tokens: list of strings with forbidden words, leave None to not apply forbidden_filter
    :param filter_numeric: boolean, True if numbers are to be filtered from ngrams
    :param length: int length of created ngrams
    :param top: int number of top matches to return
    :param metric: string name of metric to use when scoring ngrams
    :return: list of tuples with ngrams and their score
    """
    def forbidden_filter(forbidden):
        def t_filter(term):
            return term_filter(term, lambda t: t not in forbidden)

        return t_filter

    def number_filter():
        def t_filter(term):
            return term_filter(term, lambda t: not re.search(r"\d", t))

        return t_filter

    assert length > 0, "Length is negative!"
    assert metric in ["tfidf", "tf"], "Metric should have one of these values: tfidf, tf"

    posts_about_drug = search(drug_names, posts)
    drug_ngrams = ngram_dict(posts_about_drug, length)

    results = []

    for term in drug_ngrams:
        filters = [
            forbidden_filter(sp_tokens) if sp_tokens is not None else None,
            number_filter() if filter_numeric else None,
        ]

        if all([f(term) for f in filters if f is not None]):
            if metric == "tfidf":
                score = get_tf_idf(term, drug_ngrams, doc_freq, len(posts))
            elif metric == "tf":
                score = drug_ngrams[term]

            results.append((term, score))

    top_results = sorted(results, key=lambda x: x[1], reverse=True)
    return top_results[:top]
