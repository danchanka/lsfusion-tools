import re
import os
import sys

data = '';

fout = open('alinks.txt', 'w', encoding='utf-8')

cnt = 0
for filename in os.listdir(sys.argv[1]): 
	with open(sys.argv[1] + '/' + filename, 'r', encoding='utf-8') as infile:
		content = infile.read()
		data += content
		res = re.findall(r'https?://documentation[^"]*"', content)		
		if len(res) != 0:
			fout.write("\n%s\n" % filename)	
			for item in res:
				fout.write("%s\n" % item)
				cnt += 1

fout.write(str(cnt))

fout.write('\n------------------------------------------\n\n')

res = re.findall(r'<a[^>]* href="https?://documentation\.lsfusion\.org/pages/viewpage\.action\?pageId=(\d+)(#[^"]*)?"[^>]*>(((?!</a>).)*)</a>', data)

for link in res:
	fout.write(f'{link}\n')

fout.write('\n------------------------------------------\n\n')

res = re.findall(r'https?://documentation[^"]*"', data)

s = set()

for link in res:
	link = re.sub(r'/viewpage\.action\?pageId=\d+"', r'/viewpage.action?pageId=number', link)
	link = re.sub(r'/viewpage\.action\?pageId=\d+#id-[^"]*"', r'/viewpage.action?pageId=number#id-anchor', link)
	s.add(link)

srt = sorted(s)

for item in srt:
	fout.write("%s\n" % item)	

