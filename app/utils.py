from django.utils.formats import number_format


def format_money(value):
    return number_format(value, decimal_pos=2, force_grouping=True)
