from .models import Cart, Product


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
            .annotate_is_in_cart(user)
            .filter(counterparty=user.counterparty)
            .select_related('measurement_unit'))
