Language definition for highlight.js

1. Pull request (https://highlightjs.readthedocs.io/en/latest/language-contribution.html)
- add or change language definition in src/languages/lsfusion.js
- add or change code example in test/detect/lsfusion/default.txt
- add yourself to AUTHORS.*.txt and CHANGES.md

Building and testing before pull request (https://highlightjs.readthedocs.io/en/latest/building-testing.html#basic-testing)
- install node.js, don't forget to run 'nmp install' to install packages. 
- build a specific language:

  > node tools/build.js --no-compress lsfusion  

Then you can use tools/developer.html (or build/demo/index.html) to see how this build highlights a test sample. 
Then you need to test language auto detection. Build the package with all languages: 

  > node tools/build.js --target node

Go to test/ directory.

  > npm install
  > npm test


2. Usage of the package. 
- build a package as described above

  > node tools/build.js lsfusion java    

- find highlight.pack.js in the build/ directory
- find a sample usage at the demo/ directory   