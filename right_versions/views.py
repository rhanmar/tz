from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseBadRequest

from .models import Deal, Customer, Item

import datetime

from deals.serializers import TopCustomersSerializer

from rest_framework.viewsets import ModelViewSet

from django.db.models import Sum, F, Q, Count

from django.contrib.postgres.aggregates import ArrayAgg

from .utils import get_top_customers


def index(request):
    return render(
        request,
        'deals/index.html')


class TopCustomersView(ModelViewSet):
    queryset = get_top_customers()
    serializer_class = TopCustomersSerializer


def upload_csv(request):
    # DELETE EVERYTHING FROM DATABASE
    Deal.objects.all().delete()
    Customer.objects.all().delete()
    Item.objects.all().delete()

    csv_file = request.FILES["csv_file"]

    if not csv_file.name.endswith('.csv'):
        return HttpResponseBadRequest('Wrong type of file!')

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")

    firstline = True  # skip first line
    for line in lines:
        if firstline:
            firstline = False
            continue

        if len(line) == 0:  # check end of csv file
            break

        fields = line.split(',')
        customer, item, total, quantity, date = fields

        # create / get Customer and Item
        try:
            my_customer = Customer.objects.get(customer_name=customer)
        except Customer.DoesNotExist:
            Customer.objects.create(customer_name=customer)
            my_customer = Customer.objects.get(customer_name=customer)

        try:
            my_item = Item.objects.get(item_name=item)
        except Item.DoesNotExist:
            Item.objects.create(item_name=item)
            my_item = Item.objects.get(item_name=item)

        # create date
        my_date = date.rstrip()
        my_date = datetime.datetime.strptime(
            my_date, "%Y-%m-%d %H:%M:%S.%f")

        Deal.objects.create(
            customer=my_customer,
            item=my_item,
            total=total,
            quantity=quantity,
            date=my_date
        )

    return redirect('index')


def test(request):
    # this view duplicates get_top_customers() func from utils.py
    # but returns HttpResponse
    richest_customers = Deal.objects.values('customer_id').annotate(spent_money=Sum('total')).order_by('-spent_money')[:5]
    richest_customers_id = richest_customers.values('customer_id')
    richest_gems_info = Deal.objects.filter(customer_id__in=richest_customers_id).values('item_id', 'customer_id').distinct()
    richest_gems_id = []
    for elem in richest_gems_info:
        richest_gems_id.append(elem['item_id'])
    required_gems_id = []  # the gems we find
    for i in richest_gems_id:
        if richest_gems_id.count(i) >= 2:
            required_gems_id.append(i)
    required_gems_id = list(set(required_gems_id))
    r = Deal.objects.annotate(
        username=F('customer_id__customer_name'),
        spent_money=Sum('total')).values('username', 'spent_money').annotate(
            gems=ArrayAgg('item_id__item_name',
                distinct=True,
                filter=Q(item_id__in=required_gems_id)
                )).order_by('-spent_money')[:5]
    return HttpResponse(r)
