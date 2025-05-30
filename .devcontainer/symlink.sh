#!/bin/bash
PKGNAME=$(python3 -c 'print(eval(open("package").read())["name"])')

ln -sv $WORKSPACE/package $OMD_ROOT/var/check_mk/packages/$PKGNAME
ln -sv $WORKSPACE $OMD_ROOT/local/lib/python3/cmk_addons/plugins/$PKGNAME

for DIR in 'agents' 'checkman' 'checks' 'doc' 'inventory' 'notifications' 'pnp-templates' 'web'; do
  rm -rfv $OMD_ROOT/local/share/check_mk/$DIR
  ln -sv $WORKSPACE/$DIR $OMD_ROOT/local/share/check_mk/$DIR
done

rm -rfv $OMD_ROOT/local/lib/python3/cmk/base/plugins/agent_based
ln -sv $WORKSPACE/agent_based $OMD_ROOT/local/lib/python3/cmk/base/plugins/agent_based

rm -rfv $OMD_ROOT/local/lib/python3/cmk_addons/plugins
ln -sv $WORKSPACE/plugins $OMD_ROOT/local/lib/python3/cmk_addons/plugins

mkdir -p $OMD_ROOT/local/lib/check_mk/base/cee/plugins
ln -sv $WORKSPACE/lib/base/cee/plugins/bakery $OMD_ROOT/local/lib/check_mk/base/cee/plugins/bakery

rm -rfv $OMD_ROOT/local/lib/nagios/plugins
ln -sv $WORKSPACE/nagios_plugins $OMD_ROOT/local/lib/nagios/plugins

rm -rfv $OMD_ROOT/local/share/check_mk/agents
ln -sv $WORKSPACE/local/share/check_mk/agents $OMD_ROOT/local/share/check_mk/agents
