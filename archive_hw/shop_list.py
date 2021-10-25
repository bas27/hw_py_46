cook_book = {
  'Омлет': [
    {'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
    {'ingredient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
    {'ingredient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
    ],
  'Утка по-пекински': [
    {'ingredient_name': 'Утка', 'quantity': 1, 'measure': 'шт'},
    {'ingredient_name': 'Вода', 'quantity': 2, 'measure': 'л'},
    {'ingredient_name': 'Мед', 'quantity': 3, 'measure': 'ст.л'},
    {'ingredient_name': 'Соевый соус', 'quantity': 60, 'measure': 'мл'}
    ],
  'Запеченный картофель': [
    {'ingredient_name': 'Картофель', 'quantity': 1, 'measure': 'кг'},
    {'ingredient_name': 'Чеснок', 'quantity': 3, 'measure': 'зубч'},
    {'ingredient_name': 'Сыр гауда', 'quantity': 100, 'measure': 'г'},
    ]
  }

from pprint import pprint  

def get_shop_list_by_dishes(dishes, person_count):
  
    shop_list = {}
    
    for dish in dishes:
        
        for lst in cook_book.get(dish):
            if lst['ingredient_name'] in shop_list:
                lst['quantity'] += lst['quantity']
                shop_list[lst['ingredient_name']] = {'quantity':(lst['quantity'])*person_count, 'measure':lst['measure']}
            else:
                shop_list[lst['ingredient_name']] = {'quantity':(lst['quantity'])*person_count, 'measure':lst['measure']}
            
    return shop_list
             

pprint(get_shop_list_by_dishes(['Омлет', 'Утка по-пекински'], 3))