import re, os, sys

def restore(dir, outdir):
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	for filename in os.listdir(dir): 
		data = ''
		with open(dir + '/' + filename, 'r', encoding='utf-8') as infile:
		    data = infile.read()


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

		with open(outdir + '/' + filename, 'w', encoding='utf-8') as outfile:
			outfile.write(data)


def main(argv):
	restore(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
   main(sys.argv[1:])	