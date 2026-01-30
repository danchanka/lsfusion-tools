import sys, os, re

outfile = open('ahref.txt', 'w', encoding='utf-8')
indir = sys.argv[1]
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.md') and not fullname.endswith('index.md'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            data = infile.read()
            results = re.finditer(r'<a href.*?</a>', data)
            for r in results:
                # outfile.write(f'{filename}: {r.group(0)}\n')
                outfile.write(f'{r.group(0)}\n')

