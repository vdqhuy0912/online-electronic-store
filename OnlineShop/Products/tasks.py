from OnlineShop.celery import app
from Products.models import Product
from .services import  get_price_sep



# def update_product_price_usd():
#     """
#     Task for updating product price
#     in USD currency. Runs every 48 hours.
#     """
#
#     for product in Product.objects.all():
#         product.price_in_usd = get_price_in_usd(product.price)
#         product.price_in_usd_with_discount = get_price_in_usd(product.price_with_discount)
#         product.price_in_usd_view = get_price_sep(product.price_in_usd)
#         product.price_in_usd_with_discount_view = get_price_sep(product.price_in_usd_with_discount)
#         product.save()
