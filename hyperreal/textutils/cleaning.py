import regex as re
from hyperreal.textutils.utils import lemmatize
from unidecode import unidecode
from textsearch import TextSearch


def clean(text, use_lemmas=False, is_post=False):
    """
    Clean text from unnecessary symbols.
    :param text: string containing text to clean
    :param use_lemmas: if True, text returned text will be lemmatized
    :param is_post: if True, text is cleaned assuming it is a post
    :return: string containing cleaned text
    """
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\t", " ", text)

    if not is_post:
        text.strip()
        return text

    text = re.sub(r"http[^\s]+", " ", text)
    text = re.sub(r"images[^\s]+", " ", text)
    text = re.sub(r":D|:p|:P|:d", " ", text)
    text = re.sub(r":\w+:", " ", text)
    text = re.sub(r"[(\[]", "", text)
    text = re.sub(r"[\^_'<>*\]\"?,).:\\/;!@$]", " ", text)
    text = re.sub(r" - ?", " ", text)
    text = re.sub(r" ?- ", " ", text)
    text = re.sub(r"\d+ \d+", " ", text)
    text = re.sub(r" \d+ ", " ", text)
    text = re.sub(r"\w+ pisze", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    text = text.lower()

    if use_lemmas:
        tokens = text.split(' ')
        tokens = [lemmatize(t) for t in tokens]
        text = ' '.join(tokens)

    text = unidecode(text)

    return text


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
