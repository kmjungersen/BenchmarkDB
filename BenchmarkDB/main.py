"""
DB Benchmarking Application
===========================

Main.py

This file houses the core of the application, and is where all of the
read/write commands are issued from, timed, and all data is analyzed.  Results
from the trials are printed to the console by default, and are also printed to
a markdown file to keep a record of.

    Usage:
        main.py <database> [options]
        main.py --debug [options]
        main.py --list
        main.py <database> <report_title> [options]

    Options:
        -h --help           Show this help screen
        -v                  Show verbose output from the application
        -V                  Show REALLY verbose output, including the time
                                from each run
        -s                  Sleep mode (experimental) - sleeps for 1/20 (s)
                                between each read and write
        -r --random         Activates random mode, where reads are taken
                                randomly from the DB instead of sequentially
        -l --list           Outputs a list of available DB modules
        --no-csv            App will not generate a CSV file with the raw data
        --no-report         Option to disable the creation of the report file
        --no-split          Alternate between reads and writes instead of all
                                writes before reads
        --debug             Generates a random dataset instead of actually
                                connecting to a DB
        --length=<n>        Specify an entry length for reads/writes
                                [default: 10]
        --trials=<n>        Specify the number of reads and writes to make to
                                the DB to collect data on [default: 1000]
"""

from __future__ import absolute_import
from __future__ import print_function

import os
import time
import string
import random
import importlib
import pylab
import ipdb
import seaborn
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from os import getcwd, listdir, makedirs
from sys import exit
from tabulate import tabulate
from docopt import docopt
from clint.textui import progress
import six


def retrieve_module_list():
    """ This function will retrieve a list of all available modules in the
    project directory and then return said list.

    :return list mod_list: The list of modules in the project directory
    """

    current_dir = getcwd()
    mod_list = []

    for item in listdir(current_dir):

        if item.endswith('db'):

            mod_list.append(item)

    return mod_list


class Benchmark():
    """ The primary benchmark class of the application, which manages the whole
    process from start to finish.  After collecting user options, the
    appropriate module is loaded and then the benchmarks are executed with the
    user's desired options.  Then this data is analyzed and collected into a
    comprehensive benchmark report.
    """

    def __init__(self, setup=False, options=None):
        """ __init__() prepares for benchmarking by collecting the user's
        runtime options and then managing the process.
        """
        if not options:
            options = {}

        self.options = options

        if self.options.get('--list'):

            self.__print_module_list()

        self.collection = 'test'

        # Retrieve command line self.options
        self.verbose = self.options.get('-v')
        self.really_verbose = self.options.get('-V')
        self.no_report = self.options.get('--no-report')
        self.random = self.options.get('--random')
        self.csv = not self.options.get('--no-csv')
        self.report_title = self.options.get('<report_title>')

        if not options.get('--length'):
            options['--length'] = 10
        self.entry_length = int(options.get('--length'))

        if not options.get('--trials'):
            options['--trials'] = 1000
        self.trials = int(options.get('--trials'))

        if self.options.get('--no-split'):

            self.split = False

        else:

            self.split = True

        self.write_times = []
        self.read_times = []

        self.time_and_date = time.strftime("%a, %d %b, %Y at %H:%M:%S")
        self.report_date = time.strftime("%b%d-%Y--%H-%M")

        if setup:
            self.setup()

    def setup(self):
        """ This function runs all of the setup commands for benchmarking. By
        separating this from __init__(), many of the functions from the
        Benchmark() class can be used outside of the application for testing.
        """

        if self.options.get('--debug'):

            self.feaux_run()

        else:

            self.db_name = self.options.get('<database>')

            self.module = self.__register_module(self.db_name)
            self.database_client = self.module[0].Benchmark(
                self.collection, setup=True, trials=self.trials
            )

            module_settings = self.module[1]
            self.number_of_nodes = module_settings.NUMBER_OF_NODES

            self.db_name = self.db_name.replace('db', '').upper()

            # Run the benchmarks!
            if self.split:

                self.run_split()

            else:

                self.run()

        if not self.report_title:

            self.report_title = '{db}-{date}'.format(
                db=self.db_name,
                date=self.report_date,
            )

        self.reports_dir = 'generated_reports/{title}'.format(
            title=self.report_title,
        )

        # TODO - fix a bug where 2 reports cannot be made in the same minute,
        # TODO - because the naming convention used here doesn't account for
        # TODO - seconds anymore
        makedirs(self.reports_dir)

        self.images_dir = self.reports_dir + '/images'
        makedirs(self.images_dir)

        self.package_dir = os.path.dirname(os.path.realpath(__file__))

        data = self.compile_data()

        report_data = self.generate_report_data(data)

        self.generate_report(report_data)

    def feaux_run(self):
        """ This function generates fake data to be used for testing purposes.
        The distribution is random so that analysis can still be performed and
        plots can be drawn.
        """

        self.number_of_nodes = 'n/a'
        self.db_name = 'feaux_db'

        r = np.random.normal(0.004, 0.001, self.trials)
        self.read_times = r.tolist()

        w = np.random.normal(0.005, 0.0015, self.trials)
        self.write_times = w.tolist()

        for i in progress.bar(list(range(self.trials))):

            pass

    def random_entry(self):
        """ This function generates a random sdata entry consisting of two
        fields - a string and an integer.  The string is generated from all
        ascii letters and the number is generated from numbers 0-9.

        :return dict entry: the random data entry that was generated
        """

        entry = dict()

        entry_fields = {
            'Number': string.digits,
            'Info': string.ascii_letters,
        }

        for field, selection in entry_fields.items():

            field_val = str()

            for x in range(self.entry_length):

                field_val += random.choice(selection)

            entry[field] = field_val

        return entry

    def run(self):
        """ This function keeps track of and calls the read/ write functions
        for benchmarking.  For each iteration, a new DB entry will be created,
        written to the DB, and then read back from it.
        """

        if self.random:

            msg = 'Error! Random mode can ONLY be used with split reads/writes!'
            exit(msg)

        for index in progress.bar(list(range(self.trials))):

            entry = self.random_entry()
            entry.update(Index=index)

            self.write(entry)

            if self.random:
                index = random.randint(0, index)

            if self.options.get('-s'):
                time.sleep(1/20)

            self.read(index)

    def run_split(self):
        """ This function performs the same actions as 'run()', with the key
        exception that this splits reads and writes into two separate runs,
        instead of alternating reads and writes.
        """

        print('\nWrite progress:\n')

        for index in progress.bar(list(range(self.trials))):

            entry = self.random_entry()
            entry.update(Index=index)

            self.write(entry)

            if self.options.get('-s'):
                time.sleep(1/20)

        print('\nRead progress:\n')

        for index in progress.bar(list(range(self.trials))):

            if self.random:
                index = random.randint(0, index)

            self.read(index)

            if self.options.get('-s'):
                time.sleep(1/20)

    def write(self, entry):
        """ This function handles all DB write commands and times that action.
        It takes a single parameter ('entry'), which is the data to
        be written to the DB.

        :param dict entry: The entry to be recorded to the DB
        """

        write_start_time = time.time()

        self.database_client.write(entry)

        write_stop_time = time.time()

        write_time = write_stop_time - write_start_time

        self.write_times.append(write_time)

        if self.really_verbose:

            write_msg = 'Write time: {time}'.format(time=write_time)

            print(write_msg)

    def read(self, index):
        """ This function handles all DB read commands, and times that action.
        It takes a single parameter, which is the index of an entry
        to retrieve from the DB.

        :param int index: The index of the item to be retrieved from the DB
        """

        read_start_time = time.time()

        read_entry = self.database_client.read(index)

        read_stop_time = time.time()

        read_time = read_stop_time - read_start_time

        self.read_times.append(read_time)

        if self.verbose or self.really_verbose:

            read_msg = 'Read data: {data}'.format(data=read_entry)

            if self.really_verbose:

                read_msg += '\nRead time: {time}'.format(time=read_time)

                read_msg += '\n--------------------------'

            print(read_msg)

    def compile_data(self):
        """ This function takes all the data collected from the trials (read
        and write times) and then calculates some important statistics about
        said data.  Without altering functionality, a report will be generated
        upon completion of analysis.

        :return dict compiled_data: dict containing all read and w
        """

        w = pd.DataFrame({'data': self.write_times})
        r = pd.DataFrame({'data': self.read_times})

        if self.csv:
            self.__generate_csv()

        write_metrics = self.__compute_descriptive_stats(w)
        read_metrics = self.__compute_descriptive_stats(r)

        rolling_avg_range = self.trials / 10

        writes_rolling_avg = self.__compute_rolling_avg(w, rolling_avg_range)
        reads_rolling_avg = self.__compute_rolling_avg(r, rolling_avg_range)

        write_metrics.update(rolling_avg=writes_rolling_avg)
        read_metrics.update(rolling_avg=reads_rolling_avg)

        normalized_writes = self.__normalize_data(
            w,
            write_metrics.get('avg'),
            write_metrics.get('stdev'),
        )
        normalized_reads = self.__normalize_data(
            r,
            read_metrics.get('avg'),
            read_metrics.get('stdev'),
        )

        write_metrics.update(normalized_data=normalized_writes)
        read_metrics.update(normalized_data=normalized_reads)

        compiled_data = {
            'write_metrics': write_metrics,
            'read_metrics': read_metrics,
            'n_stdev': self.n_stdev,
            'rolling_avg_range': rolling_avg_range,
        }

        return compiled_data

    def __compute_rolling_avg(self, dataframe, rolling_range=None):
        """ Given a dataframe object, this function will compute a rolling
        average and return it as a separate dataframe object

        :param DataFrame dataframe: a dataframe with which to compute a running
                    average
        :param int rolling_range: the range over which the rolling average
                    should be computed

        :return rolling_avg: a dataframe object with containing the running
                    average data
        """

        if not rolling_range:
            rolling_range = self.trials / 10

        rolling_avg = pd.stats.moments.rolling_mean(
            dataframe,
            rolling_range,
        )

        return rolling_avg

    def __generate_csv(self):
        """ This function creates a new DataFrame object with the raw read and
        write times and then writes it to a CSV file
        """

        raw_data = pd.DataFrame({
            'reads': self.read_times,
            'writes': self.write_times,
        })

        raw_data.to_csv('{parent_dir}/raw_data.csv'.format(
            parent_dir=self.reports_dir
        ))

    def __normalize_data(self, dataframe, average, stdev):
        """ This function takes a dataframe object and normalizes the data
        within, by removing outliers, which allows the plots to look a lot
        nicer

        :param DataFrame dataframe: the dataframe to be normalized
        :param float average: the average value from the dataframe
        :param float stdev: the standard deviation of the datframe

        :return DataFrame dataframe: the normalized dataframe
        """

        df = dataframe

        n_stdev = 3

        if self.options.get('--debug'):
            stdev = 15

        if stdev > 3 * average:

            n_stdev = 1

        elif stdev > 2 * average:

            n_stdev = 2

        self.n_stdev = n_stdev

        dataframe = df[abs(df.data - average) <= (n_stdev * stdev)]

        return dataframe

    def generate_report_data(self, compiled_data):
        """ This function prepares all of the actual tabular data for the
        report before it's written to the file.

        :param compiled_data: The post-analysis data from the benchmarks

        :return report_data: All of the tables for the report
        """

        cd = compiled_data

        param_table, param_table_md = self.__generate_parameter_tables(
            compiled_data
        )

        data_table, data_table_md = self.__generate_data_tables(
            compiled_data
        )

        if self.no_report:

            plots = {
                'speed_plot': None,
                'hist_plot': None,
                'avgs_plot': None,
            }

        else:

            plots = self.__generate_all_plots(compiled_data)

        report_data = {
            'database': self.db_name,
            'time_and_date': self.time_and_date,
            'entry_length': self.entry_length,
            'node_number': self.number_of_nodes,
            'trial_number': self.trials,
            'param_table': param_table,
            'data_table': data_table,
            'param_table_md': param_table_md,
            'data_table_md': data_table_md,
            'speed_plot': plots.get('speed_plot'),
            'hist_plot': plots.get('hist_plot'),
            'avgs_plot': plots.get('avgs_plot'),
        }

        return report_data

    def generate_report(self, report_data):
        """ This function will take the compiled data and generated a report
        from it.  A report file will also be saved in the `generated_reports`
        directory, unless the `--no_report` option was selected at runtime.

        :param report_data: all of the necessary data to generate the
                    benchmark report
        """

        if self.report_title:

            report_name = '{parent_dir}/{title}.md'.format(
                parent_dir=self.reports_dir,
                title=self.report_title,
            )

        else:

            report_name = '{parent_dir}/{db}-{date}.report.md'.format(
                parent_dir=self.reports_dir,
                db=self.db_name,
                date=self.report_date,
            )

        report_template_path = '{base_dir}/report_template.md'.format(
            base_dir=self.package_dir
        )
        with open(report_template_path, 'r') as infile:

            template = infile.read()

            terminal_report = template.format(**report_data)

            print('\n\n' + terminal_report + '\n\n')

            if not self.no_report:

                template = template.replace('_table', '_table_md')

                report = template.format(**report_data)

                with open(report_name, 'w+') as outfile:

                    outfile.write(report)

    def generate_plot(self, dataframe, name, plot_type='line', **kwargs):
        """ This function takes a DataFrame

        :param DataFrame dataframe: The data to be plotted
        :param str name: The name of the plot for saving
        :param str plot_type='line': The type of plot to generate
        :param **kwargs: the other options for controlling the look of each
                    plot
        """

        plt.figure()

        ax = dataframe.plot(
            title=kwargs.get('title'),
            grid=kwargs.get('grid'),
            legend=True,
            kind=plot_type,
        )

        if kwargs.get('x_label'):

            ax.set_xlabel(kwargs.get('x_label'))

        if kwargs.get('y_label'):

            ax.set_ylabel(kwargs.get('y_label'))

        current_name = '{parent_dir}/{name}'.format(
            parent_dir=self.images_dir,
            db=self.db_name,
            date=self.report_date,
            name=name,
        )

        plt.savefig(current_name)

    def __generate_all_plots(self, compiled_data):
        """ This function coordinates the creation of all benchmarking plots
        and then returns them

        :param dict compiled_data: all of the compiled data from benchmarks

        :return dict plots: the path for each plot created
        """

        cd = compiled_data

        template = '![Alt text](images/{db}-{date}-{name}.png "{name}")'
        img_template = template.format(
            db=self.db_name,
            date=self.report_date,
            name='{name}'
        )

        plots = {
            'speed_plot': img_template.format(name='rw'),
            'hist_plot': img_template.format(name='stats'),
            'avgs_plot': img_template.format(name='running_avg'),
        }

        img_name_template = '{db}-{date}-{name}'.format(
            db=self.db_name,
            date=self.report_date,
            name='{name}'
        )

        rw = pd.DataFrame({
            'Writes': cd.get('write_metrics').get('normalized_data').data,
            'Reads': cd.get('read_metrics').get('normalized_data').data,
        })

        avgs = pd.DataFrame({
            'Writes Average': cd.get('write_metrics').get('rolling_avg').data,
            'Reads Average': cd.get('read_metrics').get('rolling_avg').data,
        })

        self.generate_plot(
            rw,
            img_name_template.format(name='rw'),
            title='Plot of Read and Write Speeds',
            x_label='Trial Number',
            y_label='Time (s)',
        )

        self.generate_plot(
            avgs,
            img_name_template.format(name='running_avg'),
            title='Plot of Rolling Averages for Reads and Writes',
            x_label='Trial Number',
            y_label='Time (s)',
        )

        self.generate_plot(
            rw,
            img_name_template.format(name='stats'),
            title='Histogram of Read and Write Times',
            plot_type='hist',
            x_label='Value (s)',
        )

        return plots

    def __generate_parameter_tables(self, compiled_data):
        """ This function takes compiled data and gnerates the parameter table
        for the report.

        :param dict compiled_data: the compiled benchmark data

        :return tabulate_obj param_table: a tabulate object for display in the
                    console
        :return tabulate_obj param_table_md: a tabulate object for the markdown
                    report
        """

        cd = compiled_data

        param_header = [
            'Parameter',
            'Value',
        ]

        param_values = [
            ['Database Tested', self.db_name],
            ['Number of Trials', str(self.trials)],
            ['Length of Each Entry Field', str(self.entry_length)],
            ['Number of Nodes in Cluster', str(self.number_of_nodes)],
            ['# of StDev\'s Displayed in Graphs', str(cd.get('n_stdev'))],
            ['Range of Rolling Average in Graphs', str(cd.get('rolling_avg_range'))],
            ['Split Reads and Writes', str(self.split)],
            ['Debug Mode', str(self.options.get('--debug'))],
            ['Random Mode (Random Reads)', str(self.options.get('--random'))],
        ]


        param_table = tabulate(
            tabular_data=param_values,
            headers=param_header,
            tablefmt='grid',
        )

        param_table_md = tabulate(
            tabular_data=param_values,
            headers=param_header,
            tablefmt='pipe',
        )

        return param_table, param_table_md

    @staticmethod
    def __compute_descriptive_stats(dataframe):
        """ A static method that computes the descriptive statistics of a given
        dataframe

        :param DataFrame dataframe: the dataframe with which to compute the
                    descriptive stats

        :return dict metrics: a dict of the descriptive statistics
        """

        df = dataframe

        metrics = {
            'avg': df.data.mean(),
            'stdev': df.data.std(),
            'max': df.data.max(),
            'min': df.data.min(),
            }

        range = metrics.get('max') - metrics.get('min')
        metrics.update(range=range)

        return metrics

    @staticmethod
    def __generate_data_tables(compiled_data):
        """ This function creates the data tables for the report.

        :param dict compiled_data: the compiled data from benchmarking

        :return tabulate_obj data_table: the table for viewing in the terminal
        :return tabulate_obj data_table_md: the table for viewing in the
                    markdown report
        """

        cd = compiled_data

        data_header = [
            'Operation',
            'Average',
            'St. Dev.',
            'Max Time',
            'Min Time',
            'Range',
        ]

        write_metrics = cd.get('write_metrics')
        read_metrics = cd.get('read_metrics')

        metrics = [
            'avg',
            'stdev',
            'max',
            'min',
            'range',
        ]

        data_values = [
            [
                'writes'
            ],
            [
                'reads'
            ],
        ]

        for metric in metrics:

            write_metric = write_metrics.get(metric)
            data_values[0].append(write_metric)

            read_metric = read_metrics.get(metric)
            data_values[1].append(read_metric)

        data_table = tabulate(
            tabular_data=data_values,
            headers=data_header,
            tablefmt='grid',
            floatfmt='.5f',
        )

        data_table_md = tabulate(
            tabular_data=data_values,
            headers=data_header,
            tablefmt='pipe',
            floatfmt='.5f',
        )

        return data_table, data_table_md

    @staticmethod
    def __print_module_list():
        """ Static method that prints the list of available modules to the
        console
        """

        mod_list = retrieve_module_list()

        message = 'The following modules are available: \n\n'

        for mod in mod_list:

            message += '-{mod}\n'.format(mod=mod)

        exit(message)

    def __register_module(self, db_module):
        """ This function begins the process of registering a module for
        benchmarking.  It checks to see if the module exists, and if it does,
        it will attempt the import.

        :param str db_module: The module to register

        :return tup module: a tuple with the main and local parts of the module
        """

        module_list = retrieve_module_list()

        if db_module in module_list:

            module = self.__import_db_mod(db_module)

            return module

        else:

            error = 'Invalid DB module!  Please be sure you are using the \n' \
                    'package name and not just the name of the database ' \
                    'itself.\n'

            exit(error)

    @staticmethod
    def __import_db_mod(module):
        """ This function does the actual import of the database-specific
        module.

        :param str module: The module to be imported

        :return tup module: a tuple with the main and local parts of the module
        """

        try:

            main = importlib.import_module(module + '.main')
            local = importlib.import_module(module + '.local')

            module = (main, local)

            return module

        except ImportError:

            error = 'Error!  Package could not be imported!  Please make \n' \
                    'sure you are using the package name and not the name \n' \
                    'of the database itself.'

            exit(error)

if __name__ == '__main__':

    doc_opt= docopt(__doc__)

    Benchmark(setup=True, options=doc_opt)