import os
import sys
import importlib

from invoke import task, run

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')


@task
def docs(clean=False, browse=False):
    if clean:
        clean_docs()
    run("sphinx-build {0} {1}".format(docs_dir, build_dir), pty=True)
    if browse:
        browse_docs()

@task
def browse_docs():
    run("open {}".format(os.path.join(build_dir, 'index.html')))

@task
def clean_docs():
    run("rm -rf {dir}".format(dir=build_dir))

@task
def list_mods():
    from main import retrieve_module_list

    mod_list = retrieve_module_list()

    print mod_list

#TODO - add tasks for running ansible playbooks from invoke