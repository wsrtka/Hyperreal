data_csv_path = ''
import pandas as pd
import hyperreal.datautils.preprocess as preprocess
import hyperreal.overview.stats as stats
df = pd.read_csv(data_csv_path)
df = preprocess.data_pre(df)

print(stats.get_posts_per_year(df))

print(stats.get_most_active_authors(df))

print(stats.get_total_posts(df))

print(stats.get_forum_popularity(df, 384))
