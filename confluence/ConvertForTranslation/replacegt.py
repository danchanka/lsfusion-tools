with open('file.xml', 'r', encoding='utf-8') as myfile:
    data = myfile.read()
data = data.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
with open('file_p.xml', 'w', encoding='utf-8') as outfile:
    outfile.write(data)