import re, os, sys

def restore_aclink(data):
	data = re.sub(r'<a href="(?!http)([^"]+?)#([^"]*?)__BODY">(.*?)</a>', 
		r'<ac:link ac:anchor="\2"><ri:page ri:content-title="\1" /><ac:link-body>\3</ac:link-body></ac:link>', data) 

	data = re.sub(r'<a href="(?!http)([^"]+?)#([^"]*?)__DATA">(.*?)</a>', 
		r'<ac:link ac:anchor="\2"><ri:page ri:content-title="\1" /><ac:plain-text-link-body><![CDATA[\3]]></ac:plain-text-link-body></ac:link>', data) 

	data = re.sub(r'<a href="#([^"]*?)__DATA">(.*?)</a>', 
		r'<ac:link ac:anchor="\1"><ac:plain-text-link-body><![CDATA[\2]]></ac:plain-text-link-body></ac:link>', data) 

	data = re.sub(r'<a href="(?!http)([^"]+?)__BODY">(.*?)</a>', 
		r'<ac:link><ri:page ri:content-title="\1" /><ac:link-body>\2</ac:link-body></ac:link>', data)	

	data = re.sub(r'<a href="(?!http)([^"]+?)__LSFUS__DATA">(.*?)</a>', 
		r'<ac:link><ri:page ri:space-key="LSFUS" ri:content-title="\1" /><ac:plain-text-link-body><![CDATA[\2]]></ac:plain-text-link-body></ac:link>', data)	

	data = re.sub(r'<a href="(?!http)([^"]+?)__DATA">(.*?)</a>', 
		r'<ac:link><ri:page ri:content-title="\1" /><ac:plain-text-link-body><![CDATA[\2]]></ac:plain-text-link-body></ac:link>', data)	

	data = re.sub(r'<a href="(?!http)([^"]+?)__LSFUS">(.*?)</a>', 
		r'<ac:link><ri:page ri:space-key="LSFUS" ri:content-title="\1" /></ac:link>', data)	

	data = re.sub(r'<a href="(?!http)([^"]+?)">(.*?)</a>', 
		r'<ac:link><ri:page ri:content-title="\1" /></ac:link>', data)	

	return data	

def fix_nbsp(data):
	return re.sub(r'&nbsp([^;])', r'&nbsp;\1', data) 

def fix_newlines_in_codeblock(data):
	pos = 0
	out_data = ''
	find_pos = re.search(r'<ac:plain-text-body><!\[CDATA\[((?!<\/ac:plain-text-body>).)*\\n.*<\/ac:plain-text-body>', data[pos:])
	while find_pos is not None:
		prefix = '<ac:plain-text-body><![CDATA['
		next_start_pos = pos + find_pos.start() 	
		out_data += data[pos:next_start_pos]
		out_data += prefix
		pos = next_start_pos + len(prefix)
		opened = 1
		while opened > 0:
			if data[pos] == '[':
				opened += 1
			elif data[pos] == ']':
				opened -= 1

			if data[pos] == '\\' and data[pos+1] == 'n':
				out_data += '\n'
				pos += 1
			else:
				out_data += data[pos]			
			pos += 1

		find_pos = re.search(r'<ac:plain-text-body><!\[CDATA\[((?!<\/ac:plain-text-body>).)*\\n.*<\/ac:plain-text-body>', data[pos:])

	out_data += data[pos:]
	return out_data

def restore(dir, outdir):
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	for filename in os.listdir(dir): 
		data = ''
		with open(dir + '/' + filename, 'r', encoding='utf-8') as infile:
		    data = infile.read()
		    data = restore_aclink(data)	
		    data = fix_nbsp(data)
		    data = fix_newlines_in_codeblock(data)	

		with open(outdir + '/' + filename, 'w', encoding='utf-8') as outfile:
			outfile.write(data)


def main(argv):
	restore(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
   main(sys.argv[1:])	