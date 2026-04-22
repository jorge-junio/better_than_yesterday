from django.utils import timezone
from django.db.models import Sum, F, Count
from app.utils import format_money
from brands.models import Brand
from categories.models import Category
from products.models import Product
from sales.models import Sale, SaleItem


def get_product_metrics():
    # calcula direto no banco de dados
    metrics = Product.objects.aggregate(
        total_cost_price=Sum(F('cost_price') * F('quantity')),
        total_selling_price=Sum(F('selling_price') * F('quantity')),
        total_quantity=Sum('quantity'),
    )

    total_selling_price = metrics['total_selling_price'] or 0
    total_cost_price = metrics['total_cost_price'] or 0

    metrics['total_profit'] = total_selling_price - total_cost_price

    metrics['total_cost_price'] = format_money(total_cost_price)
    metrics['total_selling_price'] = format_money(total_selling_price)
    metrics['total_profit'] = format_money(metrics['total_profit'])
    metrics['total_quantity'] = metrics['total_quantity'] or 0
    return metrics


def get_sales_metrics():
    sales_metrics = Sale.objects.aggregate(
        total_sales_value=Sum('total_amount'),
        total_sales=Count('id'),
    )
    items_metrics = SaleItem.objects.aggregate(
        total_sales_cost=Sum(F('cost_price') * F('quantity')),
        total_product_sold=Sum('quantity'),
    )

    total_sales_cost = items_metrics['total_sales_cost'] or 0
    total_sales_value = sales_metrics['total_sales_value'] or 0
    total_product_sold = items_metrics['total_product_sold'] or 0
    total_sales = sales_metrics['total_sales'] or 0

    return {
        'total_sales_cost': format_money(total_sales_cost),
        'total_sales_value': format_money(total_sales_value),
        'total_sales_profit': format_money(total_sales_value - total_sales_cost),
        'total_product_sold': total_product_sold,
        'total_sales': total_sales,
    }


def get_daily_sales_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    values = []

    for date in dates:
        sales_total = Sale.objects.filter(
            created_at__date=date
        ).aggregate(
            total_sales=Sum('total_amount')
        )['total_sales'] or 0
        values.append(float(sales_total))

    return {
        'dates': dates,
        'values': values,
    }


def get_daily_sales_quantity_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    quantities = []

    for date in dates:
        sales_quantity = Sale.objects.filter(created_at__date=date).count()
        quantities.append(float(sales_quantity))

    return {
        'dates': dates,
        'values': quantities,
    }


def get_graphic_product_category_metric():
    categories = Category.objects.all()
    return {c.name: Product.objects.filter(category=c).count() for c in categories}


def get_graphic_product_brand_metric():
    brands = Brand.objects.all()
    return {b.name: Product.objects.filter(brand=b).count() for b in brands}
