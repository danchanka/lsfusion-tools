# <span class="confluence-anchor-link" id="IDE-newproject"></span>

import sys, os, re

outfile = open('spans.txt', 'w', encoding='utf-8')
indir = sys.argv[1]
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.html') and not fullname.endswith('index.html'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            data = infile.read()
            results = re.finditer(r'<span class="confluence-anchor-link" id="[^"]*?-([^"-]*)"></span>(?:</?.*?>)*?([^<]+)</?.*?>', data)
            for r in results:
                outfile.write(r.group(0) + '\n')
                outfile.write(r.group(1) + '\n')
                outfile.write(r.group(2) + '\n')
                outfile.write('\n')

