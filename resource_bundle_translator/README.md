# Java resource bundle translation tool that uses google translate.

### Preconditions

- python and [googletrans](https://py-googletrans.readthedocs.io/en/latest/) library.

```bash
pip install googletrans
```

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