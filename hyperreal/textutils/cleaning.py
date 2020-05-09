from datetime import date, timedelta
import regex as re
from hyperreal.textutils.utils import lemmatize
from unidecode import unidecode


def clean(text, use_lemmas=False, is_post=False):
    """
    Clean text from unnecessary symbols.
    :param text: string containing text to clean
    :param use_lemmas: if True, text returned text will be lemmatized
    :param is_post: if True, text is cleaned assuming it is a post
    :return: string containing cleaned text
    """
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\\n", " ", text)
    text = re.sub(r"\t", " ", text)

    if not is_post:
        text.strip()
        return text

    text = re.sub(r"http[^\s]+", " ", text)
    text = re.sub(r"images[^\s]+", " ", text)
    text = re.sub(r":D|:p|:P|:d", " ", text)
    text = re.sub(r":\w+:", " ", text)
    text = re.sub(r"[(\[]", "", text)
    text = re.sub(r"[\^_'<>*\]\"?,).:\\/;!@$]", " ", text)
    text = re.sub(r" - ?", " ", text)
    text = re.sub(r" ?- ", " ", text)
    text = re.sub(r"\d+ \d+", " ", text)
    text = re.sub(r" \d+ ", " ", text)
    text = re.sub(r"\w+ pisze", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    text = text.lower()

    if use_lemmas:
        tokens = text.split(' ')
        tokens = [lemmatize(t) for t in tokens]
        text = ' '.join(tokens)

    text = unidecode(text)

    return text


def normalize_date(raw_date):
    """
    Makes sure date is in correct format dd/mm/yyyy.
    :param raw_date: string containing date to be processed
    :return: string containing normalized date
    """
    if raw_date == 'dzisiaj':
        return date.today().strftime("%d/%m/%Y")
    if raw_date == 'wczoraj':
        return (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")

    # [day, raw_month, year] = raw_date.split()
    day, raw_month, year = raw_date.split()

    month = {
        'stycznia': '01',
        'lutego': '02',
        'marca': '03',
        'kwietnia': '04',
        'maja': '05',
        'czerwca': '06',
        'lipca': '07',
        'sierpnia': '08',
        'września': '09',
        'października': '10',
        'listopada': '11',
        'grudnia': '12',
    }.get(raw_month)

    if month is None:
        return (date.today()+timedelta(days=1)).strftime("%d/%m/%Y")

    return "{}/{}/{}".format(day, month, year)

