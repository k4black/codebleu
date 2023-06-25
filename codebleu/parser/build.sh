git clone --depth=1 --single-branch https://github.com/tree-sitter/tree-sitter-go tree-sitter/go
git clone --depth=1 --single-branch https://github.com/tree-sitter/tree-sitter-javascript tree-sitter/javascript
git clone --depth=1 --single-branch https://github.com/tree-sitter/tree-sitter-python tree-sitter/python
git clone --depth=1 --single-branch https://github.com/tree-sitter/tree-sitter-ruby tree-sitter/ruby
git clone --depth=1 --single-branch https://github.com/tree-sitter/tree-sitter-php tree-sitter/php
git clone --depth=1 --single-branch https://github.com/tree-sitter/tree-sitter-java tree-sitter/java
git clone --depth=1 --single-branch https://github.com/tree-sitter/tree-sitter-c-sharp tree-sitter/c-sharp
python build.py
#rm -rf tree-sitter
