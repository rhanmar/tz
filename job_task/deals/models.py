from django.db import models


class Customer(models.Model):
    customer_name = models.CharField(max_length=215)

    def __str__(self):
        return self.customer_name

    def get_customer_name(self):
        return self.customer_name


class Item(models.Model):
    item_name = models.CharField(max_length=215)

    def __str__(self):
        return self.item_name

    def get_item_name(self):
        return self.item_name


class Deal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(
            self.customer,
            self.item,
            self.total,
            self.quantity,
            self.date
        )
