'''common functions'''

import os
import subprocess
import re


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
    if not os.path.isfile(in_path):
        print("Warning: File not found:", self.imagefile)
        return

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # using cp -u
    cp_command = ['cp', '-u', in_path, out_dir]

    exitcode = subprocess.call(cp_command)


def url_encode_str(string):
    # 1) convert spaces to dashes
    dashed = re.sub(r'[\ ]', '-', string)
    # 2) only accept [^a-zA-Z0-9-]
    #    replace everything else by %
    alnum_dashed = re.sub(r'[^a-zA-Z0-9-]', '-', dashed)
    # 3) lowercase
    return alnum_dashed.lower()


def sort_pages(pages):
    try:
        pages.sort(key=lambda k: k.title)
    except AttributeError:
        print("Warning: Bad title, can't properly sort...")
        pass
    try:
        pages.sort(key=lambda k: k.date_obj.timestamp())
    except AttributeError:
        print("Warning: Bad date, can't properly sort...")
        pass
    return pages
