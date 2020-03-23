from .models import Deal, Customer, Item

from django.db.models import Sum, F, Q, Count

from django.contrib.postgres.aggregates import ArrayAgg


def get_top_customers():
    richest_customers = Deal.objects.values('customer_id'
        ).annotate(spent_money=Sum('total')).order_by('-spent_money')[:5]

    richest_customers_id = richest_customers.values('customer_id')

    richest_gems_info = Deal.objects.filter(customer_id__in=richest_customers_id
        ).values('item_id', 'customer_id').distinct()

    richest_gems_id = []
    for elem in richest_gems_info:
        richest_gems_id.append(elem['item_id'])
    required_gems_id = [] # the gems we find
    for i in richest_gems_id:
        if richest_gems_id.count(i) >= 2:
            required_gems_id.append(i)
    required_gems_id = list(set(required_gems_id))

    result = Deal.objects.annotate(
        username=F('customer_id__customer_name'),
        spent_money=Sum('total')).values('username', 'spent_money'
        ).annotate(
            gems=ArrayAgg('item_id__item_name',
            distinct=True,
            filter=Q(item_id__in=required_gems_id))
            ).order_by('-spent_money')[:5]
    return result
