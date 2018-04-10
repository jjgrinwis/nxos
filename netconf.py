from ncclient import manager
import jinja2

# lets try and build a netconf ssh connection
with manager.connect_ssh(device, username="cisco", password='cisco', hostkey_verify=False, port=22) as m:
    # now make sure this device is doing netconf :validate should be in response
    assert (":validate" in m.server_capabilities)

    # build our new config using jinja template
    for i in range(1, 10):

        context = {
            'id': i,
            'description': 'klant {0}'.format(i)
        }

        evpnconfig = render('templates/l2vpn.jinja', context)
        print(evpnconfig)

        # now send our config via edit_config netconf call and commit() our new config
        m.edit_config(target='candidate', config=evpnconfig, test_option='test-then-set')
        m.commit()