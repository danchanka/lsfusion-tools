# Java resource bundle translation tool that uses google translate.

### Preconditions

- python and [google_trans_new](https://pypi.org/project/google-trans-new/) library.

```bash
pip install google_trans_new
```

**Change**: Now it is not enough just to install the library, you must also replace the .py files with files from the https://github.com/lushan88a/google_trans_new repository

- [native2ascii](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/native2ascii.html) tool available from the command line.

### Usage

```bash
translate.py prop_file
```

Source language is taken from a filename. For example in this case

```bash
translate.py resourceBundle_ru.properties
```

`ru` language will be used as from-language.

Output languages can be edited in the source code, in `languages` list.