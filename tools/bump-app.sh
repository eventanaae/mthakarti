#!/bin/sh
# After editing app.js, run this so browsers fetch the new version (cache-busting hash in index.html).
cd "$(dirname "$0")/.." && h=$(sha1sum app.js | cut -c1-10) && sed -i "s#/app.js?v=[0-9a-f]*#/app.js?v=$h#" index.html && echo "app.js?v=$h"
