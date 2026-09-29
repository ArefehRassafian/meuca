from products.models import Product

CART_SESSION_ID = 'cart'
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            # item['product'] = Product.objects.get(id=int(item['id']))
            item['total'] = int(item['quantity']) * int(item['price'])
            item['image'] = Product.objects.filter(pk=int(item["id"])).first().images.all()[0].image.url
            item['name']=Product.objects.filter(pk=int(item["id"])).first().name
            item['code']=str(Product.objects.filter(pk=int(item["id"])).first().code)
            item['final_price'] = str(Product.objects.filter(pk=int(item["id"])).first().final_price)

            yield item


    def add(self, product):
        variant_id = str(product.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0, 'price': str(product.price) , 'id':product.id}
        self.cart[variant_id]['quantity'] += 1
        self.save()


    def sub(self, product):
        variant_id = str(product.id)
        if (variant_id in self.cart) and (self.cart[variant_id]['quantity']!=1) :
            self.cart[variant_id]['quantity'] -= 1
        elif (variant_id in self.cart) and (self.cart[variant_id]['quantity']==1):
            del self.cart[variant_id]
        self.save()
    def delete(self , id):
        if str(id) in self.cart:
            del self.cart[str(id)]
            self.save()

    def remove_cart (self):
        del self.session[CART_SESSION_ID]
        self.save()


    def save(self):
        self.session.modified = True

    def __len__(self):
        cart = self.session.get(CART_SESSION_ID)
        count=0
        for item in cart.values():
            count+=1
        return count

