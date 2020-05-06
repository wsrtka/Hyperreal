
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

