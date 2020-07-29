from googletrans import Translator
import sys
import os
translator = Translator()

def batchTranslate(outf, lines, src_lang, dest_lang):
    keys = []
    isupper = []
    value = ""
    for line in lines:
        a = line.strip().split('=', 1)
        if len(a) > 1 and line[0] != '#':
            keys.append(a[0])
            isupper.append(a[1].strip()[0].isupper())
            value += a[1].strip() + '\n'

    if len(value) > 0:    
        translated = translator.translate(value, src=src_lang, dest=dest_lang)
        values = translated.text.split('\n')
        
        for i in range(len(keys)):
            if isupper[i] and not values[i][0].isupper():
                values[i] = values[i][0].upper() + values[i][1:]
            outf.write(keys[i] + '= ' + values[i] + '\n')

def get_input_language(filename):
    und_index = filename.rfind('_')
    if und_index < 0:
        return 'en'
    else:
        return filename[und_index+1:]    

def get_filename(fullfilename):
    dot_index = fullfilename.rfind('.')
    if dot_index < 0:
        return fullfilename
    else:
        return fullfilename[0:dot_index]    

def get_bundle_name(filename):
    und_index = filename.rfind('_')
    if und_index < 0:
        return filename
    else:
        return filename[0:und_index]    

if len(sys.argv) < 2:
	print('Usage: translate.py prop_file\nBase language is taken from prop_file name, output languages can be edited in the source code.')
	sys.exit() 

full_filename = sys.argv[1]
filename = get_filename(full_filename)
bundle_name = get_bundle_name(filename)
input_lang = get_input_language(filename)

full_filename_utf8 = full_filename + '_u'
os.system('native2ascii -reverse -encoding utf-8 {} > {}'.format(full_filename, full_filename_utf8))
inf = open(full_filename_utf8, 'r', encoding='utf-8')
lines = inf.readlines()

languages = ['uk', 'be']
for lang in languages:
    out_filename_utf8 = bundle_name + '_' + lang + '.properties_u'
    outf = open(out_filename_utf8, 'w', encoding='utf-8')

    cur = 0
    batch_size = 25
    while cur < len(lines):
        last = cur + batch_size
        if cur + batch_size >= len(lines):
            last = len(lines)
        batchTranslate(outf, lines[cur:last], input_lang, lang)
        cur = last

    outf.close()    
    out_filename = bundle_name + '_' + lang + '.properties'
    os.system('native2ascii -encoding utf-8 {} > {}'.format(out_filename_utf8, out_filename))
    print('{} language file is generated'.format(lang))
    os.remove(out_filename_utf8)

inf.close()    
os.remove(full_filename_utf8)