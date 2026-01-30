import sys, re, os, json
import xml.etree.ElementTree as ET

def transform_name(title):
    title = title.replace('MyCompany : ', '')
    title = title.replace('English : ', '')
#    title = title.replace('lsFusion : ', '')
    title = title.replace('&gt;', '>').replace('&lt;', '<')    
    title = re.sub(r'[\s<>()\[\]{}:;\'`"\/\\|?\*~!@#$%^&,]', '_', title)
    title = re.sub(r'__+', '_', title) 
#    title = re.sub(r'_+$', '', title)
    return title

def add_to_filemap(data, filename, file_dict, md_dict):
    title = re.search('<title>(.*?)</title>', data).group(1)
    if title:
        name = transform_name(title)                        
        file_dict[filename] = md_dict[name + ".md"]
    else:
        print(f'error: there was no title in {filename}')

# <span class="confluence-anchor-link" id="IDE-newproject"></span>
def add_to_anchormap(data, filename, d):
    results = re.finditer(r'<span class="confluence-anchor-link" id="[^"]*?-([^"-]*)"></span>(?:</?.*?>)*?([^<]+)</?.*?>', data)
    innerd = {r.group(1) : r.group(2).strip() for r in results}
    d[filename] = innerd

def add_file_id(filename, mdname, id_to_md):
    match = re.fullmatch(r'[^\d]*(\d+)\.html', filename)
    if match:
        id_to_md[match.group(1)] = mdname

def parse_confluence_xml(id_to_md, xml_filename):
    samples_links = {}
    with open(xml_filename, 'r', encoding='utf-8') as xmlfile:
        root = ET.fromstring(xmlfile.read())
        for obj in root.iter('object'):
            if obj.get('class') == 'BodyContent':
                body = ''
                id = 0
                for property in obj.iter('property'):
                    if property.get('name') == 'body':
                        body = property.text
                    elif property.get('name') == 'content' and property.get('class') == 'Page':
                        id = property.find('id').text
                if body and id:
                    # print(f'{id}: ')
                    if id in id_to_md:
                        # print(f'id {id} in dict')
                        links = re.findall(r'"http://localhost:5000/samphighl\?.*?"', body)    
                        simple_links = [link.replace('&amp;', '&').replace('%2F', '/')[1:-1] for link in links]
                        samples_links[id_to_md[id]] = simple_links
                    # else:    
                    #     # print(f'id {id} not in dict')
    return samples_links

settings = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
file_dict = {}
anchor_dict = {}
id_to_md = {}
indir = settings['html_dir']
md_dict = json.load(open(settings["mdmap"], 'r', encoding='utf-8'))

print('building maps...')
for filename in os.listdir(indir):
    fullname = indir + '/' + filename 
    if os.path.isfile(fullname) and fullname.endswith('.html') and not fullname.endswith('index.html'):
        with open(fullname, 'r', encoding='utf-8') as infile:
            data = infile.read()
            add_to_filemap(data, filename, file_dict, md_dict)
            add_to_anchormap(data, file_dict[filename], anchor_dict)
            add_file_id(filename, file_dict[filename], id_to_md)

json.dump(file_dict, open(settings['filemap'], 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
json.dump(anchor_dict, open(settings['anchormap'], 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

samples_dict = parse_confluence_xml(id_to_md, settings['xml_file'])
# print(len(samples_dict)) 
json.dump(samples_dict, open(settings['samples'], 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

print('end of building maps')