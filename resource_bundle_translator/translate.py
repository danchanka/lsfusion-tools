from google_trans_new import google_translator  
import sys
import os
import time
import re
import subprocess

def batchTranslate(outf, translator, properties, src_lang, dest_lang):
    separator = '\n+++\n'
    keys = []
    isupper = []
    values = []
    print(len(properties))

    for prop in properties:
        a = prop.strip().split('=', 1)
        if len(a) > 1:
            keys.append(a[0])
            isupper.append(a[1].strip()[0].isupper())
            values.append(a[1].strip()) 

    value = separator.join(values)

    if value:
        translated = translator.translate(value, lang_src=src_lang, lang_tgt=dest_lang)
        has_line_breaks = '\n' in translated

        if has_line_breaks:
            translated_values = translated.split(separator)
        else:
            translated_values = translated.split(f'  {separator.strip()}  ')

        for i, tvalue in enumerate(translated_values):
            if isupper[i] and not tvalue[0].isupper():
                tvalue = tvalue[0].upper() + tvalue[1:]
            tvalue = tvalue.strip()
            if has_line_breaks:
                tvalue = '\\\n'.join(tvalue.split('\n'))
            else:
                tvalue = '\\\n'.join(tvalue.split('  '))        
            outf.write(f'{keys[i]}= {tvalue}\n')

def get_input_language(filename):
    und_index = filename.rfind('_')
    return filename[und_index+1:] if und_index >= 0 else 'en'

def get_filename(fullfilename):
    dot_index = fullfilename.rfind('.')
    return fullfilename[:dot_index] if dot_index >= 0 else fullfilename

def get_bundle_name(filename):
    und_index = filename.rfind('_')
    return filename[:und_index] if und_index >= 0 else filename

def add_property(properties, property):
    if property:
        properties.append(property)
    return ''    

def ends_with_backslash(s):
    return s.rstrip().endswith('\\')

def get_properties(lines):
    properties = []
    cur_property = ''

    for line in lines:
        if re.match(r'^[a-zA-Z0-9_.]+\s*=', line) or cur_property:
            cur_property += line
            if not ends_with_backslash(line):
                cur_property = add_property(properties, cur_property)
            else:
                slash_index = cur_property.rfind('\\')
                cur_property = cur_property[:slash_index] + cur_property[slash_index+1:]    

    return properties

def main():
    if len(sys.argv) < 2:
        print('Usage: translate.py prop_file\nBase language is taken from prop_file name, output languages can be edited in the source code.')
        sys.exit() 

    full_filename = sys.argv[1]
    filename = get_filename(full_filename)
    bundle_name = get_bundle_name(filename)
    input_lang = get_input_language(filename)

    full_filename_utf8 = full_filename + '_u'
    subprocess.run(f'native2ascii.exe -reverse -encoding utf-8 {full_filename} {full_filename_utf8}', shell=True)
    inf = open(full_filename_utf8, 'r', encoding='utf-8')

    translator = google_translator()

    properties = get_properties(inf.readlines())
    languages = ['uk']
    for lang in languages:
        out_filename_utf8 = f'{bundle_name}_{lang}.properties_u'
        with open(out_filename_utf8, 'w', encoding='utf-8') as outf:
            cur = 0
            batch_size = 20

            while cur < len(properties):
                last = min(cur + batch_size, len(properties))
                try:    
                    batchTranslate(outf, translator, properties[cur:last], input_lang, lang)
                    cur = last
                except Exception as e:
                    print(f'error!: {e}')

        out_filename = f'{bundle_name}_{lang}.properties'
        subprocess.run(f'native2ascii -encoding utf-8 {out_filename_utf8} > {out_filename}', shell=True)
        print(f'{lang} language file is generated')
        os.remove(out_filename_utf8)

    inf.close()    
    os.remove(full_filename_utf8)

if __name__ == "__main__":
    main()
