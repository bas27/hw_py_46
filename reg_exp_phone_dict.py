from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
import pandas as pd

with open('phonebook_raw.csv', encoding='UTF8') as f:
    reader = csv.DictReader(f, delimiter=",")
    contact_list = list(reader)
   
new_list = []
for row in contact_list:
    check_ext = False
    tmp_dict = {}
    tel_num = re.sub(r"(\+7|8)\s*\(?(\d{3})\)?-?\s*(\d{3})-?(\d{2})-?(\d+)(\s*)(\(?(доб.)\)?\s(\d+)\)?)?", r"+7(\2)\3-\4-\5\6\8\9", row['phone'])
       
    tmp_dict['lastname'] = row['lastname'].split()[0]
    
    if len(row['lastname'].split()) == 3:
        tmp_dict['firstname'] = row['lastname'].split()[1]
        tmp_dict['surname'] = row['lastname'].split()[2]
    elif len(row['lastname'].split()) == 2:
        tmp_dict['firstname'] = row['lastname'].split()[1]
        tmp_dict['surname'] = row['surname']
    elif len(row['firstname'].split()) == 2:
        tmp_dict['firstname'] = row['firstname'].split()[0]
        tmp_dict['surname'] = row['firstname'].split()[1]
    else:
        tmp_dict['firstname'] = row['firstname']
        tmp_dict['surname'] = row['surname']

    tmp_dict['organization'] = row['organization']
    tmp_dict['position'] = row['position']
    tmp_dict['phone'] = tel_num
    tmp_dict['email'] = row['email']

    for item in new_list:
        if item['lastname'] == tmp_dict['lastname']:
            if item['firstname'] == tmp_dict['firstname']:
                check_ext = True
                if item['organization'] == '': item['organization'] = row['organization']
                if item['position'] == '': item['position'] = row['position']
                if item['phone'] == '': item['phone'] = row['phone']
                if item['email'] == '': item['email'] = row['email']        
    
    if check_ext == False:
        new_list.append(tmp_dict)

df = pd.DataFrame(new_list)
print(df)

with open('csv_write_dictwriter.csv', 'w', encoding='utf8') as f:
    writer = csv.DictWriter(
        f, fieldnames=list(new_list[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for d in new_list:
        writer.writerow(d)