#!/bin/bash

cd "$(dirname -- "${BASH_SOURCE[0]}")" || exit 1

python3 -m zipapp -o tgui-red -p "/usr/bin/env python3" -c src/

