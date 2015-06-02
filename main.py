"""
DB Benchmarking Application
===========================

Main.py

This file houses the core of the application, and is where all of the
read/write commands are issued from, timed, and all data is analyzed.  Results
from the trials are printed to the console by default, and are also printed to
a markdown file to keep a record of.  This is particularly helpful when
benchmarking multiple DB's in a row to see which one is fastest for deployment
purposes.

    Usage:
        main.py <database> [options]
        main.py --debug [options]
        main.py <database> <report_title> [options]

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
        --csv               Records unaltered read and write data to a CSV file
                                for your own analysis
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
import ipdb

# TODO [x] - add a progress bar for non-verbose output
# TODO [x] - add some better data analysis
# TODO [ ] - add python 3.x support
# TODO [ ] - remove outlier table from report and add system parameter table

from os import getcwd, listdir, makedirs
from sys import exit
import time
import string
import random
import importlib
import pandas as pd
import numpy as np
import pylab

from tabulate import tabulate

from docopt import docopt
from clint.textui import progress

# Although it appears as if this import is unused, it's used for formatting
# pandas graphs.
import seaborn


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

        if options.get('--list'):

            mod_list = retrieve_module_list()

            message = 'The following {number} modules are available: \n\n'.\
                format(number=mod_list.__len__())

            for mod in mod_list:

                message += '-{mod}\n'.format(mod=mod)

            exit(message)

        self.verbose = options.get('-v')
        self.really_verbose = options.get('-V')
        self.collection = 'test'
        self.sorting_index = 'ID'
        self.entry_length = int(options.get('--length'))
        self.trials = int(options.get('--trials'))
        self.no_report = options.get('--no-report')
        self.chaos = options.get('--chaos')
        self.csv = options.get('--csv')
        self.report_title = options.get('<report_title>')

        self.write_times = []
        self.read_times = []

        self.time_and_date = time.strftime("%a, %d %b, %Y %H:%M:%S")
        self.report_date = time.strftime("%b%d-%Y-%H:%M:%S")
        self.split = True

        if options.get('--debug'):

            self.feaux_run()

        else:
            self.db_name = options.get('<database>')

            self.module = self.register_module(self.db_name)
            self.database = self.module.Benchmark(self.collection, setup=True, trials=self.trials)

            self.module_settings = self.import_db_mod(
                self.db_name, mod_file='local')
            self.number_of_nodes = self.module_settings.NUMBER_OF_NODES

            self.db_name = self.db_name.replace('db', '').upper()

            # Run the benchmarks!
            if options.get('--no-split'):
                self.split = False
                self.run()
            else:
                self.run_split()

        if self.report_title:
            self.reports_dir = 'generated_reports/{title}'.format(
                               title=self.report_title,
            )

        else:
            self.reports_dir = 'generated_reports/{db}-{date}'.format(
                               db=self.db_name,
                               date=self.report_date,
            )
        makedirs(self.reports_dir)

        self.images_dir = self.reports_dir + '/images'
        makedirs(self.images_dir)

        data = self.compile_data()

        report_data = self.generate_report_data(data)

        self.generate_report(report_data)

        # self.compile_plots(data)

    def feaux_run(self):
        """ This function generates fake data to be used for testing purposes.
        """

        self.number_of_nodes = 'n/a'
        self.db_name = 'feaux_db'

        r = np.random.normal(0.004, 0.001, self.trials)
        self.read_times = r.tolist()

        w = np.random.normal(0.005, 0.0015, self.trials)
        self.write_times = w.tolist()

        for i in progress.bar(range(self.trials)):

            pass

    def random_entry(self, entry_type='string'):
        """ This function generates a random string or random number depending
        on the arguments passed in.  The string is generated from all ascii
        letters and the number is generated from numbers 0-9.

        :param entry_type: the specified type of random entry, either 'string'
                    or 'number'

        :return: the random string or number that was just generated
        """

        entry = ''
        entry_length = self.entry_length

        if entry_type == 'string':

            selection = string.ascii_letters

        else:

            selection = string.digits
            entry_length /= 2

        for x in range(entry_length):

            entry += random.choice(selection)

        return entry

    def run(self):
        """ This function will keep track of and call the read/ write functions
        for benchmarking.  For each iteration, a new DB entry will be created,
        written to the DB,  and then read back from it.

        """
        if self.chaos:

            msg = 'Error! Chaos mode can ONLY be used with split reads/writes!'
            exit(msg)

        for index in progress.bar(range(self.trials)):

            item_number = self.random_entry(entry_type='number')
            info = self.random_entry(entry_type='string')

            entry = {
                'Index': index,
                'Number': item_number,
                'Info': info
            }

            if not self.writes(entry):
                print 'WRITE ERROR'

            if self.chaos:
                index = random.randint(0, index)

            if options.get('-s'):
                time.sleep(1/20)

            if not self.reads(index):
                print 'READ ERROR'

    def run_split(self):
        """ This function performs the same actions as 'run()', with the key
        exception that this splits reads and writes into two separate runs,
        instead of alternating reads and writes.
        """

        print('\nWrite progress:\n')

        for index in progress.bar(range(self.trials)):

            item_number = self.random_entry(entry_type='number')
            info = self.random_entry(entry_type='string')

            entry = {
                'Index': index,
                'Number': item_number,
                'Info': info
            }

            if not self.writes(entry):
                print 'WRITE ERROR!'

            if options.get('-s'):
                time.sleep(1/20)

        print('\nRead progress:\n')

        for index in progress.bar(range(self.trials)):

            if self.chaos:
                    index = random.randint(0, index)

            if not self.reads(index):
                print 'READ ERROR!'

            if options.get('-s'):
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

        :return compiled_data: All of the data needed to generate a full
                    benchmarking report
        """

        w = pd.DataFrame({'data': self.write_times})
        r = pd.DataFrame({'data': self.read_times})

        if self.csv:

            w.to_csv('{parent_dir}/writes.csv'.format(
                parent_dir=self.reports_dir
            ))
            r.to_csv('{parent_dir}/reads.csv'.format(
                parent_dir=self.reports_dir
            ))

        w_out = pd.DataFrame({'data': self.write_times})
        r_out = pd.DataFrame({'data': self.read_times})

        write_avg = w.data.mean()
        write_stdev = w.data.std()
        write_max = w.data.max()
        write_min = w.data.min()
        write_range = write_max - write_min

        read_avg = r.data.mean()
        read_stdev = r.data.std()
        read_max = r.data.max()
        read_min = r.data.min()
        read_range = read_max - read_min

        if options.get('--debug'):
            write_stdev = 15
            read_stdev = 15

        n_stdev = 3

        if (read_stdev > 3 * read_avg) or (write_stdev > 3 * write_avg):

            n_stdev = 1

        elif (read_stdev > 2 * read_avg) or (write_stdev > 2 * write_avg):

            n_stdev = 2

        # Remove values that are beyond 3 st. dev.'s from the mean
        w = w[abs(w.data - write_avg) <= (n_stdev * write_stdev)]
        r = r[abs(r.data - read_avg) <= (n_stdev * read_stdev)]

        # Keep these outliers for display to the user
        w_out = w_out[abs(w_out.data - write_avg) >= (n_stdev * write_stdev)]
        r_out = r_out[abs(r_out.data - read_avg) >= (n_stdev * read_stdev)]

        writes_rolling_avg = self.compute_rolling_avg(w)
        reads_rolling_avg = self.compute_rolling_avg(r)

        outlier_values = []

        if len(w_out):
            for count, value in w_out.data.iteritems():
                outlier_values.append([
                    'Write',
                    count,
                    value,
                ])

        if len(r_out):
            for count, value in r_out.data.iteritems():
                pass
                outlier_values.append([
                    'Read',
                    count,
                    value,
                ])

        compiled_data = {
            'writes': w,
            'write_avg': write_avg,
            'write_stdev': write_stdev,
            'write_max': write_max,
            'write_min': write_min,
            'write_range': write_range,
            'writes_rolling_avg': writes_rolling_avg,
            'reads': r,
            'read_avg': read_avg,
            'read_stdev': read_stdev,
            'read_max': read_max,
            'read_min': read_min,
            'read_range': read_range,
            'reads_rolling_avg': reads_rolling_avg,
            'outlier_values': outlier_values,
            'n_stdev': n_stdev,
        }

        return compiled_data

    def generate_report_data(self, compiled_data):
        """ This function generates all of the actual tabular data that is
        displayed in the report.

        :param compiled_data: The post-analysis data from the benchmarks

        :return report_data: All of the tables for the report
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
            ['# of StDev\'s Displayed in Graphs', str(cd['n_stdev'])],
            ['Split Reads and Writes', str(self.split)],
            ['Debug Mode', str(options.get('--debug'))],
            ['Chaos Mode (Random Reads)', str(options.get('--chaos'))],
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
            ['Writes', cd['write_avg'], cd['write_stdev'], cd['write_max'],
             cd['write_min'], cd['write_range']],
            ['Reads', cd['read_avg'], cd['read_stdev'], cd['read_max'],
             cd['read_min'], cd['read_range']],
        ]

        outlier_header = [
            'Operation',
            'Trial Number',
            'Value',
        ]

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
            tabular_data=cd['outlier_values'],
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
            tabular_data=cd['outlier_values'],
            headers=outlier_header,
            tablefmt='pipe'
        )

        #TODO - fix the terminal report so graph names aren't generated

        image_template = '![Alt text](images/{db}-{date}-{name}.png "{name}")'

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

        rw = pd.DataFrame({
            'Writes': cd['writes'].data,
            'Reads': cd['reads'].data,
        })
        # ipdb.set_trace()
        avgs = pd.DataFrame({
            'Writes Average': cd['writes_rolling_avg'],
            'Reads Average': cd['reads_rolling_avg'],
        })

        if not self.no_report:

            self.generate_plot(
                'rw', rw,
                title='Plot of Read and Write Speeds',
                x_label='Trial Number',
                y_label='Time (s)',
            )

            self.generate_plot(
                'running_averages', avgs,
                title='Plot of Rolling Averages for Reads and Writes',
                x_label='Trial Number',
                y_label='Time (s)',
            )

            self.generate_plot(
                'stats', rw,
                title='Histogram of Read and Write Times',
                plot_type='hist',
                x_label='Value (s)',
            )

        report_data = {
            'database': self.db_name,
            'time_and_date': self.time_and_date,
            'entry_length': self.entry_length,
            'node_number': self.number_of_nodes,
            'trial_number': self.trials,
            'param_table': param_table,
            'data_table': data_table,
            'outlier_table': outlier_table,
            'param_table_md': param_table_md,
            'data_table_md': data_table_md,
            'outlier_table_md': outlier_table_md,
            'speed_plot': speed_plot,
            'hist_plot': hist_plot,
            'avgs_plot': avgs_plot,
        }

        return report_data

    @staticmethod
    def compute_rolling_avg(dataframe):
        """ Given a dataframe object, this function will compute a running
        average and return it as a separate dataframe object

        :param dataframe: a dataframe with which to compute a running average
        :return rolling_avg: a dataframe object with .data containing the
                    running average data
        """

        rolling_avg = pd.stats.moments.rolling_mean(dataframe, 100).data

        # count = 0
        # sum = 0
        # avgs = []
        #
        # for item in dataframe.data:
        #
        #     sum += item
        #     count += 1
        #
        #     avg = sum / count
        #     avgs.append(avg)
        #
        # rolling_avg = pd.DataFrame({'data': avgs})

        return rolling_avg

    def generate_report(self, report_data):
        """ This function will take the compiled data and generated a report
        from it.  If the `--report` option was selected at runtime, a report
        file will also be saved in the `generated_reports` directory.

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

        with open('report_template.md', 'r') as infile:

            template = infile.read()

            terminal_report = template.format(**report_data)

            print '\n\n' + terminal_report + '\n\n'

            if not self.no_report:

                template = template.replace('_table', '_table_md')

                report = template.format(**report_data)

                with open(report_name, 'w+') as outfile:

                    outfile.write(report)

    def generate_plot(self, name, data_frame, title=None, x_label=None,
                      y_label=None, grid=True, plot_type='line'):
        """ This function take several parameters and generates a plot based
        on them.

        :param name: The name of the plot, which is important for saving
        :param data_frame: The data to be plotted
        :param title: The title to be displayed above the plot
        :param x_label: The label for the x-axis
        :param y_label: The label for the y-axis
        :param grid: Boolean to determine whether or not a grid should be used
        :param plot_type: The type of plot to generate
        """

        import matplotlib.pyplot as plt

        plt.figure()

        ax = data_frame.plot(
            title=title,
            grid=grid,
            legend=True,
            kind=plot_type,
        )

        if x_label:

            ax.set_xlabel(x_label)

        if y_label:

            ax.set_ylabel(y_label)

        current_name = '{parent_dir}/{db}-{date}-{name}'.format(
            parent_dir=self.images_dir,
            db=self.db_name,
            date=self.report_date,
            name=name,
        )

        pylab.savefig(current_name)

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
                    'package name and not just the name of the database ' \
                    'itself.\n'

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