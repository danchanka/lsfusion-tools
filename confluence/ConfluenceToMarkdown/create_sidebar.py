import sys, re, os, json

def depth(s):
    return len(s) - len(s.lstrip())

def label(s):
    return re.search(r"\[(.*[^\\])\]", s).group(1)

def name(s):
    return re.search(r"\]\((.*\.md)\)", s).group(1)

def printsp(text, d, outfile):
    outfile.write(' ' * (d + 4) + text + '\n')

def open_category(line, d, outfile):
    printsp('{', d, outfile)    
    printsp('type: \'category\',', d+2, outfile)
    printsp(f'label: \'{label(line)}\',', d+2, outfile)
    printsp('items: [', d+2, outfile)

def close_category(d, outfile):
    printsp(']', d+2, outfile)
    printsp('},', d, outfile)

# def print_leaf(line, d, outfile):
#     printsp('{', d, outfile)    
#     printsp('type: \'doc\',', d+2, outfile)
#     printsp(f'id: \'LSFUS/{name(line)}\',', d+2, outfile)
#     printsp('},', d, outfile)

def print_leaf(line, d, md_map, outfile):
    printsp(f'\'{md_map[name(line)][:-3]}\', ', d, outfile)

def build_sidebar(lines, outfile, md_map):
    category_list = []
    stack = []
    for i, line in enumerate(lines):
        d = depth(line)
        if i + 1 != len(lines) and depth(line) < depth(lines[i+1]):
            open_category(line, d, outfile)
            category_list.append(md_map[name(line)])
            print_leaf(line, d+4, md_map, outfile)
            stack.append(line)
        else:         
            print_leaf(line, d, md_map, outfile)
            if i+1 == len(lines) or depth(line) > depth(lines[i+1]):
                nextd = -1 if i+1 == len(lines) else depth(lines[i+1])
                while stack and depth(stack[-1]) >= nextd:
                    close_category(depth(stack[-1]), outfile)        
                    stack.pop()
    return category_list                


if len(sys.argv) < 4:
    print('Usage: create_sidebar.py path_to_index_md path_to_sidebars.js settings.json');
    sys.exit()

with open(sys.argv[1], 'r', encoding='utf-8') as infile:
    lines = [line.rstrip() for line in infile.readlines() if re.fullmatch(r'\s*-[^-].*\n', line)]
    settings = json.load(open(sys.argv[3], 'r', encoding='utf-8'))
    md_map = json.load(open(settings['mdmap'], 'r', encoding='utf-8'))
    # print('\n'.join(lines))
    with open(sys.argv[2], 'w', encoding='utf-8') as outfile:
        outfile.write('module.exports = {\n  docs: [\n')
        category_list = build_sidebar(lines, outfile, md_map)
        outfile.write('  ]\n};\n')
        outfile.close()

    json.dump(category_list, open(settings['category_list'], 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
     
