from datetime import datetime
import re


# Converts goodreads date format into datetime
def standardize_dates(input_date_str):
    try:
        if input_date_str == 'unknown':
            output_dt = None
            return output_dt
        try:
            return datetime.strptime(input_date_str, '%b %d, %Y')
        except:
            return datetime.strptime(input_date_str, '%Y')
    except:
        pass


# Converts text-based goodreads rating into an integer
def str_to_int_rating(str_rating):
    if bool(re.search(r"it was amazing", str_rating)):
        int_rating = 5
    elif bool(re.search(r"really liked it", str_rating)):
        int_rating = 4
    elif bool(re.search(r"liked it", str_rating)):
        int_rating = 3
    elif bool(re.search(r"did not like it", str_rating)):
        int_rating = 1
    else:
        int_rating = None
    return int_rating


def get_number_of_pages(input_td_str):
    if input_td_str == 'num pages unknown\n':
        return None
    else:
        return int(re.search(r'[\d]+', input_td_str).group())
