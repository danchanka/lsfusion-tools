import sys, os, re

outfile = open('links.txt', 'w', encoding='utf-8')
indir = sys.argv[1]
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.md') and not fullname.endswith('index.md'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            data = infile.read()
            # results = re.finditer(r'\.md#.*?-([^-]*?)\)', data)
            results = re.finditer(r'\(#.*?-([^-]*?)\)', data)
            for r in results:
                outfile.write(r.group(1) + '\n')

