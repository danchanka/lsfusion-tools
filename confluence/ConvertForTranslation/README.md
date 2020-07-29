Converts/restores Confluence files (a directory with a single html file for every Confluence page) to/from the files where <ac:link> tags are replaced with <a href...> tags.

Example of usage:
convert.py source_dir converted_dir
translate resulting htmls
restore.py converted_dir result_dir 