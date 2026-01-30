import sys, re, os, json
import urllib.request

def get_dirs(settings):
    input_dir = settings["input_dir"]
    if not os.path.isdir(input_dir):                
        print(f'"{input_dir}" is not a correct path to directory. ' + usage_string)
        sys.exit()

    output_dir = settings["output_dir"]
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    if not input_dir.endswith('/'):
        input_dir += '/'        
    if not output_dir.endswith('/'):
        output_dir += '/'        
    return input_dir, output_dir

def transform_tables(data, filename, samples_links, samples_url):
    lines = data.split('\n')
    nlines = []
    table_lines = []
    inside_simple_table = False
    opened = 0
    sample_index = 0
    for line in lines:
        if line.lstrip().startswith('<table'):
            opened += 1
            if opened == 1:
                inside_simple_table = True
                if line.lstrip().startswith('<table class="highlighttable"'):
                    inside_simple_table = False
                    # if sample_index == 0:
                    #     nlines.append('import {CodeSample} from \'./CodeSample.mdx\'')
                    #     nlines.append('')

                    # <CodeSample url="https://documentation.lsfusion.org/sample?file=ActionSample&block=write"/>                        
                    url = samples_links[sample_index].replace("http://localhost:5000/samphighl", samples_url)    
                    codeblock = get_codeblock_by_url(url)
                    nlines.extend(codeblock)
                    # nlines.append(f'<CodeSample url="{url}"/>')
                    sample_index += 1
                # else:    
                #     nlines.append('[table was removed]')

        if opened == 0:
            nlines.append(line)   
        elif inside_simple_table:    
            table_lines.append(line)

        if line.lstrip().startswith('</table>'):
            opened -= 1    
            if opened == 0 and inside_simple_table:
                inside_simple_table = False
                transformed_table_lines = transform_simple_table(table_lines)
                transformed_table_lines = extra_execution_auto_file_check(filename, transformed_table_lines)
                nlines.extend(transformed_table_lines)
                table_lines = []

    return '\n'.join(nlines)    

def get_codeblock_by_url(url):
    lines = []
    lines.append('```lsf')

    with urllib.request.urlopen(url) as response:
        for line in response:
            lines.append(line.rstrip().decode('utf-8'))

    lines.append('```')
    return lines

def transform_simple_table(lines):
    data = '\n'.join(lines)
    data = transform_links_inside_table(data)
    data = remove_style_from_table(data) 
    data = replace_em_tag(data)
    rows = []
    pos = 0
    while True:
        tr_start = data.find('<tr', pos)
        if tr_start == -1:
            break
        close_pos = find_close_tag_pos(data, tr_start + 1, '<tr', '</tr>')
        rows.append(get_table_row(data[tr_start:close_pos]))
        pos = close_pos

    if len(rows) == 1:
        if len(rows[0]) != 2:
            print(f'one row table with unusual number of cells\n{data}')
        return create_caution_block(rows)     
    else:
        return create_md_table(rows)    
    return data.split('\n')

def extra_execution_auto_file_check(filename, lines):
    if filename == 'Execution_auto_.md':
        data = '\n'.join(lines)
        data = re.sub(r'<code class=.*?>', '', data).replace('</code>', '')
        data = re.sub(r'<pre class=.*?>', '', data).replace('</pre>', '')
        data = data.replace('$INSTALL_DIR/Server/bin/lsfusion4_serverw.exe', '$INSTALL\\_DIR/Server/bin/lsfusion4\\_serverw.exe')
        data = data.replace('FUSION_OPTS', 'FUSION\\_OPTS')
        return data.split('\n')
    return lines    

def transform_links_inside_table(data):
    return re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', data)

def remove_style_from_table(data):
    return re.sub(r'\bstyle=".*?"', '', data) 

def replace_em_tag(data):
    data = re.sub(r'<em.*?>', '*', data)
    return data.replace('</em>', '*')

def get_table_row(data):
    row = []
    pos = 1
    cell_tag = 'td' if data.find('<td', pos) != -1 else 'th'
    open_tag = f'<{cell_tag}'
    close_tag = f'</{cell_tag}>'
    while True:
        td_start = data.find(open_tag, pos)
        if td_start == -1:
            break
        close_pos = find_close_tag_pos(data, td_start+1, open_tag, close_tag)
        row.append(data[data.find('>', td_start) + 1 : close_pos - len(close_tag)].replace('\n', '<br/>').replace('|', '\\|'))
        pos = close_pos
    return row    


def create_caution_block(rows):
    return [':::caution', rows[0][1].replace('<p>', '').replace('</p>', ''), ':::']

def create_md_table(rows):
    cells_cnt = len(rows[0])
    lines = ['|' + '|'.join(rows[0]) + '|', '|' + '---|'*cells_cnt]
    for row in rows[1:]:
        lines.append('|' + '|'.join(row) + '|')
    return lines

def find_close_tag_pos(data, start_pos, open_tag, close_tag):
    opened = 1
    cur_pos = start_pos
    while opened > 0:
        open_pos = data.find(open_tag, cur_pos)
        close_pos = data.find(close_tag, cur_pos)
        if open_pos != -1 and open_pos < close_pos:
            opened += 1
            cur_pos = open_pos + len(open_tag)
        else:
            opened -= 1
            cur_pos = close_pos + len(close_tag)            
    return cur_pos
        
def escape_title(title):
    return '\'' + title + '\''       

def create_title(data, is_category, overview_str):
    lines = data.split('\n')
    title = lines[0][2:]
    data = '---\n'
    if is_category:
        data += f'title: {escape_title(title + ": " + overview_str)}\n'
        data += f'sidebar_label: {overview_str}'
    else:
        data += f'title: {escape_title(title)}'
    data += '\n---\n' + '\n'.join(lines[1:])
    return data

def replace_html_ltgt(data):
    nlines = []
    lines = data.split('\n')
    for line in lines:
        if line.find('&gt;') != -1 and line.find('&lt;') != -1:
            line = line.replace('&gt;', '\\>').replace('&lt;', '<')    
        else:     
            line = line.replace('&gt;', '>').replace('&lt;', '<')
        nlines.append(line)
    return '\n'.join(nlines)

def trash_stars(line):
    return line.count('*') > 2 and re.fullmatch(r'[* \t]*', line)

def make_headers(data):
    lines = data.split('\n')
    nlines = []
    for line in lines:
        if not trash_stars(line):
            if len(line) > 2 and line.startswith('**') and line.endswith('**') and not re.fullmatch(r'[A-Z* \t]+', line):
                nlines.append('### ' + line[2:-2])
            else:
                nlines.append(line)    
    return '\n'.join(nlines)    

def change_headers(data):
    lines = data.split('\n')
    types = sorted(list({re.match(r'#+', line).end() for line in lines if line.startswith('#')}))
    change_map = {}
    if len(types) == 1:
        change_map = { types[0]: 3 }
    elif types == [3, 5, 6]:
        change_map = { 3: 4, 5: 2, 6: 3 }
    else:
        l = 2
        for i in types:
            change_map[i] = l
            l += 1 

    nlines = []
    for line in lines:
        if line.startswith('#'):
            dashes = re.match(r'#+', line).end()
            line = change_map[dashes] * '#' + line[dashes:]
        nlines.append(line)

    return '\n'.join(nlines)

def fix_image_links(data):
    return re.sub(r'<img src="(.*?)".*?/>', r'![](\1)', data)

def remove_unnecessary_stars(data):
    # matches = list(re.finditer(r'[^*](\*\*)[^*]|[^*](\*\*)$|^(\*\*)[^*]|^(\*\*)$', data))
    # ndata = ''
    # prev = 0
    # for i in range(len(matches)-1):
    #     if i % 2 == 0 and re.fullmatch(r'\s+', data[matches[i].end(1) : matches[i+1].start(1)]):
    #         ndata += data[prev:matches[i].start(1)]
    #         prev = matches[i+1].end(1)
    # ndata += data[prev:]        
    data = re.sub(r'\n\*\*[ \t]*\n\*\*', '', data)
    return data

def remove_myCompany_staff(data):
    lines = data.split('\n')
    nlines = []
    for line in lines:
        if line.startswith('## Attachments:') or line.startswith('### Attachments:'):
            break
        if '![](attachments/thumbnails/1146972/1147367)' in line: continue
        if '![](attachments/thumbnails/1146972/1147365)' in line: continue
        if '![](attachments/1146972/1147367.png)' in line: continue
        if '![](attachments/1146972/1147365.png)' in line: continue
        if '![](plugins/servlet/confluence/placeholder/unknown-attachment)' in line: continue
        
        nlines.append(line)
    return '\n'.join(nlines)

def transform_broken_MyCompanyLinks(data):
    logfile = open('mycompany_links.log', 'w', encoding='utf-8')
    html_map = load_map('filemap_mc_ru.json')
    replacements = {}
    for oldfile, newfile in html_map.items():
        oldlink = f'https://mycompany-docs.lsfusion.org/pages/viewpage.action?pageId={oldfile[:-5]}'
        data = data.replace(oldlink, newfile)
        logfile.write(f'{oldlink} -> {newfile}\n')
    return data

def transform_file_content(data, filename, samples_links, samples_url, info_list, is_category, overview_str):
    data = transform_broken_MyCompanyLinks(data)
    data = transform_tables(data, filename, samples_links, samples_url)
    data = replace_html_ltgt(data)
    data = create_title(data, is_category, overview_str)
    data = make_headers(data)
    data = change_headers(data)
    data = fix_image_links(data)
    data = add_info_blocks(data, info_list)
    data = remove_unnecessary_stars(data)
    data = remove_myCompany_staff(data)
    return data    
    
def load_map(filename):
    return json.load(open(filename, 'r', encoding='utf-8'))

def header_text_to_anchor(text):
    anchor = re.sub(r'\s+', '-', text.lower())
    anchor = re.sub(r'[/()\']', '', anchor)
    return anchor

def fix_anchors(data, anchors_map, filename, logfile):
    data = re.sub(r'\.md#.*?-([^-()]*?)\)', r'.md#\1)', data)  # '.md#WRITEoperator-extension)' -> '.md#extension'
    data = re.sub(r'\(#.*?-([^-()]*?)\)', r'(#\1)', data) # '(#Interactiveview-delete)' -> '(#delete)'

    replacements = {}
    all_count = 0
    broken_count = 0

    for r in re.finditer(r'\]\(([^)]*?\.md)#([^)]*?)\)', data): # ](filename.md#id)
        lfilename = r.group(1)
        anchor = r.group(2)
        all_count += 1
        if anchor not in anchors_map[lfilename]:
            broken_count += 1
            replacements[f'({lfilename}#{anchor})'] = f'({lfilename}#{anchor}-broken)'       

    for r in re.finditer(r'\(#([^)]*?)\)', data): # ](#id)
        anchor = r.group(1)
        all_count += 1
        if anchor not in anchors_map[filename]:
            broken_count += 1
            replacements[f'(#{anchor})'] = f'(#{anchor}-broken)'

    for key, value in replacements.items():
        logfile.write(f'Broken {filename}: {key} -> {value}\n')
        data = data.replace(key, value)            
    return (data, all_count - broken_count, broken_count) 

def fix_links(data, anchors_map, filename, logfile, filemap_name, md_map_name):
    html_to_md = load_map(filemap_name)
    for html, md in html_to_md.items():
        data = data.replace(html, md)

    md_to_md = load_map(md_map_name)    
    for md_name_source, md_name_dest in md_to_md.items():
        data = data.replace(md_name_source, md_name_dest)

    data = re.sub(r'(\[[^\[]*?\])\(\.\./\w+?/(.*?)\)', r'\1(\2)', data) # [Learn](../LSFUS/Learn.md) -> [Learn](Learn.md)

    return fix_anchors(data, anchors_map, filename, logfile)    

def add_anchor_ids_to_headers(files, logfile, anchormap_filename):
    anchor_map = load_map(anchormap_filename)
    for filename in files:
        if filename in anchor_map:
            data = files[filename]
            lines = data.split('\n')
            nlines = []
            headers = set()
            for line in lines:
                if line.startswith('#'):
                    header = re.sub(r'^#+', '', line).strip().replace('*', '')    
                    for key, value in anchor_map[filename].items():
                        if header == value:
                            line = f'{line} {{#{key}}}'
                            break
                    headers.add(header)        
                nlines.append(line)    
                                
            to_delete = [key for key, value in anchor_map[filename].items() if value not in headers] 
            for del_key in to_delete:
                # logfile.write(f'Filtered {filename}: {del_key} -> {anchor_map[filename][del_key]}\n') 
                del anchor_map[filename][del_key]
            data = '\n'.join(nlines)
            files[filename] = data    
    return anchor_map            

def transform_files(settings, indir):
    samples_links = load_map(settings["samples"])
    infomap = load_map(settings["infomap"])
    categories = set(load_map(settings['category_list']))
    files = {}
    for filename in os.listdir(indir):
        fullname = indir + filename 
        if os.path.isfile(fullname) and fullname.endswith('.md') and not fullname.endswith('index.md'):
            infile = open(fullname, 'r', encoding='utf-8')
            data = infile.read()
            infile.close()
            if len(data) > 0 and data[0] == '#': # not transformed earlier
                files[filename] = transform_file_content(data, filename, samples_links.get(filename, []), settings["samples_url"], infomap.get(filename, []), filename in categories, settings['overview_str'])
    return files

def fix_all_links(settings, files):
    logfile = open(settings["anchors_log"], 'w', encoding='utf-8')
    anchors_map = add_anchor_ids_to_headers(files, logfile, settings["anchormap"])
    # json.dump(anchors_map, logfile, indent=4)
    success = 0
    fail = 0
    for filename, data in files.items():
        data, s, f = fix_links(data, anchors_map, filename, logfile, settings["filemap"], settings["mdmap"])
        success += s
        fail += f
        files[filename] = data

    logfile.write(f'success: {success}, fail: {fail}, percent: {0 if success + fail == 0 else success / (success + fail)}')    

def add_info_blocks(data, info_list):
    lines = data.split('\n')
    cur_block = 0
    opened = False
    nlines = []
    tmp = []
    for line in lines:
        if cur_block >= len(info_list):
            nlines.append(line)
        else:
            if not opened and line.lstrip().replace('\\*', '*').replace('\\[', '[').replace('\\]', ']').startswith(info_list[cur_block]['prefix']):
                opened = True

            if not opened:
                nlines.append(line)  
            else:      
                tmp.append(line)
                if line.rstrip().replace('\\*', '*').replace('\\[', '[').replace('\\]', ']').endswith(info_list[cur_block]['suffix']):
                    opened = False
                    tmp[0] = tmp[0].lstrip()
                    nlines.append('')
                    nlines.append(':::info')
                    nlines.extend(tmp)
                    nlines.append(':::')    
                    tmp = []
                    cur_block += 1

    if opened:
        nlines.extend(tmp)

    for i in range(cur_block, len(info_list)):
        print(f'Error: block ("{info_list[i]["prefix"]}", "{info_list[i]["suffix"]}") not replaced\n')

    return '\n'.join(nlines)    

def write_files(outdir, files):
    for filename, data in files.items():
        with open(outdir + filename, 'w', encoding='utf-8') as outfile:
            outfile.write(data)

print('transform started...')

usage_string = 'Usage: transform_md.py settings_file' 
if len(sys.argv) < 1:
    print(usage_string)
    sys.exit()

settings = json.load(open(sys.argv[1], 'r', encoding='utf-8'))

indir, outdir = get_dirs(settings)

files = transform_files(settings, indir)
fix_all_links(settings, files)
write_files(outdir, files)

print('transform finished')
