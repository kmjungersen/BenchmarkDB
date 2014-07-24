# DB-Benchmarking

## Installing separate DB's:

Each DB had two instances installed, each of which on a separate vagrant environment.

### Mongo

1. Import the public key used by the package management system:

    `$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10`

2. Create a list file for MongoDB:

    `$ echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list`

3. Reload local package DB

    `$ sudo apt-get update`
on
4. Install Mongo:

    `sudo apt-get install mongodb-org`

5. Fire it up!

    `$ sudo service mongod start`

    Or you can also "stop" and "restart" with the same syntax

