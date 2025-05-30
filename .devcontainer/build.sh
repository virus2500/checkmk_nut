#!/bin/bash
set -e

export OMD_ROOT="/omd/sites/cmk"

NAME=$(python -c 'import ast; print(ast.literal_eval(open("package").read())["name"])')
echo $NAME
rm /omd/sites/cmk/var/check_mk/packages/* || true
ln -s "$WORKSPACE/package" "$OMD_ROOT/var/check_mk/packages/$NAME"

mkp -v package "$OMD_ROOT/var/check_mk/packages/$NAME"

if [ -n "$GITHUB_OUTPUT" ]; then
  VERSION=$(python -c 'import ast; print(ast.literal_eval(open("package").read())["version"])')
  cp /opt/omd/sites/cmk/var/check_mk/packages_local/$NAME\-$VERSION.mkp .
  PKGFILE=$(ls *.mkp 2>/dev/null || true)

  {
    echo "pkgfile=$PKGFILE"
    echo "pkgname=$NAME"
    echo "pkgversion=$VERSION"
  } >>"$GITHUB_OUTPUT"
fi
