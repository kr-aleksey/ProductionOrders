# Production orders

## Заказы на производство

### Технологии

* Python 3.11
* Django 4.1
* PostgreSQL 15
* Bootstrap 5.3
* Docker
* CI/CD - GitHub Actions

### О проекте

**Production orders** - это система Production заказов на производство 
продукции. 
**Production orders** предоставляет возможность клиентам производственного 
предприятия размещать заказы. 

Отличительной особенностью этого проекта является то, что он ориентирован на 
OEM производителей и производителей, выпускающих продукцию для других 
производств. Номенклатура таких производителей может быть уникальна для каждого
клиента. Например, OEM производитель выпускает телевизоры на единой платформе
для разных заказчиков. Для каждого заказчика телевизор может иметь свой набор 
опций и логотип. Или производитель упаковки выпускает коробки с 
характеристиками и логотипом заказчика. **Production orders** предоставляет 
заказчику выбор из списка предназначенной для него номенклатуры и из списка 
обезличенной продукции. 

**Production orders** имеет возможность обмениваться данными с ERP системой. 
Обмен осуществляется посредством XML файлов. Использование XML позволяет 
интегрировать **Production orders** с ERP системами различных поставщиков без 
больших временных и финансовых затрат.