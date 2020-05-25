from hyperreal.textutils.word2vec import *
from hyperreal.textutils.utils import *
import pandas as pd


data_file = ''
data_df = pd.read_csv(data_file)

model_file = ''
model = load_model_from_file(model_file)

sentences = get_sentences(data_df)

model = finetuned_model(model, sentences, 'fasttext_file', 'drug_w2v', './finetuned_model')

ziolo = find_new_drug_names('marihuana', model)

print(ziolo[10:])
