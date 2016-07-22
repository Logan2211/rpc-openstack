#!/usr/bin/env python

# Copyright 2015, Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess
import sys

from maas_common import metric_bool
from maas_common import print_output
from maas_common import status_err
from maas_common import status_ok


def check_process_running(process_names):
    """
    Check if each of the processes in process_names is in a list of running
    processes on this host
    """

    procs = []
    # for proc in process_iter():
    try:
        # Create a list of only names of running process
        procs = [p['name'] for p in
            [proc.as_dict(attrs=['name'])for proc in process_iter()]]
    except (AccessDenied, NoSuchProcess, ZombieProcess):
        pass
    except:
        status_err('Could not get a list of running processes')

    # Since we've fetched a process list, report status_ok.
    status_ok()

    # Report the presence of each process in the running process list
    for process_name in process_names:
        metric_bool('%s_process_status' % process_name,
                    process_name in procs)


def main():
    args = sys.argv[1:]
    if not args:
        status_err('No executable names supplied')

    check_process_running(args)


if __name__ == "__main__":
    with print_output():
        main()
