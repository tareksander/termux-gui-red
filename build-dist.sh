#!/bin/bash

cd "$(dirname -- "${BASH_SOURCE[0]}")" || exit 1

rm -rf build termux-gui-python-bindings

git clone https://github.com/tareksander/termux-gui-python-bindings.git
(cd termux-gui-python-bindings || exit 1; python3 -m build)
cp -r src build

python3 -m pip install --target build requests praw termux-gui-python-bindings/dist/*.whl

rm -rf build/*.dist-info build/bin build/__pycache__

python3 -m zipapp -o tgui-red -p "/usr/bin/env python3" -c build/

