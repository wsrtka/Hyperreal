from hyperreal.textutils.ngrams import *
from hyperreal.datautils.utils import *
from hyperreal.textutils.utils import *
from hyperreal.overview.stats import *
import pandas as pd


narkopedia_file = 'narkopedia.json'
data_csv_file = 'data.csv'

narkopedia_df = get_narkopedia(narkopedia_file)
narkopedia_map = get_narkopedia_map(narkopedia_df)
# teraz mamy słownik narkotyk => inne nazwy

data_df = pd.read_csv(data_csv_file)
content_df = data_df['content']

ngrams_total, ngrams_docfreq = ngram_dict(content_df)

for k, _ in narkopedia_map:
    # dostosuj atrybut length lub nazwe narkotyku
    # funkcja poniżej korzysta z ngrams_describing_drug('marihuana', content_df, ngrams_docfreq), można to jakoś inaczej za pomocą wyniku tej funkcji zwizualizować pewnie
    # przeczytaj funkcję bo ma jeszcze parametry na np. długość ngramu
    show_word_cloud(k, data_df['content'], narkopedia_map, ngrams_docfreq, length=2)
    break


