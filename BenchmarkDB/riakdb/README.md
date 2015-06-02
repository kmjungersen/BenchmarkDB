# Riak 1.x

There are a few quick changes to make here before deployment:

1. Be sure to edit `ansible/hosts` according to the IP addresses needed.  The values they default to are the IP's specified in the `Vagrantfile`.
2. Make those same changes in `local.py`, so that the python client can connect to it. 