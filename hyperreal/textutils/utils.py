from _collections import namedtuple
import re
from gensim import utils
import nlp as nlp
from termcolor import colored
from textsearch import TextSearch
from hyperreal.textutils.cleaning import clean

def tokenize(text):
    """
    Split text into tokens.
    :param text: string text to split
    :return: list of strings created by splitting text by empty spaces
    """
    return text.split(" ")

def lemmatize(token, lemma_dict):
    """
    Get or create a lemma for the given token.
    :param token: string containing token to lemmatize
    :param lemma_dict: current lemma dictionary of type (word: lemma)
    :return:
    """
    lemma = lemma_dict.get(token)
    return token if lemma is None else lemma


def get_lemma_dict(filename, split_char):
    """
    Get lemma dict from given file.
    :param filename: string containing file name
    :param split_char: string containing column separation symbol
    :return: dictionary of type (word: lemma)
    """
    lemma_dict = {}

    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            lemma, word, _ = line.split(split_char)

            if not lemma_dict.get(word):
                lemma_dict[word] = lemma
            else:
                current_lemma = lemma_dict[word]
                #TODO: is the following legal? Coulnd't find anything in docs
                current_count = lemma_dict.get(current_lemma)
                other_count = lemma_dict.get(lemma)

                if not current_count or (other_count and other_count > current_count):
                    lemma_dict[word] = lemma

    return lemma_dict


def get_narkopedia_map(narkopedia):
    """
    Read data from narkopedia and create a dictionary with drug names and alternative names.
    :param narkopedia: dataframe containing narkopedia data, must include "other-forms", "generic-names" and "other-names" columns
    :return: dictionary containing drug names and respective alternative names
    """
    def names(cell):
        val = str(cell)

        if val == "[]":
            return []

        val = val[1:-1]
        val = val.split(", ")
        val = [v.replace("'", "").strip().lower() for v in val]

        return val

    results = {}

    for _, row in narkopedia.iterrows():
        other = list(
            set(
                names(row["other-forms"])
                + names(row["generic-names"])
                + names(row["other-names"])
            )
        )
        results[row["name"].lower()] = other

    return results


WordInContext = namedtuple("WordInContext", ["left_context", "word", "right_context"])


def word_in_context(word_index, text, width):
    """
    Create a tuple with a word's context.
    :param word_index: int index of word in text
    :param text: list of strings in which to search for context
    :param width: int radius of context
    :return: WordInContext tuple with left, right contexts and the word
    """
    left_context = [text[j] for j in range(word_index - width, word_index) if j > 0]
    right_context = [text[j] for j in range(word_index + 1, word_index + width + 1) if j < len(text)]
    return WordInContext(left_context, text[word_index], right_context)


def get_keywords_contexts(text, width, keywords, lemma_dict):
    """
    Get contexts of key words.
    :param lemma_dict: current lemma dictionary of type (word: lemma)
    :param text: string containing the text to analise
    :param width: int radius of context
    :param keywords: list of strings containing keywords for which we need contexts
    :return: list of WordInContext tuple
    """
    words_in_context = []
    tokens = text.split(" ")
    tokens = [lemmatize(token, lemma_dict) for token in tokens]

    word_index = 0

    while word_index < len(tokens):
        if tokens[word_index] in keywords:
            words_in_context.append(word_in_context(word_index, tokens, width))
        word_index += 1

    return words_in_context


def compare_context(a, b):
    """
    Compare contexts of two WordInContext tuples
    :param a: WordInContext tuple
    :param b: WordInContext tuple
    :return: True if contexts match
    """
    return set(a.left_context) == set(b.left_context) and set(a.right_context) == set(b.right_context)


def words_matching_context(text, contexts, width, lemma_dict):
    """
    Find words which match given contexts.
    :param text: string containing text to analise
    :param contexts: list of WordInContext tuples to compare contexts to, must be same width as width param
    :param width: int width of contexts
    :param lemma_dict: current lemma dictionary of type (word: lemma)
    :return: list of strings containing words which match any of the given contexts
    """
    words = []
    tokens = text.split(" ")
    tokens = [lemmatize(token, lemma_dict) for token in tokens]

    for i in range(len(tokens)):
        wic = word_in_context(i, tokens, width)

        for ctx in contexts:
            if compare_context(wic, ctx):
                words.append(wic.word)

    return words


def get_new_names(texts, contexts, keywords, width, lemma_dict):
    """
    Get a list of new potential names for keywords (i.e. drug names for drugs).
    :param texts: list of string lists containing texts to analise
    :param contexts: list of WordInContext tuples to compare contexts to, must be same width as width param
    :param keywords: list of strings containing words we are looking for alternatives for
    :param width: int width of contexts
    :param lemma_dict: current lemma dictionary of type (word: lemma)
    :return:
    """
    new_keywords = []

    for text in texts:
        for word in words_matching_context(text, contexts, width, lemma_dict):
            if word not in keywords:
                new_keywords.append(word)

    return new_keywords


def clear_tags(text):
    """
    Clear text of tags created by crawler.
    :param text: string containing text to clear of rags
    :return: string of cleared text
    """
    def find_tags(t):
        """Find the tags created by the crawler (?) and return MatchObject of matches."""
        return re.search(r'\{:tag\s*.*\s*:content\s*\[\s*"?(.*)?"?\s*\]\s*.*\s*\}', t, re.M)

    s = find_tags(text)

    while s is not None and len(s.groups()) > 0:
        text = text.replace(s.group(0), s.group(1))
        s = find_tags(text)

    return text


# TODO: ta funkcja może się przydać w innej formie
def find_phrase(phrase, df, column="content", limit=None):
    """
    Print the text with highlighted phrase occurrences.
    :param column: the column containing texts to analise
    :param phrase: string with phrase to highlight
    :param df: dataframe containing texts in which to search for phrase occurrences
    :param limit: int number limiting the amount of posts to analise
    :return: print the text with highlighted phrase
    """
    results = df[df[column].str.contains(phrase)][column].values
    i = 0

    for r in results:

        if limit is not None and i >= limit:
            return

        i += 1
        r = clear_tags(r)
        words = r.split(' ')
        print(' '.join([colored(w, on_color='on_green') if phrase in w else w for w in words]))
        print('\n----------------------\n')


def get_other_form_dict(drugs):
    """
    Get a dictionary with other names for a drug and alternative forms of the drug name.
    :param drugs: dataframe containing drug data (narkopedia)
    :return: dictionary (string: {string, string}) of drug name and alternative name forms and names
    """
    results = {}

    for row in drugs.iterrows():
        results[row[1]['name']] = {
            'other-forms': row[1]['other-forms'],
            'other-names': row[1]['other-names']
        }

    return results


def search(query, docs):
    """
    Find docs containing matching query.
    :param query: list of strings a doc has to contain to be returned
    :param docs: list of strings (docs) to be searched
    :return: list containing docs with query
    """
    ts = TextSearch(case="ignore", returns="match")
    ts.add(query)

    results = []

    for doc in docs:
        if ts.contains(doc):
            results.append(doc)

    return results


def find_drug_forums(forums, drugs_name):
    """
    Find forums with names containing names of drugs.
    :param drugs_name: list of strings containing drugs name
    :param forums: dataframe with forum data, including forum names
    :return: dataframe of forum infos with looked-for names
    """
    predicate = forums['name'].str.lower().str.contains(drugs_name[0])

    for d in drugs_name[1:]:
        predicate = (predicate | forums['name'].str.lower().str.contains(d[:3]))

    return forums[predicate]


def get_sentences(posts, content_col="content"):
    """
    Get sentences from posts.
    :param posts: dataframe with posts data
    :param content_col: string containing content column name
    :return: array of strings containing sentences
    """
    sents = []
    for content in posts[content_col].values:
        doc = nlp(clean(content))

        for s in doc.sents:
            if len(s) > 2:
                sentence = s.text.strip()
                sents.append(utils.simple_preprocess(sentence))

    return sents


def term_filter(terms, predicate):
    """
    Checks if given terms are valid using predicate.
    :param terms: list of string terms to check
    :param predicate: function representing condition a term has to fulfill in order to be valid
    :return: True if all of the terms fulfill condition
    """
    return [t for t in terms if not predicate(t)] == []
