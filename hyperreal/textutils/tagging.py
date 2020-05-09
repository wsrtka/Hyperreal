from random import random

import flair


def tagged_sentences(sentences, drug_names):
    """
    Tags drug names used in sentences.
    :param sentences: list of strings containing text to tag
    :param drug_names: list of strings containing drug names
    :return: list of strings containing tagged sentences, int number of tags added
    """
    tagged = []
    tags_added = 0

    for s in sentences:
        for t in s:
            if t.text.lower().strip() in drug_names:
                t.add_tag('ner', 'drug')
                tags_added += 1
        tagged.append(s)

    return tagged, tags_added


def build_corpus(sents, train_r=0.7, dev_r=0.15):
    tl = int(train_r * len(sents))
    dl = int(dev_r * len(sents))

    s = sents.copy()
    random.shuffle(s)

    train = flair.SentenceDataset(s[:tl])
    dev = flair.SentenceDataset(s[tl:tl+dl])
    test = flair.SentenceDataset(s[tl+dl:])

    return flair.Corpus(train, dev, test)
