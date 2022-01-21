from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
import pandas as pd


# print(os.listdir())
with open('phonebook_raw.csv', encoding='UTF8') as f:
  rows = csv.reader(f, delimiter=",")
  headers = next(rows)
  # print('Headers: ', headers)
  contacts_list = list(rows)
  # print(contacts_list)
  new_list = []
  new_list.append(headers)

  # pattern = re.match()

  for el in contacts_list:
      tmp = []
      tel_num = re.sub(r"(\+7|8)\s*\(?(\d{3})\)?-?\s*(\d{3})-?(\d{2})-?(\d+)(\s*)(\(?(доб.)\)?\s(\d+)\)?)?", r"+7(\2)\3-\4-\5\6\8\9", el[5])
      
      tmp.append(el[0].split()[0])        
      if len(el[0].split()) == 3:
        tmp.append(el[0].split()[1])
        tmp.append(el[0].split()[2])
      elif len(el[0].split()) == 2:
        tmp.append(el[0].split()[1])
        tmp.append(el[1])
      elif len(el[1].split()) == 2:
        tmp.append(el[1].split()[0])
        tmp.append(el[1].split()[1])
      # elif len(el[1].split()) == 1:
      else:
        tmp.append(el[1])
        tmp.append(el[2])
    
      tmp.append(el[3])
      tmp.append(el[4])
      tmp.append(tel_num)
      tmp.append(el[6])

      
      new_list.append(tmp)

  



  # df = pd.DataFrame(new_list)

  # df = df.groupby('0')
  # pprint(out)
  out_list = []
  
  for contact in new_list:
    
    print(contact[0])
    
    # print(tmp)


  # pprint(new_list)  


    # tmp.append()



# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
# with open("phonebook.csv", "w", encoding='utf8') as f:
#   datawriter = csv.writer(f, delimiter=',')
#   # Вместо contacts_list подставьте свой список
#   datawriter.writerows(new_list)





# "(\+7|8)?\s*?\(?\d+\)?\s*?[\d]+-?\d*-?\d+\s?(\(?(доб.)\)?\s(\d+)\)?)?"
# /(\+7|8)\s?\(?(\d{3})\)?-?\s*?(\d{3})-?(\d{2})-?(\d+)\s?(\(?(доб.)\)?\s(\d+)\)?)?/gm - номера телефонов
# /[\w\d.]+@\w+\.\w+/gm - электронка
# reader = csv.DictReader(f)
    # for row in reader:
    #     print(row)