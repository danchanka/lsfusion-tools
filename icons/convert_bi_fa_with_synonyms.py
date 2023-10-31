import json, sys, os, re

def read_synonyms(filename):
    f = open(filename)

    out_dict = {}
    for line in f:
        d = json.loads(line)
        word = d['word']
        syn_list = d['synonyms']
        synonyms = out_dict.get(word, set())
        synonyms.update(syn_list)
        out_dict[word] = synonyms

    return {word : sorted(synonyms) for word, synonyms in out_dict.items()}


def add_synonyms(word, synonyms, out_list):
    out_list.extend(synonyms.get(word.lower(), []))    

def all_synonyms(label, terms, synonyms):
    out_list = []
    add_synonyms(label, synonyms, out_list)
    for term in terms:
        add_synonyms(term, synonyms, out_list)
    return out_list    

def read_bi_icons(directory):
    icons_dict = {}

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            lines = open(filepath, 'r').readlines()
            name = filename[:-3]
            title = lines[1][len('title: '):].strip()
            terms_index = lines.index('tags:\n')
            terms = [line.strip()[2:] for line in lines[terms_index+1:-1]]
            icons_dict[name] = (title, terms)

    return icons_dict        

def fa_icons(synonyms):
    fa_icons = json.load(open('fontawesome_icons6_4.json', 'r'))
    out_list = []
    for name, info in fa_icons.items():
        if 'search' in info:
            label = info['label']
            terms = info['search']['terms']
            if label.lower() in terms:
                terms.remove(label.lower())
            free = info['free']
            icon_synonyms = all_synonyms(label, terms, synonyms)
            out_list.append({'name': name, 'label': label, 'terms': terms, 'synonyms': icon_synonyms, 'free': free})    
    return out_list


def bi_icons(synonyms):
    bi_icons = read_bi_icons('D:/icons-1.10.3/docs/content/icons')
    out_list = []
    for name, (title, terms) in bi_icons.items():
        if title.lower() in terms:
            terms.remove(title.lower())
        icon_synonyms = all_synonyms(title, terms, synonyms)
        out_list.append({'name': name, 'label': title, 'terms': terms, 'synonyms': icon_synonyms, 'free': ["bi"]})    
    return out_list

def filter_result(res_list):
    for icon in res_list:
        label_parts = icon['label'].lower().split(' ')
        splitted_terms = []
        for term in icon['terms']:
            splitted_terms.extend(term.lower().split(' ')) 

        terms_changed = False    
        for part in label_parts:
            if part in splitted_terms:
                splitted_terms.remove(part)
                terms_changed = True
                
        if terms_changed:
            icon['terms'] = splitted_terms        

def main():
    synonyms = read_synonyms('en_thesaurus.jsonl')
    out_list = fa_icons(synonyms)
    print('---------------')
    out_list.extend(bi_icons(synonyms))
    filter_result(out_list)

    with open("icons_with_synonyms.json", "w") as outfile:
        json.dump(out_list, outfile, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()