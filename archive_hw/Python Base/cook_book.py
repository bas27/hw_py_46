def cook_book(files_cook):
    
    import os
    
    path = os.path.join(os.getcwd(), files_cook)

    with open (path, encoding='utf-8') as file:
        
        result = {}
        
        for name_disches in file:
            disches = name_disches.strip()
            count = int(file.readline().strip())
            tmp_lst = []
        
            for _ in range(count):
            
                ingredient_name, quantity, measure = file.readline().split('|')
                tmp_lst.append({'ingredient_name':ingredient_name, 'quantity':int(quantity), 'measure':measure.strip()})
                result[disches] = tmp_lst
            
            file.readline()
        
    return result

print(cook_book('files/recipes.txt'))
