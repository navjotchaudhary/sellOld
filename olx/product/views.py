from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, ProductImage, Category, Brand
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views import View

# Create your views here.
def productList(request, category_slug=None):
    pro = Product.objects.all()
    categorys = Category.objects.annotate(total_products=Count('product'))
    
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        pro = Product.objects.filter(category=category)

    
    search_query = request.GET.get('search')
    if search_query:
        pro = pro.filter(
            Q(name__icontains = search_query) |
            Q(description__icontains = search_query) |
            Q(condition__icontains = search_query) |
            Q(brand__brand_name__icontains = search_query) |
            Q(owner__username__icontains = search_query)
        )
        
    template = 'product/product_list.html'
    paginator = Paginator(pro,2)
    page = request.GET.get('page')
    pro = paginator.get_page(page)
    context = {
        'product_list':pro,
        'category_list':categorys  
        }
    return render(request,template,context)



def productDetail(request,product_slug):
    data = Product.objects.get(slug=product_slug)
    print(data)
    template = 'product/product_detail.html'
    product_images = ProductImage.objects.filter(product = data)
    context = {
        'product_detail':data,
        'product_images':product_images
    }
    return render(request,template,context)


'''class AddProductView(View):

    def get(self, request):
        if request.user.is_authenticated:
            category  = Category.objects.all()
            brands  = Brand.objects.all()
            context = {
                'categories':category,
                'brands':brands
            }
            return render(request,'product/add_product.html',context)
        else:
            return redirect('product:product_list')
    def post(self,request):
        
        print(request.FILES['fileselect'])
        productName = request.POST['productName']
        productDescription = request.POST['productDescription']
        
        brand = request.POST['brand']
        files = request.FILES['fileselect']
        productCondition = request.POST['productCondition']
        category = request.POST['category']
        price = request.POST['price']
        braand = Brand.objects.get(brand_name = brand)
        item = Product(name = productName,price = price,owner = request.user,description = productDescription,condition = productCondition, brand = braand,image = files)
        item.save()'''


def addProduct(request):
    if request.method == 'POST':
        #print(request.FILES['fileselect'])
        productName = request.POST['productName']
        productDescription = request.POST['productDescription']
        
        brand = request.POST['brand']
        files = request.POST['fileselect']
        productCondition = request.POST['productCondition']
        category = request.POST['category']
        price = request.POST['price']
        braand = Brand.objects.get(brand_name = brand)
        item = Product(name = productName,price = price,owner = request.user,description = productDescription,condition = productCondition, brand = braand,image = "main_image/"+files)
        item.save()
        return redirect('product:product_list')
    else:
        if request.user.is_authenticated:
            category  = Category.objects.all()
            brands  = Brand.objects.all()
            context = {
                'categories':category,
                'brands':brands
            }
            return render(request,'product/add_product.html',context)
        else:
            return redirect('login')
