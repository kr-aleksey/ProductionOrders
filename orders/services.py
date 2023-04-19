from django.db.models import Max

from .models import Cart, Order, OrderProduct, Product


def check_product_rights(user, product):
    """
    Проверяет право пользователя на продукт.
    """
    if user.is_anonymous:
        return False
    if None in (user.counterparty, product.counterparty):
        return False
    if user.counterparty == product.counterparty:
        return True
    return False


def creat_or_update_cart_item(user, product, quantity):
    """
    Обновляет или добавляет продукт в корзине.
    """
    if not check_product_rights(user, product):
        return None
    cart_item, _ = Cart.objects.update_or_create({'quantity': quantity},
                                                 user=user,
                                                 product=product)
    return cart_item


def delete_cart_item(user, product):
    """
    Удаляет продукт из корзины.
    """
    Cart.objects.filter(user=user, product=product).delete()


def get_products_for_user(user):
    """
    Возвращает queryset с доступными для пользователя продуктами.
    Аннотирует параметром is_in_cart (в корзине покупок).
    """
    if user.is_anonymous or user.counterparty is None:
        return Product.objects.none()
    return (Product
            .objects
            .in_stock()
            .filter(counterparty=user.counterparty)
            .annotate_is_in_cart(user))


def get_cart_items(user):
    """
    Возвращает queryset с продуктами в корзине пользователя.
    """
    if user.is_anonymous:
        return Cart.objects.none()
    return (user
            .products_in_cart
            .filter(product__counterparty=user.counterparty,
                    product__in_stock=True))


def get_new_order_number(user):
    """
    Возвращает номер для нового заказа пользователя.
    """
    if user.is_anonymous:
        return None
    last = (Order
            .objects
            .filter(counterparty=user.counterparty)
            .aggregate(last=Max('number'))['last']) or 0
    return last + 1


def clear_cart(user):
    Cart.objects.filter(user=user).delete()


def create_order_from_cart(user, note):
    """
    Создает Order с продуктами из корзины пользователя, очищает корзину.
    """
    cart_items = get_cart_items(user)
    order_number = get_new_order_number(user)
    order = Order.objects.create(number=order_number,
                                 customer=user,
                                 counterparty=user.counterparty,
                                 status=Order.CREATED,
                                 note=note)
    order_product_list = [
        OrderProduct(order=order,
                     product=i.product,
                     quantity=i.quantity) for i in cart_items
    ]
    OrderProduct.objects.bulk_create(order_product_list)
    clear_cart(user)
