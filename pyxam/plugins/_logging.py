# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin _logging

This plugin is considered a core plugin (indicated by the underscore in its name) it should only be replaced or removed
if the user knows what they are doing.



This plugin sets the logging configuration for Pyxam. The default value for logging is hardcoded but a command line
option is added to allow the user to set the logging level at runtime. The [plugin_loader](%/Modules/plugin_loader) will
always load _logging first so that other Plugins can use logging
in their load functions.
"""

import logging
import options

# logging config by ejrbuss: The default logging configuration for pyxam
signature = 'logging config', 'ejrbuss', 'The default logging configuration for pyxam'

# Logging option description
description = 'Set the logging level for pyxam\n{}: DEBUG\n{}: INFO\n{}: WARNING\n{}: CRITICAL'.format(
    logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL
)

# Default logging level
default = logging.DEBUG


def load():
    """
    Loads the following [option](%/Modules/options.html):
     - `logging -l` Set the logging level for pyxam
    Sets logging.basicConfig with a default format and sets it to the option value.

    :return: plugin signature
    """
    options.add_option('logging', '-l', description, default, int)
    # Set logging configuration
    logging.basicConfig(format='%(levelname)s@%(module)s.%(funcName)s(): %(message)s', level=options.state.logging())
    # Log configuration
    logging.info('Logging configured with level {}'.format(logging.getLevelName(options.state.logging())))
    # Return signature
    return signature
