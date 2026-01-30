rd docusaurustest/docs -r >$null
yarn --cwd ./confluence-to-markdown start ../LSFUS ../docusaurustest/docs
robocopy ./docusaurustest/docs/LSFUS ./docusaurustest/docs /e /copyall /move >$null
robocopy ./LSFUS/download ./docusaurustest/docs/download /e /copyall >$null
xcopy CodeSample.mdx docusaurustest\docs /Y >$null

python rename_md_files.py docusaurustest/docs/index.md docusaurustest/docs/index.md settings.json docusaurustest/docs/

python build_maps.py settings.json

python find_info_blocks.py settings.json

python transform_md.py settings.json

python create_sidebar.py docusaurustest/docs/index.md docusaurustest/sidebars.js settings.json

yarn --cwd ./docusaurustest/ start

