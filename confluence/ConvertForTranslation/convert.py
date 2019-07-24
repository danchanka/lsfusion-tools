import re, os, sys

def convert(dir, outdir):
	if not os.path.exists(outdir):
		os.makedirs(outdir)
		
	for filename in os.listdir(dir): 
		data = ''
		with open(dir + '/' + filename, 'r', encoding='utf-8') as infile:
		    data = infile.read()

		data = re.sub(r'<ac:link><ri:page ri:content-title="(.*?)" /></ac:link>', 
			r'<a href="\1">\1</a>', data)

		data = re.sub(r'<ac:link><ri:page ri:space-key="LSFUS" ri:content-title="(.*?)" /></ac:link>', 
			r'<a href="\1__LSFUS">\1</a>', data)

		data = re.sub(r'<ac:link><ri:page ri:content-title="(.*?)" /><ac:plain-text-link-body><!\[CDATA\[(.*?)\]\]></ac:plain-text-link-body></ac:link>', 
			r'<a href="\1__DATA">\2</a>', data)

		data = re.sub(r'<ac:link><ri:page ri:space-key="LSFUS" ri:content-title="(.*?)" /><ac:plain-text-link-body><!\[CDATA\[(.*?)\]\]></ac:plain-text-link-body></ac:link>', 
			r'<a href="\1__LSFUS__DATA">\2</a>', data)

		data = re.sub(r'<ac:link><ri:page ri:content-title="(.*?)" /><ac:link-body>(.*?)</ac:link-body></ac:link>', 
			r'<a href="\1__BODY">\2</a>', data)



		data = re.sub(r'<ac:link ac:anchor="(.*?)"><ac:plain-text-link-body><!\[CDATA\[(.*?)\]\]></ac:plain-text-link-body></ac:link>', 
			r'<a href="#\1__DATA">\2</a>', data)

		data = re.sub(r'<ac:link ac:anchor="(.*?)"><ri:page ri:content-title="(.*?)" /><ac:plain-text-link-body><!\[CDATA\[(.*?)\]\]></ac:plain-text-link-body></ac:link>', 
			r'<a href="\2#\1__DATA">\3</a>', data)

		data = re.sub(r'<ac:link ac:anchor="(.*?)"><ri:page ri:content-title="(.*?)" /><ac:link-body>(.*?)</ac:link-body></ac:link>', 
			r'<a href="\2#\1__BODY">\3</a>', data)

		with open(outdir + '/' + filename, 'w', encoding='utf-8') as outfile:
			outfile.write(data)


def main(argv):
	convert(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
   main(sys.argv[1:])	