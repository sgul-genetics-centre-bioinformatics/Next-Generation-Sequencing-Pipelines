import os
import sys
import os
import multiprocessing
import subprocess
import time
from optparse import OptionParser
from capturer import CaptureOutput

def parallel_command(command, n=2, wordir=os.getcwd()+'/', name='log.txt'):
    """
    Function that takes a list of linux commands as its argument, instructs the linux system to run them
    one by one in parallel using the required amount of processors and capturing the output into a log file.
    :param command: List (Required). List of Linux commands that will be running.
    :param n: Integer (Optional). Number of processors will be used. Default to 2.
    :param wordir: String (Optional). Full pathname of the place where the log file will be saved to. Default
    to the current working directory. Should always finish with an '/'.
    :param name: String (Optional). Name of the output log file. Default to log.txt
    """
    processes = set()
    max_processes = n
    with CaptureOutput() as capturer:
        for i in range(0, len(command)):
            processes.add(subprocess.Popen(command[i], shell=True))
            if len(processes) >= max_processes:
                os.wait()
                processes.difference_update([p for p in processes if p.poll() is not None])

        for p in processes:
            if p.poll() is None:
                p.wait()

    text_file = open(wordir + name, "a+")
    text_file.write("\n" + capturer.get_text())
    text_file.close()
    return

def get_files_with_suffix(dir, suffix1='', suffix2='', inside_word='', mindepth=False):
    """Function that will iterate through the files of a directory and will return a list
    of the full pathnames of the files fulfilling the requirements set with the below parameters.
    :param dir: String (Required). The directory of which the files you want to iterate through. Should always finish with an '/'
    :param suffix1: String (Optional). The prefix you want the files of the dir to START with.
    Default is None: the function will not look for files starting with a particular prefix.
    :param suffix2: String (Optional). The suffix you want the files of the dir to END with.
    Default is None: the function will not look for files ending with a particular suffix.
    :param inside_word: String (Optional). A particular string you want to be included within the
    filenames of the dir. Default is None: the function will not look for files having the given inside word.
    :param mindepth: Boolean (Optional). True: Search for files in all subdirectories of the dir.
    False: Only search for files within dir. Default to False.
    :return: A list of all the files meeting the requirements set above.
    """
    if mindepth==False:
        rfiles = [dir + x for x in os.listdir(dir) if
                  x.startswith(suffix1) and inside_word in x and x.endswith(suffix2)]
    if mindepth==True:
        temp = []
        for path, subdirs, files in os.walk(dir, followlinks=True):
            for name in files:
                temp.append(os.path.join(path, name))
        rfiles = [x for x in temp if x.startswith(suffix1) and inside_word in x and x.endswith(suffix2)]
    rfiles.sort()
    return(rfiles)