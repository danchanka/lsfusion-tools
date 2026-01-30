import json, sys, os, re

outfile = open('header_types.txt', 'w', encoding='utf-8')
indir = sys.argv[1]
types = {}
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.md') and not fullname.endswith('index.md'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            lines = infile.read().split('\n')
            ftypes = {re.match(r'#+', line).end() for line in lines if line.startswith('#')}
            types[filename] = list(ftypes)

json.dump(types, open('header_types.txt', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)