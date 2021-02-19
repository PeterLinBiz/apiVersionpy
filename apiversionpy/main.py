# BSD 3-Clause License
#
# Copyright (c) 2021, Peter Lin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
apiVersionpy

This apiVersionpy is a tool to upgrade apiVersion of Salesforce DX 
source format projects written using Python.

try - Only generate report files.
run - Change to new apiVersion, e.g. '51'.

Usage:
  main.py try [options]
  main.py run [options]
  main.py (-h | --help)
  main.py --version

Options:
  -d, --path=PATH   The path to the Salesforce DX Project.
  -t, --temppath=TEMPPATH (Default: 'temp') TEMPPATH for generated temporary report files.
  -n, --newversion=NEWVERSION   The new apiVersion, e.g. '51'.
  -h, --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
from pathlib import Path
from lxml import etree


def main(docopt_argv):
    parser = etree.XMLParser()
    print(docopt_argv)
    print('\n')
    print(docopt_argv['--path'])
    p = Path(docopt_argv['--path'])
    set_version(p, '**/*.cls-meta.xml')
    set_version(p, '**/*.cmp-meta.xml')
    set_version(p, '**/*.page-meta.xml')


def set_version(_path=None, _glob_type=''):
    version_files = _path.glob(_glob_type)
    print(version_files)
    print(type(version_files))
    for vf in version_files:
        print(vf)
        tree = etree.parse(str(vf))
        root = tree.getroot()
        for element in root.iter(r'{*}apiVersion'):
            print(element.tag)
            print(element.text)
            element.text = '51.0'
            print('Modified \n')
            print(element.tag)
            print(element.text)
        tree.write(str(vf),  encoding="UTF-8",
                             pretty_print=True,
                             doctype=r'<?xml version="1.0" encoding="UTF-8"?>')
        print(etree.tostring(tree, encoding="UTF-8",
                             pretty_print=True,
                             doctype=r'<?xml version="1.0" encoding="UTF-8"?>'))
        print('\n')


if __name__ == '__main__':
    arguments = docopt(__doc__, version='apiVersionpy 21.219.0.1')
    # print(arguments)
    main(arguments)
