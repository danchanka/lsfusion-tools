import sys, os, re

outfile = open('cyrillic.txt', 'w', encoding='utf-8')
indir = sys.argv[1]
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.md') and not fullname.endswith('index.md'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            lines = infile.read().split('\n')
            for line in lines:
                has_russian = False
                nline = ''
                for ch in line: 
                    if ch >= 'а' and ch <= 'я':
                        has_russian = True
                        nline += f'[{ch}]'
                    else:
                        nline += ch 
                if has_russian:
                    outfile.write(f'Russian letters: {fullname}:{nline}\n\n')        
