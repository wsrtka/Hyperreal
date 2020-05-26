data_csv_path = 'data.csv'
import pandas as pd
import hyperreal.datautils.preprocess as preprocess
import hyperreal.overview.stats as stats
import hyperreal.overview.plotting as plot
import matplotlib.pyplot as plt


df = pd.read_csv(data_csv_path)
df = preprocess.data_pre(df)

res1 = stats.get_posts_per_year(df)

res2 = stats.get_most_active_authors(df)

res3 = (stats.get_total_posts(df))

res4, name = (stats.get_forum_popularity(df, 'inne-stymulanty'))

# plotting test

plot.plot_post_per_year(df)
plt.show()

plot.plot_author_activity(df)
plt.show()

# plot.plot_total_post_count_per_forum(res3)

print(res4)

plot.plot_forum_popularity(res4, name)
plt.show()


print(stats.get_forum_popularity(df, 'inne-stymulanty'))
