from django.utils import timezone


def get_product_metrics():
    return {
        'total_cost_price': 0,
        'total_selling_price': 0,
        'total_profit': 0,
        'total_quantity': 0,
    }


def get_sales_metrics():
    return {
        'total_sales_cost': 0,
        'total_sales_value': 0,
        'total_sales_profit': 0,
        'total_product_sold': 0,
        'total_sales': 0,
    }


def get_daily_sales_data():
    return {
        'dates': [str(timezone.now().date())],
        'values': [0.0],
    }


def get_daily_sales_quantity_data():
    return {
        'dates': [str(timezone.now().date())],
        'values': [0.0],
    }


def get_graphic_product_category_metric():
    return {}


def get_graphic_product_brand_metric():
    return {}
