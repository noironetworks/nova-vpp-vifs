#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import functools
from os_vif import objects
from oslo_log import log as logging

from nova.network import model
import nova.network.os_vif_util as os_vif_util

LOG = logging.getLogger(__name__)

if not hasattr(os_vif_util._nova_to_osvif_vif_vhostuser, 'NOVA_VPP_VIFS_ADDED'):
def wrap_nova_to_osvif_vif_vhostuser(fn):
    @functools.wraps(fn)
    def vpp_nova_to_osvif_vif_vhostuser(vif):
        try:
            vif_obj = fn(vif)
        except NotImplementedError as e:
            if vif['details'].get("vhostuser_vpp_plug", False):
                profile = objects.vif.VIFPortProfileOpenVSwitch(
                    interface_id=vif.get('ovs_interfaceid') or vif['id'],
                    datapath_type=model.VIF_DETAILS_OVS_DATAPATH_NETDEV)
                obj = os_vif_util._get_vif_instance(
                        vif, objects.vif.VIFVHostUser,
                        port_profile=profile, plugin="vpp",
                        vif_name=('vhu' + vif['id'])[:model.NIC_NAME_LEN])
                os_vif_util._set_vhostuser_settings(vif, obj)
                return obj
            else:
                raise e
        else:
            return vif_obj
    return vpp_nova_to_osvif_vif_vhostuser
os_vif_util._nova_to_osvif_vif_vhostuser = (
    wrap_nova_to_osvif_vif_vhostuser(
	os_vif_util._nova_to_osvif_vif_vhostuser))
LOG.debug("Successfully patched "
    "os_vif_util._nova_to_osvif_vif_vhostuser")
setattr(os_vif_util._nova_to_osvif_vif_vhostuser, 'NOVA_VPP_VIFS_ADDED', True)

def dummy_decorator(name, fn):
    """Dummy decorator which is used from utils.monkey_patch().

        :param name: name of the function
        :param fn: - object of the function
        :returns: fn -- decorated function

    """
    def wrapped_func(*args, **kwarg):
        return fn(*args, **kwarg)
    return wrapped_func


class DummyClass(object):
    """Dummy class used as a means of patching nova's neutron API
     code.
     """

    def __init__(self, *args, **kwargs):
        pass

    def dummy_method(self, *args, **kwargs):
        pass
