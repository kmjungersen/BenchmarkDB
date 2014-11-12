"""
DB Benchmarking Application
===========================

Main.py

This file houses the core of the application, and is where all of the read/write
commands are issued from, timed, and all data is analyzed.  Results from the
trials are printed to the console by default, but can optionally be printed to a
file to keep a record of.  This is particularly helpful when benchmarking
multiple DB's in a row to see which one is best for deployment purposes.

    Usage:
        main.py <database> [options]

    Options:
        -h --help           Show this help screen
        -v                  Show verbose output from the application
        -V                  Show REALLY verbose output, including the time
                                from each run
        -s                  Sleep mode (experimental) - sleeps for 1/20 (s)
                                between each read and write

        -c --chaos          Activates CHAOS mode, where reads are taken
                                randomly from the DB instead of sequentially
        -l --list           Outputs a list of available DB modules
        -r --report         Option to generate a report file, which will
                                OVERWRITE any existing reports from the specified
                                DB in the `generated_reports` directory
        --split             Splits reads and writes into two consecutive
                                batches instead of alternating between them
        --debug             Generates a random dataset instead of actually
                                connecting to a DB

        --length=<n>        Specify an entry length for reads/writes [default: 10]
        --trials=<n>        Specify the number of reads and writes to make to the
                                DB to collect data on [default: 100]

"""

# TODO [x] - add a progress bar for non-verbose output
# TODO [ ] - add some better data analysis

from os import getcwd, listdir
from sys import exit
import time
import string
import random
import importlib
import pandas as pd
import numpy as np
import pylab
import seaborn

from tabulate import tabulate

# from numpy import array, average, std, max, min, delete
from scipy import stats
from docopt import docopt
from clint.textui import progress


def retrieve_module_list():
    """ This function will retrieve a list of all available modules in the
    project directory and then return said list.

    :return mod_list: The list of modules in the project directory

    """
    current_dir = getcwd()
    mod_list = []

    for item in listdir(current_dir):

        if item.endswith('db'):

            mod_list.append(item)

    return mod_list


class Benchmark():

    def __init__(self):
        """ The init method is passed a single parameter upon initialization in
        order to define which database should be benchmarked.  Other important
        values are defined here, such as the entry length and the number of
        trials to execute.

        """

        if options['--list']:

            mod_list = retrieve_module_list()

            message = 'The following {number} modules are available: \n\n'.\
                format(number=mod_list.__len__())

            for mod in mod_list:

                message += '-{mod}\n'.format(mod=mod)

            exit(message)

        self.verbose = options['-v']
        self.really_verbose = options['-V']
        self.collection = 'test'
        self.entry_length = int(options['--length'])
        self.number_of_trials = int(options['--trials'])
        self.report = options['--report']
        self.chaos = options['--chaos']



        # if self.report:
        # self.matplotlib = importlib.import_module('matplotlib')
        # self.matplotlib.use('Agg')
        # self.plt = importlib.import_module('matplotlib.pyplot')

        self.write_times = []
        self.read_times = []

        self.sorting_index = 'ID'
        self.reports_dir = 'generated_reports'
        self.image_names = {}

        self.time_and_date = time.strftime("%a, %d %b, %Y %H:%M:%S")
        self.report_date = time.strftime("%b%d-%Y-%H:%M:%S")

        if options['--debug']:

            self.feaux_run()

        else:
            self.db_name = options['<database>']

            self.module = self.register_module(self.db_name)
            self.database = self.module.Benchmark(self.collection, setup=True)

            self.module_settings = self.import_db_mod(
                self.db_name, mod_file='local')
            self.number_of_nodes = self.module_settings.NUMBER_OF_NODES

            self.db_name = self.db_name.replace('db', '').upper()

            # Run the benchmarks!
            if options['--split']:
                self.run_split()
            else:
                self.run()

        data = self.compile_data()

        report_data = self.generate_report_data(data)

        self.generate_report(report_data)

        # self.compile_plots(data)


    def random_entry(self, entry_type='string'):
        """ This function generates a random string or random number depending
        on the arguments passed in.  The string is generated from all ascii
        letters and the number is generated from numbers 0-9.

        :param entry_type: the specified type of random entry, either 'string'
                    or 'number'

        :return: the random string or number that was just generated
        """

        entry = ''

        if entry_type == 'string':

            selection = string.ascii_letters

        else:

            selection = string.digits

        for x in range(self.entry_length):

            entry += random.choice(selection)

        return entry

    def run(self):
        """ This function will keep track of and call the read/ write functions
        for benchmarking.  For each iteration, a new DB entry will be created,
        written to the DB,  and then read back from it.

        """

        for index in progress.bar(range(self.number_of_trials)):

            item_number = self.random_entry(entry_type='number')
            info = self.random_entry(entry_type='string')

            entry = {
                'Index': index,
                'number': item_number,
                'Info': info
            }

            if not self.writes(entry):
                print 'WRITE ERROR'

            if self.chaos:
                index = random.randint(0, index)

            if options['-s']:
                time.sleep(1/20)

            if not self.reads(index):
                print 'READ ERROR'

    def run_split(self):
        """

        :return:
        """

        print "Write progress:\n"

        for index in progress.bar(range(self.number_of_trials)):

            item_number = self.random_entry(entry_type='number')
            info = self.random_entry(entry_type='string')

            entry = {
                'Index': index,
                'number': item_number,
                'Info': info
            }

            if not self.writes(entry):
                print 'WRITE ERROR!'

            if options['-s']:
                time.sleep(1/20)

        print 'Read progress:\n'

        for index in progress.bar(range(self.number_of_trials)):

            if self.chaos:
                    index = random.randint(0, index)

            if not self.reads(index):
                print 'READ ERROR!'

            if options['-s']:
                time.sleep(1/20)

    def writes(self, entry):
        """ This function handles all DB write commands, and times that action
        as well.  It takes a single parameter ('entry'), which is the data to
        be written to the DB.

        :param entry: The entry to be recorded to the DB

        :return: True, if all operations successfully completed
        """

        write_start_time = time.time()

        self.database.write(entry)

        write_stop_time = time.time()

        write_time = write_stop_time - write_start_time

        self.write_times.append(write_time)

        if self.really_verbose:

            write_msg = 'Write time: {time}'.format(time=write_time)

            print write_msg

        return True

    def reads(self, index):
        """ This function handles all DB read commands, and times that action
        as well.  It takes a single parameter, which is the index of an entry
        to retrieve from the DB.

        :param index: The index of the item to be retrieved from the DB

        :return: True, if all operations successfully completed
        """

        read_start_time = time.time()

        read_entry = self.database.read(index)

        read_stop_time = time.time()

        read_time = read_stop_time - read_start_time

        self.read_times.append(read_time)

        if self.verbose or self.really_verbose:

            read_msg = 'Read data: {data}'.format(data=read_entry)

            if self.really_verbose:

                read_msg += '\nRead time: {time}'.format(time=read_time)

                read_msg += '\n--------------------------'

            print read_msg

        return True

    def compile_data(self):
        """ This function takes all the data collected from the trials (read
        and write times) and then calculates some important statistics about
        said data.  Without altering functionality, a report will be generated
        upon completion of analysis.

        :return compiled_data: All of the data and tables needed to generate a
                    full benchmarking report
        :return results: The compiled results from the statistical analysis of
                    the trial data as a dict
        """

        self.write_times = array(self.write_times)
        self.read_times = array(self.read_times)

        write_avg = average(self.write_times)
        write_stdev = std(self.write_times)
        write_max = max(self.write_times)
        write_min = min(self.write_times)
        write_range = write_max - write_min

        read_avg = average(self.read_times)
        read_stdev = std(self.read_times)
        read_max = max(self.read_times)
        read_min = min(self.read_times)
        read_range = read_max - read_min

        unnormalized_data = {
            'write_times': self.write_times,
            'write_avg': write_avg,
            'write_stdev': write_stdev,
            'write_max': write_max,
            'write_min': write_min,
            'read_times': self.read_times,
            'read_avg': read_avg,
            'read_stdev': read_stdev,
            'read_max': read_max,
            'read_min': read_min,
        }

        normalized_data = self.normalize_data(unnormalized_data)

        self.write_times = normalized_data['writes']
        self.read_times = normalized_data['reads']
        writes_running_avg = normalized_data['writes_running_avg']
        reads_running_avg = normalized_data['reads_running_avg']
        writes_outliers = normalized_data['writes_outliers']
        reads_outliers = normalized_data['reads_outliers']

        param_header = [
            'Parameter',
            'Value',
        ]

        param_values = [
            ['Database Tested', self.db_name],
            ['Number of Trials', str(self.number_of_trials)],
            ['Length of Each Entry Field', str(self.entry_length)],
            ['Number of Nodes in Cluster', str(self.number_of_nodes)],
        ]

        data_header = [
            'Operation',
            'Average',
            'St. Dev.',
            'Max Time',
            'Min Time',
            'Range',
        ]

        data_values = [
            ['Writes', write_avg, write_stdev, write_max, write_min,
             write_range],
            ['Reads', read_avg, read_stdev, read_max, read_min,
             read_range],
        ]

        outlier_header = [
            'Operation',
            'Trial Number',
            'Value',
        ]

        outlier_values = []

        if len(writes_outliers):
            for count, value in writes_outliers.iteritems():
                outlier_values.append([
                    'Write',
                    count,
                    value,
                ])

        if len(reads_outliers):
            for count, value in reads_outliers.iteritems():
                outlier_values.append([
                    'Read',
                    count,
                    value,
                ])

        param_table = tabulate(
            tabular_data=param_values,
            headers=param_header,
            tablefmt='grid',
        )

        data_table = tabulate(
            tabular_data=data_values,
            headers=data_header,
            tablefmt='grid',
            floatfmt='.5f',
        )

        outlier_table = tabulate(
            tabular_data=outlier_values,
            headers=outlier_header,
            tablefmt='grid'
        )

        param_table_md = tabulate(
            tabular_data=param_values,
            headers=param_header,
            tablefmt='pipe',
        )

        data_table_md = tabulate(
            tabular_data=data_values,
            headers=data_header,
            tablefmt='pipe',
            floatfmt='.5f',
        )

        outlier_table_md = tabulate(
            tabular_data=outlier_values,
            headers=outlier_header,
            tablefmt='pipe'
        )

        image_template = '![Alt text](images/{db}-{date}-{name}.png "{name}"'

        speed_plot = image_template.format(
            db=self.db_name,
            date=self.report_date,
            name='rw',
        )

        hist_plot = image_template.format(
            db=self.db_name,
            date=self.report_date,
            name='stats',
        )

        avgs_plot = image_template.format(
            db=self.db_name,
            date=self.report_date,
            name='running_averages',
        )

        results = {
            'database': self.db_name,
            'trial_number': self.number_of_trials,
            'entry_length': self.entry_length,
            'node_number': self.number_of_nodes,
            'write_times': self.write_times,
            'write_avg': write_avg,
            'write_stdev': write_stdev,
            'write_max': write_max,
            'write_min': write_min,
            'write_range': write_range,
            'writes_running_avg': writes_running_avg,
            'read_times': self.read_times,
            'read_avg': read_avg,
            'read_stdev': read_stdev,
            'read_max': read_max,
            'read_min': read_min,
            'read_range': read_range,
            'reads_running_avg': reads_running_avg,
        }

        compiled_data = {
            'database': self.db_name,
            'time_and_date': self.time_and_date,
            'param_table': param_table,
            'data_table': data_table,
            'outlier_table': outlier_table,
            'param_table_md': param_table_md,
            'data_table_md': data_table_md,
            'outlier_table_md': outlier_table_md,
            'speed_plot': speed_plot,
            'hist_plot': hist_plot,
            'avgs_plot': avgs_plot,
            'results': results,
        }

        return compiled_data

    def normalize_data(self, unnormalized_data):
        """
        """

        writes = unnormalized_data['write_times']
        reads = unnormalized_data['read_times']
        write_stdev = unnormalized_data['write_stdev']
        read_stdev = unnormalized_data['read_stdev']
        write_avg = unnormalized_data['write_avg']
        read_avg = unnormalized_data['read_avg']

        writes_running_avg = []
        reads_running_avg = []
        writes_outliers = {}
        reads_outliers = {}

        w_count = 0
        r_count = 0
        w_sum = 0
        r_sum = 0

        for w in writes:
            if abs(w - write_avg) > (3 * write_stdev):
                delete(writes, w_count)
                writes_outliers[w_count] = w

            w_sum += w
            w_count += 1
            avg = w_sum / w_count
            writes_running_avg.append(avg)

        for r in reads:
            if abs(r - read_avg) > (3 * read_stdev):
                delete(reads, r_count)
                reads_outliers[r_count] = r

            r_sum += r
            r_count += 1
            avg = r_sum / r_count
            reads_running_avg.append(avg)

        normalized_data = {
            'writes': writes,
            'reads': reads,
            'writes_running_avg': writes_running_avg,
            'reads_running_avg': reads_running_avg,
            'writes_outliers': writes_outliers,
            'reads_outliers': reads_outliers,
        }

        return normalized_data

    def generate_report(self, report_info):
        """ This function will take the compiled data and generated a report
        from it.  If the `--report` option was selected at runtime, a report
        file will also be saved in the `generated_reports` directory.

        :param report_info: all of the necessary information to generate the
                    benchmark report
        """

        report_name = '{parent_dir}/{db}-{date}.report.md'.format(
            parent_dir=self.reports_dir,
            db=self.db_name,
            date=self.report_date,
        )

        with open('report_template.md', 'r') as infile:

            template = infile.read()

            terminal_report = template.format(**report_info)

            print '\n\n' + terminal_report + '\n\n'

            if self.report:

                template = template.replace('_table', '_table_md')

                report = template.format(**report_info)

                with open(report_name, 'w+') as outfile:

                    outfile.write(report)

    def compile_plots(self, compiled_data):
        """ This function will take compiled data and generate certain graphs
        to display it visually.

        :param report_info:
        :return:
        """

        results = compiled_data['results']

        writes = results['write_times']
        reads = results['read_times']

        writes_running_avg = results['writes_running_avg']
        reads_running_avg = results['reads_running_avg']

        # Generating read/write time plot
        self.generate_plot(
            name='rw',
            data_set={'writes': writes, 'reads': reads},
            title='Plot of read and write speeds for every trial',
            x_label='Trial Number',
            y_label='Speed (seconds)',
        )

        self.generate_plot(
            name='stats',
            data_set={'writes': writes, 'reads': reads},
            title='Histogram of Read and Write Times',
            x_label='Time (seconds)',
            y_label='Number of Occurrences',
            plot_type='hist',
        )

        self.generate_plot(
            name='running_averages',
            data_set={'writes_running_avg': writes_running_avg, 'reads_running_avg': reads_running_avg},
            title='Read and Write Speeds - Running Averages',
            x_label='Trial Number',
            y_label='Running Average (s)',
        )

    def generate_plot(self, name, data_set, title=None, x_label=None,
                      y_label=None, grid=True, plot_type='plot'):
        """

        :param name:
        :param data:
        :param title:
        :param x_label:
        :param y_label:
        :param grid:
        :param type:
        :return:
        """
        fig, a = self.plt.subplots()

        legend_list = []

        if plot_type == 'plot':

            for label, data in data_set.iteritems():

                foo, = a.plot(data, label=label)
                legend_list.append(foo)

            a.legend(handles=legend_list)

        elif plot_type == 'hist':

            data_list = []
            label_list = []

            for label, data in data_set.iteritems():

                data_list.append(data)
                label_list.append(label)

            foo = a.hist(data_list, histtype='bar', label=label_list)

        if title:
            a.set_title(title)

        if x_label:
            a.set_xlabel(x_label)

        if y_label:
            a.set_ylabel(y_label)

        if grid:
            a.grid = True

        current_name = '{parent_dir}/images/{db}-{date}-{name}'.format(
            parent_dir=self.reports_dir,
            db=self.db_name,
            date=self.report_date,
            name=name,
        )
        self.image_names['reads_writes'] = current_name

        # a.show()

        fig = a.get_figure()

        fig.savefig(current_name)

    def register_module(self, db_mod):
        """ This function begins the process of registering a module for
        benchmarking.  The first step is to check to see if the module exists,
        and if it does, it will call `import_db_mod` to attempt the import.

        :param db_mod: The module to register

        :return mod_class: `mod_class` will ONLY BE RETURNED IF `import_db_mod`
                    runs successfully!
        """

        mod_list = retrieve_module_list()

        if db_mod in mod_list:

            return self.import_db_mod(db_mod)

        else:

            error = 'Invalid DB module!  Please be sure you are using the \n' \
                    'package name and not just the name of the database itself.'\
                    '\n'

            exit(error)

    @staticmethod
    def import_db_mod(module, mod_file='main'):
        """ This function will do the actual import of the database-specific
        module.  The `try/except` format is meant to be able to attempt the
        import, but fail gracefully if for some reason the package can't be
        imported.

        :param module: The module to be imported

        :return mod_class: The `Benchmark` class of the module, if it exists
        """

        try:

            package = '{mod}.{file}'.format(mod=module, file=mod_file)

            mod_class = importlib.import_module(package)

            return mod_class

        except ImportError:

            error = 'Error!  Package could not be imported!  Please make \n' \
                    'sure you are using the package name and not the name \n' \
                    'of the database itself.'

            exit(error)

if __name__ == '__main__':

    options = docopt(__doc__)

    Benchmark()