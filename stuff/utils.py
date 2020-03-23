from .models import Deal, Customer, Item

from django.db.models import Sum


def find_similarities(l1, l2):
    # compare two lists of gems
    result = []
    for element in l1:
        if element in l2:
            result.append(element)
    return result


def change_gems(customers_data):
    # find similar gems
    new_gems_data = {}
    for customer1 in customers_data:
        new_gems_data[customer1] = []
        list_of_gems = []
        for customer2 in customers_data:
            if customer1 is not customer2:
                sim = find_similarities(
                    customers_data[customer1]['gems'],
                    customers_data[customer2]['gems'])
                list_of_gems.extend(sim)
        new_gems_data[customer1].extend(list(set(list_of_gems)))
    # replace all gems by similar gems
    for key in new_gems_data:
        customers_data[key]['gems'] = new_gems_data[key]


def make_customers_data(customers):
    result = {}
    for customer in customers:
        # add username, spent money
        name = Customer.objects.get(
            id=customer['customer_id']).get_customer_name()
        total = customer['spent_money']
        result[name] = {}
        result[name]['spent_money'] = total
        result[name]['id'] = customer['customer_id']
        result[name]['username'] = name

        # add gems
        customer_items = []
        customer_items_id = Deal.objects.filter(
            customer_id=customer['customer_id']).values('item_id').distinct()
        for item in customer_items_id:
            item_name = Item.objects.get(id=item['item_id']).get_item_name()
            customer_items.append(item_name)
        result[name]['gems'] = customer_items
    return result


def get_top_customers():
    top_customers = Deal.objects.values('customer_id').annotate(
        spent_money=Sum('total')).order_by('-spent_money')[:5]

    # create dict with customers data (username, spent money, gems, id)
    customers_data = make_customers_data(top_customers)

    # replace all gems by similar gems
    change_gems(customers_data)

    # make list of data dictionaries
    result = []
    for key in customers_data:
        result.append(customers_data[key])

    return result

