rd docusaurustest/docs -r >$null
rd docusaurustestru/docs -r >$null

yarn --cwd ./confluence-to-markdown start ../LSFUS ../docusaurustest/docs
yarn --cwd ./confluence-to-markdown start ../LSFUSRU ../docusaurustestru/docs

robocopy ./docusaurustest/docs/LSFUS ./docusaurustest/docs /e /copyall /move >$null
robocopy ./LSFUS/download ./docusaurustest/docs/download /e /copyall >$null

robocopy ./docusaurustestru/docs/LSFUSRU ./docusaurustestru/docs /e /copyall /move >$null
robocopy ./LSFUSRU/download ./docusaurustestru/docs/download /e /copyall >$null

python rename_md_files.py docusaurustest/docs/index.md docusaurustest/docs/index.md settings.json docusaurustest/docs/
python rename_md_files.py docusaurustestru/docs/index.md docusaurustest/docs/index.md settings_ru.json docusaurustestru/docs/

python build_maps.py settings.json
python build_maps.py settings_ru.json

python find_info_blocks.py settings.json
python find_info_blocks.py settings_ru.json

python transform_md.py settings.json
python transform_md.py settings_ru.json

python create_sidebar.py docusaurustest/docs/index.md docusaurustest/sidebars.js settings.json
python create_sidebar.py docusaurustestru/docs/index.md docusaurustestru/sidebars.js settings_ru.json

rd docusaurustest/i18n/ru/docusaurus-plugin-content-docs/current -r >$null
robocopy ./docusaurustestru/docs/ ./docusaurustest/i18n/ru/docusaurus-plugin-content-docs/current /e /copyall >$null

python create_i18n_sidebar.py current.json label_map_ru.json current_ru.json
xcopy current_ru.json docusaurustest\i18n\ru\docusaurus-plugin-content-docs\current.json /Y >$null

del ./docusaurustest/i18n/ru/docusaurus-plugin-content-docs/current/index.md

yarn --cwd ./docusaurustest/ start
