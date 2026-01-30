import sys, os, re

indir = sys.argv[1]
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.md') and not fullname.endswith('index.md'):
        infile = open(fullname, 'r', encoding='utf-8')
        data = infile.read()
        infile.close()
        data = data.replace(':::info', ':::note')
        outfile = open(fullname, 'w', encoding='utf-8')
        outfile.write(data)
        outfile.close()

