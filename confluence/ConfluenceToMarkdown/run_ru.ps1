rd docusaurustestru/docs -r >$null
yarn --cwd ./confluence-to-markdown start ../LSFUSRU ../docusaurustestru/docs
robocopy ./docusaurustestru/docs/LSFUSRU ./docusaurustestru/docs /e /copyall /move >$null
robocopy ./LSFUSRU/download ./docusaurustestru/docs/download /e /copyall >$null
xcopy CodeSample.mdx docusaurustestru\docs /Y >$null

python rename_md_files.py docusaurustestru/docs/index.md docusaurustest/docs/index.md settings_ru.json docusaurustestru/docs/

python build_maps.py settings_ru.json

python find_info_blocks.py settings_ru.json

python transform_md.py settings_ru.json

python create_sidebar.py docusaurustestru/docs/index.md docusaurustestru/sidebars.js settings_ru.json

yarn --cwd ./docusaurustestru/ start

