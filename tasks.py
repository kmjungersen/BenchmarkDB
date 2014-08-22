"""
DB Benchmarking Application
===========================

Tasks.py

This file houses all of the invoke commands for the application.  This makes it
very easy for a user to quickly bring up the necessary vagrant boxes for a module
and then perform benchmarks with that module.

    Usage:
        invoke <command> [args]

"""

from invoke import task, run

#TODO - make a docs directory


def check_module_naming(name):
    """ Checks to see if the inputted name is in the proper format, and fixes
     it if not before returning it

    :return name: The properly formatted DB module name
    """

    if not name.endswith('db'):
        name += 'db'

    return name


@task
def help():
    """ Returns some basic task information, much of which provided by invoke """

    run('invoke -l')


@task
def list_mods():
    """ Returns a list of existing modules """

    from main import retrieve_module_list

    mod_list = retrieve_module_list()

    print mod_list


@task
def benchmark(database):
    """ Executes benchmarks with the default settings for a given DB
    Usage: `invoke benchmark <database> """

    database = check_module_naming(database)

    run("python main.py {db}".format(db=database))


@task
def vagrant_up(module):
    """ Runs `vagrant up` for the specified module """

    module = check_module_naming(module)

    run("cd {mod}/ansible && vagrant up".format(mod=module))


@task
def install_ssh_copy_id():
    """ Installs ssh_copy_id for mac """

    run("curl -L https://raw.githubusercontent.com/beautifulcode/"
        "ssh-copy-id-for-OSX/master/install.sh | sh")


@task
def deploy(database):
    """ Runs the ansible playbook for a given db """

    database = check_module_naming(database)

    run('cd {db}/ansible && ansible-playbook -u vagrant -i hosts -s'
        ' site.yml -vv'.format(db=database))