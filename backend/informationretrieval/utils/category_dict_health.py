category_dictionary = {
    'سلامت روان': 0,
    'دهان و دندان': 1,
    'پوست و مو': 2,
    'تغذیه': 3,
    'سلامت خانواده': 4,
    'سلامت جنسی': 5,
    'پیشگیری و بیماریها': 6
}


def get_category_title(i):
    return dict(zip(category_dictionary.values(), category_dictionary.keys()))[i]
