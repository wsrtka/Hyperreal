import pandas as pd


def get_user_drugs_posts(user, posts, drug_names, author_col="author", content_col="content"):
    """
    Find the number of times user mentioned drug in post.
    :param user: string containing user name
    :param posts: dataframe containing posts data
    :param drug_names: string list of drug names
    :param author_col: string name of column containing post author name
    :param content_col: string name of column containing post content
    :return: dictionary of drug names and their number of mentions by the specified user
    """
    posts = posts[posts[author_col] == user]
    results = {}

    for d in drug_names:
        count = len(posts[posts[content_col].str.contains(d, case=False, na=False)].index)
        results[d] = count

    return results


def get_user_drugs_forums(user, forums, drug_names, author_col="author", forum_name_col="name"):
    """
    Find the number of times a user posted in drug forum.
    :param user: string containing user name
    :param forums: dataframe containing merged posts and forum data
    :param drug_names: string list of drug names
    :param author_col: string name of column containing post author name
    :param forum_name_col: string name of column containing post content
    :return: dictionary of drug names and number of times a user posted in their forums
    """
    results = {}

    for d in drug_names:
        posts = forums[forums[forum_name_col].str.contains(d, case=False, na=False)]
        count = len(posts[posts[author_col] == user].index)
        results[d] = count

    return results


def get_drug_correlation(drug1, drug2, forums, users=None, author_col="author", based_on="posts", step=100):
    """
    Get the correlation of interest in two drugs based on either drug forum activity or drug mentions in posts
    :param drug1: string containing drug name
    :param drug2: string containing drug name
    :param forums: dataframe containing merged posts and forums data
    :param users: list of strings containing usernames to analise
    :param author_col: string containing name of column with author name
    :param based_on: method of interest computing, get interest based either on drug mentions or forum activity
    :param step: int number specifying how often the function should write it's progress
    :return: int correlation of drug interest
    """
    assert based_on in ["posts", "forums"], "Correlation must be based on one of two data sources."

    if users is None:
        users = forums[author_col].unique()

    data = pd.DataFrame(columns=[drug1, drug2])
    i = 0

    # this takes A LOT of time, it is better to just supply the function with most active users
    for u in users:
        drug1_data = get_user_drugs_posts(u, forums, [drug1]) if based_on == "posts" else get_user_drugs_forums(u, forums, [drug1])
        drug2_data = get_user_drugs_posts(u, forums, [drug2]) if based_on == "posts" else get_user_drugs_forums(u, forums, [drug2])

        data = data.append({drug1: drug1_data[drug1], drug2: drug2_data[drug2]}, ignore_index=True)

        i += 1

        if i % step == 0:
            print(f"Analyzed {(i / len(users)) * 100}% of users.")

    return data.astype('float64').corr(), data
