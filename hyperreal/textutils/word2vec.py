from queue import Queue
from gensim import models
from regex import regex


def load_model_from_file(filename):
    """
    Load a word2vec model from file
    :param filename: string containing file name with model
    :return: model of keyed vectors
    """
    return models.KeyedVectors.load_word2vec_format(filename)


def finetuned_model(model, sentences, vector_file, save_format, save_file, size=300, min_count=1):
    """
    Creates a drug model based on one provided, saves it to file.
    :param model: base model on top of which to build the new one
    :param sentences: list of string sentences to build the vocabulary of the new model with
    :param vector_file: string name of file containing vectors to intersect
    :param save_format: string format of vectors for saving
    :param save_file: string file name for saving
    :param size: int parameter for new model creation
    :param min_count: int parameter for new model creation
    :return: new drug model
    """
    drug_model = models.Word2Vec(size=size, min_count=min_count)
    drug_model.build_vocab(sentences)
    total_examples = drug_model.corpus_count

    # add the vocabulary from pretrained model
    drug_model.build_vocab([list(model.vocab.keys())], update=True)

    # use the pretrained vectors, lockf=1.0 allows for updates
    drug_model.intersect_word2vec_format(vector_file, lockf=1.0)

    drug_model.train(sentences, total_examples=total_examples, epochs=drug_model.epochs)

    drug_model.wv.save_word2vec_format(save_format)
    drug_model.save(save_file)

    return drug_model


# TODO: what data type is drug_names??
def find_new_drug_names(drug_names, model, top=100, min_length=6, max_length=40):
    """
    Find new potential drug names based on current drug names and word2vec model.
    :param drug_names: list of current analysed drug names
    :param model: current word2vec model
    :param top: similar matching parameter
    :return: array of strings containing potential new drug names
    """
    drug_names_in_vocab = [d for d in drug_names.keys() if d in model.vocab]
    whitelisted_chars = regex.compile(r"[a-zA-Z0-9\-\.,\_/ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+")
    new_drug_names = []

    for drug_candidate, _ in model.most_similar(positive=drug_names_in_vocab, topn=top):
        if drug_candidate not in drug_names and whitelisted_chars.fullmatch(drug_candidate) is not None:
            new_drug_names.append(drug_candidate)

    bad_vowels = set('ąęóiouy')
    new_drug_names = [d for d in new_drug_names if max_length > len(d) > min_length and d[-1] not in bad_vowels]

    return new_drug_names


def find_similar_words(word, model, per_level=10, max_depth=1):
    """
    Find words similar to the given word
    :param word: string word to search for similarities for
    :param model: trained word2vec model
    :param per_level: int with how many words to analise per similar found
    :param max_depth: int depth of similarities tree
    :return: list of strings containing words similar to input word
    """
    results = set()
    q = Queue()
    q.put((word, 1))

    while not q.empty():
        w, l = q.get()

        if l > max_depth:
            break

        for r, _ in model.most_similar(positive=[w], topn=per_level):
            if r not in results:
                results.add(r)
                q.put((r, l+1))

    return list(results)


def find_symptoms(symptoms, model, synonyms, per_level=10, max_depth=1):
    """
    Finds similar symptoms to the ones provided.
    :param symptoms: list of string symptoms
    :param model: trained word2vec model for finding similarities
    :param synonyms: dictionary of synonyms
    :param per_level: int with how many words to analise per similar found
    :param max_depth: int depth of similarities tree
    :return: list of string similar symptoms
    """
    results = set()

    for s in symptoms:
        results.add(find_similar_words(s, model, per_level, max_depth))

    not_in_synonyms = [r for r in results if r not in synonyms]

    return list(results), not_in_synonyms


def create_symptom_dict(symptoms, synonyms):
    """
    Create a dictionary of symptom synonyms.
    :param symptoms: list of string symptoms
    :param synonyms: dictionary of synonyms
    :return: new dictionary of symptom synonyms
    """
    results = dict()

    for s in symptoms:
        lemma = synonyms[s]
        if lemma and lemma not in results:
            results[lemma] = synonyms[lemma]

    return results
