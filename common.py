'''common functions'''

import os
import subprocess


def pandoc_pipe(content, opts):
    '''Create a pandoc pipe reading from a variable and returning the output.'''

    pandoc_command = [ 'pandoc' ] + opts

    proc = subprocess.Popen( pandoc_command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE )
    input = content.encode()
    out, err = proc.communicate(input=input)
    output = out.decode('utf-8')

    return output


def write_out(content, outfile):
    '''Write out content to file.'''

    out_dir = os.path.dirname(outfile)

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    with open(outfile, 'w') as outfile_o:
        outfile_o.write(content)


def copy_file(in_path, out_dir):
    '''Call copy w/o preset directories.
(Not recursive.)
--> shutil.copy could be used for this.'''
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # using cp -u
    cp_command = ['cp', '-u', in_path, out_dir]

    exitcode = subprocess.call(cp_command)
