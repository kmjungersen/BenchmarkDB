# Riak 2.0

There are a few quick changes to make here before deployment:

1. Be sure to edit `ansible/hosts` according to the IP addresses needed.  The values they default to are the IP's specified in the `Vagrantfile`.
2. Make those same changes in `local.py`, so that the python client can connect to it.  
3. Edit `ansible/group_vars/all` to reflect your desired settings.  The primary node must be set properly for the cluster to function, here we can also [enable strong consistency](http://basho.com/introducing-riak-2-0/).

