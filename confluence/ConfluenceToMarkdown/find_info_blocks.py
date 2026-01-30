import json, sys, os, re

def getPrefix(data):
    match = re.match(r'<div class="confluence-information-macro confluence-information-macro-information">(?:<[^>]*?>)*([^<]{1,50})', data)
    return match.group(1)

def getSuffix(data):
    match = re.search(r'([^>]{1,19})(?:<[^>]*>)*</div></div>\s*$', data)
    if not match:
        print(f'{data}\n')
        return ''
    return match.group(1)

settings = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
indir = settings['html_dir']
filemap = json.load(open(settings['filemap'], 'r', encoding='utf-8'))

infodiv_text = '<div class="confluence-information-macro confluence-information-macro-information">'
logfile = open(settings['infomap_log'], 'w', encoding='utf-8')

allcnt = 0
allp = 0
infomap = {}
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.html') and not fullname.endswith('index.html'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            data = infile.read()
            positions = re.findall(infodiv_text, data)
            allp += len(positions)
            pos = 0
            mdname = filemap[filename]
            while True:
                pos = data.find(infodiv_text, pos)
                if pos == -1: break
                endpos = pos + 1
                depth = 1
                while depth > 0:
                    enddivpos = data.find('</div>', endpos)
                    match = re.search(r'<div( class=".*?")?>', data[endpos:])            
                    startdivpos = -1
                    if match: 
                        startdivpos = endpos + match.start() 
                    if startdivpos == -1 or enddivpos < startdivpos:
                        depth -= 1
                        endpos = enddivpos + len('</div>')
                    else:
                        depth += 1
                        endpos = endpos + match.end() - 1     

                info = data[pos:endpos] 
                prefix = getPrefix(info)       
                suffix = getSuffix(info)
                if mdname not in infomap:
                    infomap[mdname] = []
                infomap[mdname].append({'prefix': prefix.lstrip(), 'suffix': suffix.rstrip()})

                logfile.write(f'{filename}: {info}\n')
                logfile.write('\n')            

                allcnt += 1
                pos = endpos

logfile.write(f'Total: {allcnt} ({allp})\n')                

json.dump(infomap, open(settings['infomap'], 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

# .*?\.html: <div class="confluence-information-macro confluence-information-macro-information"><span class="aui-icon aui-icon-small aui-iconfont-info confluence-information-macro-icon"></span><div class="confluence-information-macro-body">(?:<p(?: class=".*?")?>)?(?:<span>)?([^<]{1,50})
# ([^<>]{1,20})(?:<[^>]*>)*</div></div>$