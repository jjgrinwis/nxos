import yaml
import evpn
from ncclient import manager
from create_config import create_config

# first get data from yaml file.
with open('data.yaml', 'r') as yaml_file:
    try:
        data = (yaml.load(yaml_file))
    except yaml.YAMLError as exc:
        print(exc)

for device in data['devices']:
    print "configuring device {}".format(device)

    # connect to networ device
    with manager.connect_ssh(device, username="cisco", password='cisco', hostkey_verify=False, port=22) as m:
        # now make sure this device is doing netconf :validate should be in response
        assert (":validate" in m.server_capabilities)

        for customer in data['customers']:

            # create customized customer config
            context = evpn.create_evpn_vars(customer)

            # let's create unique MAC for anycast L3 GW
            context['mac'] = "{}:{}".format(data['base_mac'], evpn.create_mac(customer['evi']))

            # send our create dict to our jinja template
            evpn_config = create_config('templates', 'evpn-bvi.jinja2', context)

            # now configure our devices using netconf and our create XML config via jija template
            m.edit_config(target='candidate', config=evpn_config, test_option='test-then-set')

        print "now trying to commit config on devce {}".format(device)
        m.commit()

print "that's all folks"