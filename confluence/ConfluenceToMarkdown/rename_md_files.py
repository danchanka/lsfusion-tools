import sys, re, os, json

def label(s):
    return re.search(r"\[(.*[^\\])\]", s).group(1)

def name(s):
    return re.search(r"\]\((.*\.md)\)", s).group(1)

def get_files_and_labels(f):
    lines = f.readlines()
    files = [name(line) for line in lines if re.fullmatch(r'\s*-[^-].*\n', line)] 
    labels = [label(line) for line in lines if re.fullmatch(r'\s*-[^-].*\n', line)]
    return files, labels

def get_label_names(f):
    return [label(line) for line in f.readlines() if re.fullmatch(r'\s*-[^-].*\n', line)]

print('renaming md files...')

ifile1 = open(sys.argv[1], 'r', encoding='utf-8')
ifile2 = open(sys.argv[2], 'r', encoding='utf-8')
settings = json.load(open(sys.argv[3], 'r', encoding='utf-8'))

files1, labels1 = get_files_and_labels(ifile1)
files2, labels2 = get_files_and_labels(ifile2)

if (len(files1) != len(files2)):
    print('Error: number of lines doesn''t match')
    sys.exit()

md_map = {}
label_map = {}
input_dir = sys.argv[4]

for index, filename in enumerate(files1):
    md_map[filename] = files2[index]
    label_map[labels2[index]] = labels1[index]
    if filename != md_map[filename]:
        os.rename(input_dir + filename, input_dir + md_map[filename])

json.dump(md_map, open(settings['mdmap'], 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
json.dump(label_map, open(settings['labelmap'], 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

print('end of renaming md files')