import sys, re, os, json

if len(sys.argv) < 4:
    print('Usage: create_i18n_sidebar.py current.json labels_map.json current_ru.json')
    sys.exit()

sidebar_i18n_file = open(sys.argv[1], 'r', encoding='utf-8')
labels_map = json.load(open(sys.argv[2], 'r', encoding='utf-8'))

data = sidebar_i18n_file.read()

for eng, ru in labels_map.items():
    data = data.replace(f'"message": "{eng}"', f'"message": "{ru}"')    

with open(sys.argv[3], 'w', encoding='utf-8') as outfile:
    outfile.write(data)
    outfile.close()
     
