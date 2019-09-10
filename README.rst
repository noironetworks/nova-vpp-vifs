# nova-vpp-vifs
Python library for VPP VIF plugging in Nova.
Two ways of using this plugin code
1.Dummy nova firewall as a means of monkey patching os-vif
modules to include vpp vif driver.
To use:
set "firewall_driver=nova_vpp_vif.vpp_plug_firewall.NoopFirewallDriver"
in /etc/nova/nova.conf on the compute node where vpp datpath is intended
to be used.
2:use nova monkey_patch feature:
In nova.conf:
monkey_patch=True
monkey_patch_modules=nova_vpp_vifs.patch_nova:nova_vpp_vifs.patch_nova.dummy_decorator
