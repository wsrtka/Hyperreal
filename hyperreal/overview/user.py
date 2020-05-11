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
        count = posts[posts[content_col].str.contains(d, case=False)].count(axis=0)
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
        posts = forums[forums[forum_name_col].str.contains(d, case=False)]
        count = posts[posts[author_col] == user].count(axis=0)
        results[d] = count

    return results


def get_drug_correlation(drug1, drug2, forums, author_col="author", based_on="posts"):
    """
    Get the correlation of interest in two drugs based on either drug forum activity or drug mentions in posts
    :param drug1: string containing drug name
    :param drug2: string containing drug name
    :param forums: dataframe containing merged posts and forums data
    :param author_col: string containing name of column with author name
    :param based_on: method of interest computing, get interest based either on drug mentions or forum activity
    :return: int correlation of drug interest
    """
    assert based_on in ["posts", "forums"], "Correlation must be based on one of two data sources."

    users = forums[author_col].unique()
    data = pd.DataFrame(columns=[drug1, drug2])

    for u in users:
        drug1_data = get_user_drugs_posts(u, forums, [drug1]) if based_on == "posts" else get_user_drugs_forums(u, forums, [drug1])
        drug2_data = get_user_drugs_posts(u, forums, [drug2]) if based_on == "posts" else get_user_drugs_forums(u, forums, [drug2])

        data = data.append({drug1: drug1_data[drug1], drug2: drug2_data[drug2]}, ignore_index=True)

    # actually can make use of just returning data df
    return data.corr
