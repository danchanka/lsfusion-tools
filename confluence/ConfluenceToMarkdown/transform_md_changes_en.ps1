rd docusaurustest/docs -r >$null
robocopy ./pure/LSFUS ./docusaurustest/docs /e /copyall >$null
robocopy ./LSFUS/download ./docusaurustest/docs/download /e /copyall >$null
xcopy CodeSample.mdx docusaurustest\docs /Y >$null

python transform_md.py settings.json

python create_sidebar.py docusaurustest/docs/index.md docusaurustest/sidebars.js settings.json

yarn --cwd ./docusaurustest/ start

