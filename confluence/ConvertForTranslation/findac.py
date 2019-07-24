import re
import os


data = '';
for filename in os.listdir('test'): 
	with open('test/' + filename, 'r', encoding='utf-8') as infile:
		data += infile.read()

res = re.findall(r'<ac:link>.*?</ac:link>', data)

s = set()

for item in res:
	item = re.sub(r'ri:content-title="[^"]*"', r'ri:content-title="text"', item)
	item = re.sub(r'<!\[CDATA\[.*\]\]>', '<![CDATA[text]]>', item)
	item = re.sub(r'<ac:link-body>.*?<strong>[^<]*</strong></ac:link-body>', 
		r'<ac:link-body>text<strong>text</strong></ac:link-body>', item)
	s.add(item)

res = re.findall(r'<ac:link ac:anchor="[^"]*">.*?</ac:link>', data)

for item in res:
	item = re.sub(r'ac:anchor="[^"]*"', 'ac:anchor="text"', item)
	item = re.sub(r'ri:content-title="[^"]*"', r'ri:content-title="text"', item)
	item = re.sub(r'<!\[CDATA\[.*\]\]>', '<![CDATA[text]]>', item)
	item = re.sub(r'<ac:link-body>.*?<strong>[^<]*</strong></ac:link-body>', 
		r'<ac:link-body>text<strong>text</strong></ac:link-body>', item)
	s.add(item)

with open('all_link.xml', 'w', encoding='utf-8') as outfile:
    for item in s:
    	outfile.write("%s\n" % item)