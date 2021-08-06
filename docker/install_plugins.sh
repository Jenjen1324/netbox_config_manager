#!/usr/bin/env -S bash -euET -o pipefail -O inherit_errexit

echo "Setting up custom plugins..."
for plugin_dir in ./plugins/* ; do
  if [ -d $plugin_dir ]; then
    echo "Setting up $plugin_dir"
    # Opening a subshell to preserve directory
    (cd $plugin_dir && pip install -e .)
  fi
done