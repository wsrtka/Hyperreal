from hyperreal.textutils.word2vec import *

symptoms = ['mdlosci', 'bol', 'wymioty']
model = ... # z new_drug_names_example
synonyms = [] #magiczny plik formatu .out który posiadała poprzednia grupa projektowa, synonimy jezyka polskiego jako slownik slowo: synonim
#olac synonimy

new_symptoms = find_symptoms(symptoms, model, synonyms)

# z new_symptoms nie robimy wykresu, jest do wypisania po prostu
