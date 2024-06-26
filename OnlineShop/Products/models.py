from django.db import models
from django.urls import reverse
from .services import get_discount, get_price_sep, get_rating_star, get_price_in_usd


class ProductCategory(models.Model):
    """
    Model of product category,
    as well model of main category for subcategory.
    """

    title = models.CharField(max_length=200, verbose_name="Category name in header of page", blank=True)
    name = models.CharField(max_length=150, verbose_name="Category name")
    slug = models.SlugField(unique=True, verbose_name="Category name in url")
    subcategory = models.ManyToManyField('ProductSubcategory', verbose_name='Subcategory', blank=True,
                                         db_index=True)

    def get_absolute_url(self):
        return reverse('products_by_cat', kwargs={'slug': self.slug, 'category_id': self.pk})

    def __str__(self):
        return f"Category: {self.name}"

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Products categories'
        ordering = ['id']


class ProductSubcategory(models.Model):
    """Model of product subcategory"""

    title = models.CharField(max_length=200, verbose_name="Subcategory name in header of page", blank=True)
    name = models.CharField(max_length=150, verbose_name="Subcategory name")
    slug = models.SlugField(unique=True, verbose_name="Subcategory name in url")
    main_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Category',
                                      db_index=True)

    def get_absolute_url(self):
        return reverse('by_sub', kwargs={'category_id': self.main_category.pk, 'slug': self.slug, 'sub_id': self.pk})

    def __str__(self):
        return f"Subcategory: {self.name}"

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'Products subcategories'


class ProductMemoryCategory(models.Model):
    """Category of products memories"""

    memory_size = models.CharField(max_length=250, verbose_name='Size of memory', blank=True)
    int_memory_value = models.IntegerField(verbose_name='Value of memory size(In megabytes)', blank=True)

    def __str__(self):
        return f'Memory size: {self.memory_size}'

    class Meta:
        verbose_name = 'Product memory category'
        verbose_name_plural = 'Product memory categories'

    def save(self, *args, **kwargs):
        if str(self.int_memory_value) in self.memory_size:
            """If value of memory have in memory size field"""
            self.memory_size = self.memory_size
        else:
            """If value of memory not in memory size field"""
            if self.int_memory_value == 1000:
                """We write this condition because 1000GB = 1TB"""
                self.memory_size = f'{1}TB'
            else:
                self.memory_size = f'{self.int_memory_value}GB'
        super(ProductMemoryCategory, self).save(*args, **kwargs)

class ProductColorCategory(models.Model):
    """Category of products colors"""

    color_in_admin_panel = models.CharField(max_length=350, verbose_name='Product color in admin panel', blank=True)
    color = models.CharField(max_length=350, verbose_name='Product color')
    color_hex = models.CharField(max_length=350, verbose_name='Product HEX color', blank=True)

    def __str__(self):
        return f'Color: {self.color_in_admin_panel}'

    class Meta:
        verbose_name = 'Color category'
        verbose_name_plural = 'Color categories'


class Product(models.Model):
    """Model of products"""

    PRODUCT_STATUS_CHOICES = [
        ('Have in shop', 'In stock'),
        ('Ends in shop', 'Ends in shop'),
        ('Not in shop', 'Out of stock'),
    ]
    name = models.CharField(max_length=250, verbose_name="Product name")
    characteristics = models.TextField(verbose_name='Characteristics of product', blank=True)
    info = models.TextField(verbose_name='Information about product', blank=True)
    img = models.ImageField(upload_to='products_images/', verbose_name='Photo of product', blank=True)
    main_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, null=True,
                                      verbose_name='Main category of product', blank=True, db_index=True)
    subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.PROTECT, null=True,
                                    verbose_name='Subcategory of product', blank=True, db_index=True)
    price = models.IntegerField(verbose_name='Product price')
    discount_availability = models.BooleanField(default=False, verbose_name='Discount availability')
    discount = models.IntegerField(verbose_name='Discount', blank=True, default=1)
    price_with_discount = models.IntegerField(verbose_name='Product price with discount', default=0, blank=True)
    article = models.CharField(max_length=250, verbose_name='Product article', blank=True)
    status = models.CharField(max_length=300, choices=PRODUCT_STATUS_CHOICES, default='Have in shop',
                              verbose_name='Availability status of product')
    slug = models.SlugField(unique=False, verbose_name="Product name in url", blank=True)
    total_rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Total rating of product',
                                       default=0)
    product_memory = models.ForeignKey(ProductMemoryCategory, on_delete=models.CASCADE, null=True,
                                       verbose_name='Product memory size', related_name='product', blank=True)
    product_color = models.ForeignKey(ProductColorCategory, on_delete=models.CASCADE, null=True,
                                      verbose_name='Product color', related_name='product', blank=True)
    editing = models.BooleanField(default=False,
                                  verbose_name='Dont touch this field, after saving it will be True.')
    bonuses = models.IntegerField(verbose_name='Bonuses for buying this product', default=0)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category': self.main_category.slug,
                                                 'subcategory': self.subcategory.slug,
                                                 'pk': self.pk,
                                                 'slug': self.slug})

    def __str__(self):
        if self.article:
            return f"{self.name}"
        else:
            return f"{self.name}"

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'Products'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        """Discount calculation"""

        if self.discount_availability:
            """If we have discount"""
            self.price_with_discount = get_discount(self.price, self.discount)


        else:
            """If we dont have discount"""
            self.price_with_discount = self.price

        return super(Product, self).save(*args, **kwargs)

    def get_star(self):
        """
        Method for getting stars of rating.
        Go to services.py to see how it works.
        """

        return get_rating_star(self.total_rating)

    def get_price_view(self):
        """Getting product price for template."""

        price_view = get_price_sep(self.price)
        return price_view


    def get_price_with_discount_view(self):
        """Getting product price with discount for template."""

        price_with_discount_view = get_price_sep(self.price_with_discount)
        return price_with_discount_view


class Reviews(models.Model):
    """Model of reviews"""

    name = models.CharField(max_length=200, verbose_name="Name")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product',
                                related_name='review_product')
    review = models.TextField(verbose_name='Review')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    rating = models.FloatField(verbose_name='Rating')
    ip = models.CharField(max_length=20, blank=True, verbose_name='IP address')

    def __str__(self):
        return f"Name: {self.name}, Review ID: {self.id}"

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

    def get_review_star(self):
        """
        Method for getting stars of rating.
        Go to services.py to see how it works.
        """

        return get_rating_star(self.rating)


class ProductColorChoice(models.Model):
    """Model of available choices of product colors"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, verbose_name='Product',
                                related_name='product')
    subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, db_index=True,
                                    verbose_name='Subcategory', null=True)
    color = models.CharField(max_length=250, verbose_name='Color name at the choice button')
    memory = models.ForeignKey(ProductMemoryCategory, on_delete=models.CASCADE, db_index=True,
                               verbose_name='Product memory size', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Is active?')
    background_color = models.CharField(max_length=250, verbose_name='Button background color', blank=True)

    def __str__(self):
        return f'Color: {self.color}'

    class Meta:
        verbose_name = 'Color choice'
        verbose_name_plural = 'Colors choices'


class ProductMemoryChoice(models.Model):
    """Model of available choices of product memories"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, verbose_name='Product',
                                related_name='memory_product')
    subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, db_index=True,
                                    verbose_name='Subcategory', null=True)
    color = models.ForeignKey(ProductColorCategory, on_delete=models.CASCADE, db_index=True,
                              verbose_name='Product color', null=True, blank=True)
    memory = models.CharField(max_length=250, verbose_name='Memory at the choice button', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Is active?')

    def __str__(self):
        return f'Memory: {self.memory}'

    class Meta:
        verbose_name = "memory choice"
        verbose_name_plural = "Memory choices"

class ProductPhotos(models.Model):
    """Model of product photos"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    photo = models.ImageField(upload_to='product_photos/%Y-%m-%d', blank=True, verbose_name='Photo')

    def __str__(self):
        return f'Product: {self.product.name}'

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'Products photos'
