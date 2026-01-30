rd mycompany-docs/docs -r >$null
rd mycompany-rudocs/docs -r >$null

yarn --cwd ./confluence-to-markdown start ../MC ../mycompany-docs/docs
yarn --cwd ./confluence-to-markdown start ../MCRU ../mycompany-rudocs/docs

robocopy ./mycompany-docs/docs/MC ./mycompany-docs/docs /e /copyall /move >$null
robocopy ./mycompany-rudocs/docs/MCRU ./mycompany-rudocs/docs /e /copyall /move >$null

python rename_md_files.py mycompany-docs/docs/index.md mycompany-docs/docs/index.md settings_mc.json mycompany-docs/docs/
python rename_md_files.py mycompany-rudocs/docs/index.md mycompany-docs/docs/index.md settings_mc_ru.json mycompany-rudocs/docs/

python build_maps.py settings_mc.json
python build_maps.py settings_mc_ru.json

python find_info_blocks.py settings_mc.json
python find_info_blocks.py settings_mc_ru.json

python transform_md.py settings_mc.json
python transform_md.py settings_mc_ru.json

python create_sidebar.py mycompany-docs/docs/index.md mycompany-docs/sidebars.js settings_mc.json
python create_sidebar.py mycompany-rudocs/docs/index.md mycompany-rudocs/sidebars.js settings_mc_ru.json

rd mycompany-docs/i18n/ru/docusaurus-plugin-content-docs/current -r >$null
robocopy ./mycompany-rudocs/docs/ ./mycompany-docs/i18n/ru/docusaurus-plugin-content-docs/current /e /copyall >$null

python create_i18n_sidebar.py current_mc.json label_map_mc_ru.json current_mc_ru.json
xcopy current_mc_ru.json mycompany-docs\i18n\ru\docusaurus-plugin-content-docs\current.json /Y >$null

del ./mycompany-docs/i18n/ru/docusaurus-plugin-content-docs/current/index.md

# yarn --cwd ./docusaurustest/ start
