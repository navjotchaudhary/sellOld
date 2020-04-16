from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from olx.settings import AUTH_USER_MODEL
# Create your models here.
class Product(models.Model):
    CONDITION_TYPE = (
        ("New","New"),
        ("Used","Used")
    )



    name = models.CharField(max_length=100)
    owner = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    condition = models.CharField(max_length=100,choices=CONDITION_TYPE)
    price = models.DecimalField(max_digits=17,decimal_places=4)
    created = models.DateTimeField(default = timezone.now)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,null = True)
    brand = models.ForeignKey('brand',on_delete = models.SET_NULL, null = True)
    slug = models.SlugField(blank=True, null = True)
    image = models.ImageField(upload_to='main_image',blank = True, null = True)

    def save(self,*args,**kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)

        super(Product,self).save(*args,**kwargs)


    def __str__(self):
        return self.name


class Category(models.Model):
    ##for product caegory
    clategory_name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to='category/',blank = True, null = True)
    slug = models.SlugField(blank=True, null = True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self,*args,**kwargs):
        if not self.slug and self.clategory_name:
            self.slug = slugify(self.clategory_name)

        super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return self.clategory_name



class Brand(models.Model):
    ##for product caegory
    brand_name = models.CharField(max_length = 50)
    
    
    def __str__(self):
        return self.brand_name



class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete= models.CASCADE)
    image = models.ImageField(upload_to='products/', blank = True, null = True)


    def __str__(self):
        return self.product.name