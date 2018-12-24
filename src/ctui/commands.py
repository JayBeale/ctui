"""
Control Things User Interface, aka ctui.py

# Copyright (C) 2017-2019  Justin Searle
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details at <http://www.gnu.org/licenses/>.
"""

import shlex
import re
import time
from prompt_toolkit.application.current import get_app
from prompt_toolkit.document import Document
from tabulate import tabulate
from os.path import expanduser


class Commands(object):
    """Commands that users may use at the application prompt."""
    # Each function that users can call must:
    #     - start with a do_
    #     - accept self, input_text, output_text, and event as params
    #     - return a string to print, None, or False
    # Returning a False does nothing, forcing users to correct mistakes


    def execute(self, input_text, output_text, event):
        """Extract command and call appropriate function."""
        parts = input_text.strip().split(maxsplit=1)
        command = parts[0].lower()
        if len(parts) == 2:
            arg = parts[1]
        else:
            arg = ''
        try:
            func = getattr(self, 'do_' + command)
        except AttributeError:
            return False
        return func(arg, output_text, event)


    def commands(self):
        commands = [a[3:] for a in dir(self.__class__) if a.startswith('do_')]
        return commands


    def meta_dict(self):
        meta_dict = {}
        for command in self.commands():
            # TODO: find a better way to do this than eval
            meta_dict[command] = eval('self.do_' + command + '.__doc__')
        return meta_dict


    def do_clear(self, input_text, output_text, event):
        """Clear the screen."""
        return ''


    def do_help(self, input_text, output_text, event):
        """Print application help."""
        output_text += '==================== Help ====================\n'
        output_text += 'Welcome to Control Things User Interface, or ctui.\n\n'
        output_text += 'You can replace this help message by setting '
        output_text += 'get_app.help equal to whatever text you wish \n\n'
        table = []
        for key, value in self.meta_dict().items():
            table.append([key, value])
        output_text += tabulate(table, tablefmt="plain") + '\n'
        output_text += '==============================================\n'
        return output_text


    def do_history(self, input_text, output_text, event):
        """Print current history."""
        output_text += str(event.current_buffer.go_to_history(0))
        return output_text


    def do_exit(self, input_text, output_text, event):
        """Exit the application."""
        event.app.exit()
        output_text += 'Closing application.\n'
        return output_text
