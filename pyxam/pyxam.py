#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module pyxam

This is the primary script for Pyxam. This script can be run from the command line with Pyxam's options or run in api
mode from another python script. When run from the command line all command line arguments are passed to Pyxam and api
mode is automatically disabled. In addition to launching Pyxam this script is also responsible for welcome and goodbye
messages and tracking the Pyxam version number.



Prior to launching however script checks Python dependencies for `matplotlib` and `numpy` which are needed for
generating figure images as well as `pweave` which is needed for weaving inline Python code. Failing to meet one of
these dependencies will result in an exit statement and a recommendation todo `pip install` for the dependency.
"""
# TODO Finish docs
# TODO Tests & cleanup


# Module Dependencies
try:
    import matplotlib
except ImportError:
    exit('matplotlib is required for Pyxam. Please run:\n\n\t$ pip install matplotlib')
try:
    import numpy
except ImportError:
    exit('numpy is required for Pyxam. Please run:\n\n\t$ pip install numpy')
try:
    import pweave
except ImportError:
    exit('pweave is required for Pyxam. Please run:\n\n\t$ pip install pweave')


import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import mixer
import options
import fileutil
import lib_loader
import process_list
import plugin_loader
import parser_composer


# Pyxam Version Number
__version__ = 'v0.3.5'


# Copy of original arguments
_args = ['No stored args']


# Pyxam Title String
title = '    ____                           \n' \
        '   / __ \__  ___  ______ _____ ___ \n' \
        '  / /_/ / / / / |/_/ __ `/ __ `__ \\ \n' \
        ' / ____/ /_/ />  </ /_/ / / / / / /\n' \
        '/_/    \__, /_/|_|\__,_/_/ /_/ /_/ \n' \
        '      /____/'


def welcome():
    """
    Posts the Pyxam title and version number
    """
    options.post(title, '\n\n\tLatex Exam Generation.', __version__, '\n')


def goodbye():
    """
    Posts a goodbye message
    """
    options.post('Thanks for using Pyxam, have a nice day!')


def store_args(args=None):
    """
    Store a list of arguments. Called every time Pyxam is run.

    :param args: The args to store
    :return: The most recently stored args or a message saying there are no stored args.
    """
    global _args
    if args is not None:
        _args.append(args)
    return _args[-1]


def start(args, api=True):
    """
    Start Pyxam with a set of [options](%/Modules/options.html). Start adds the following processes to the
    [process_list](%/Modules/process_list.html):
     - `load_options` loads the command line options
     - `welcome` displays a welcome message
     - `load_plugins` loads all available plugins
     - `build_files` fixes paths and builds all necessary files
     - `run_commands` prepossesses commands in the template (see [bang](%/Modules/bang.html))
     - `post_status` posts the current state of all options
     - `mix` runs any inline code within the template
     - `parse` reads the template document into an intermediate format (see [formatter](%/Modules/parser_composer.py))
     - `compose` converts the intermediate format into the output format
     - `export` moves files from the tmp directory to the final out directory
     - `cleanup` removes all temporary files
     - `unload_plugins` unloads all available plugins
     - `goodbye` display a goodbye message
    Once added these processes are consumed until there are no more processes.

    :param args: A list of options provided in command line syntax
    :param api: A flag indicating if Pyxam is being called as an api
    """
    # Clear last session data
    store_args(args)
    options.clear()
    process_list.clear()
    # Add api option
    options.add_option('api', '-api', 'Run Pyxam in api mode', True, bool, value=api)
    process_list.append([
        options.load_options,
        welcome,
        plugin_loader.load_plugins,
        options.load_template,
        fileutil.build_files,
        mixer.setup,
        options.post_status,
        parser_composer.parse,
        parser_composer.compose,
        fileutil.export,
        fileutil.cleanup,
        plugin_loader.unload_plugins,
        goodbye])
    while process_list.ready():
        args = process_list.consume(args)


if __name__ == '__main__':
    # If main start Pyxam with argv and API mode False
    # Slice argv so as not to pass ./Pyxam.py
    start(sys.argv[1:], api=False)

def main():
    start(sys.argv[1:], api=False)

