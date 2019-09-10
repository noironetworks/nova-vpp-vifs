# nova-vpp-vifs
Python library for VPP VIF plugging in NOva
Dummy nova firewall as a means of monkey patching os-vif
modules to include vpp vif driver.
To use:
set "firewall_driver=nova_vpp_vif.vpp_plug_firewall.NoopFirewallDriver"
in /etc/nova/nova.conf on the compute node where vpp datpath is intended
to be used.
