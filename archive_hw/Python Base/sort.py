import os

def unity_files(path):
    
    lst_files = os.listdir(path)
    
    tmp = {}

    for file in lst_files:
        files_path = os.path.join(os.getcwd(), path, file)
        
        with open (files_path, encoding='utf-8') as f:

            tmp[file] = sum(1 for _ in f)
    
    sorted_tmp = {}
    sorted_keys = sorted(tmp, key=tmp.get)
    for val in sorted_keys:
        sorted_tmp[val] = tmp[val]

    if os.path.isfile(os.path.join(os.getcwd(), 'data.txt')):
        os.remove(os.path.join(os.getcwd(), 'data.txt'))
        # print('Удалено')
    
    # else: print("Файл отсутствует")

    for file, n_line in sorted_tmp.items():
        files_path = os.path.join(os.getcwd(), path, file)
        new_file = os.path.join(os.getcwd(), 'data.txt')
        
        with open(new_file, mode='a',encoding='utf-8') as new_f, open(files_path, mode='r', encoding='utf-8') as f1:
            new_f.write(file + '\n')
            new_f.write(str(n_line) + '\n')
            for line in f1:

                new_f.write(line)
            new_f.write('\n')    

    


unity_files('sorted')