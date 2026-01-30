rd docusaurustestru/docs -r >$null
robocopy ./pureru/LSFUSRU ./docusaurustestru/docs /e /copyall >$null
robocopy ./LSFUSRU/download ./docusaurustestru/docs/download /e /copyall >$null
xcopy CodeSample.mdx docusaurustestru\docs /Y >$null

python transform_md.py settings_ru.json

python create_sidebar.py docusaurustestru/docs/index.md docusaurustestru/sidebars.js settings_ru.json

yarn --cwd ./docusaurustestru/ start

