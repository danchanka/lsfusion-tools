import sys, os, re

knownHeaders = ['**Syntax**', '**Description**', '**Parameters**', '**Examples**', '**Example**', '**Language**']

outfile = open('stars.txt', 'w', encoding='utf-8')
indir = sys.argv[1]
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.md') and not fullname.endswith('index.md'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            lines = infile.read().split('\n')
            first = True
            for line in lines:
                if line not in knownHeaders and line.startswith('**') and line.endswith('**') and not re.fullmatch(r'[* \t]*', line):
                    if first:
                        outfile.write(filename + '\n')
                        first = False
                    outfile.write(line + '\n')   
            if not first:        
                outfile.write('\n')                
