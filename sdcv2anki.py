#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, argparse, subprocess

STARDICT_DICT_FILE_PATH = os.path.expanduser("~/dic.txt")



def sdcv(word):
    cmd = subprocess.Popen(['sdcv', '-n', word], stdout=subprocess.PIPE)
    out = cmd.stdout.read()
    raw = out.decode('utf-8')
    # dirty hack for latest XML dict format.
    formattedOut = re.sub(r'<[^\!]+?>', r'', raw)
    formattedOut = re.sub(r'<\!\[CDATA\[(.+?)\]\]>', r'\1\n', formattedOut)
    
    formattedOut = re.sub(r'(.+)\n', r'\1<br/>', formattedOut)
    formattedOut = re.sub(r'-->(.+)<br/>-->(.+)<br/>',
                          r"<h5 style='background-color:#666; color:#88bbff; margin:0;'>\1</h5>"\
                          r"<h3 style='background-color:#666; color:#fff; margin:0;'>\2</h3>"
                          , formattedOut)

    formattedOut = re.sub(r'\n', r'<br/>', formattedOut)
    formattedOut = re.sub(r'(<br/>)+', r'<br/>', formattedOut)
    print(formattedOut)
            # print(formattedOut)
    return formattedOut


def process(ARGS):
    FIN = [] # [(word, definition), ...]
    
    with open(STARDICT_DICT_FILE_PATH, 'r') as file:
        while True:
            line = file.readline()
            word = line[0:-1]
            if (not word) or (word == '') :
                break
            print("Processing '{}'...\r".format(word), end="\r")
            FIN.append(word + "\t" + sdcv(word) + "\n")

    export_file_path = os.path.join(os.path.expanduser(ARGS.output_root_directory), ARGS.output_filename)
    with open(export_file_path, 'w') as file:
        file.writelines(FIN)

    print("{} words have been exported to {}".format(len(FIN), export_file_path))
            
        

def parseArguments():
    _parser = argparse.ArgumentParser(
        prog="find_duplicated_files",
        description='Find duplicated files via MD5 checksum and output the list as file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    _parser.add_argument("-o", "--output-filename", nargs="?", metavar="FILE NAME",
                         default='export.txt',
                         help='specify the exporting filename.')
    _parser.add_argument("-r", "--output-root-directory", nargs="?", metavar="ROOT DIR",
                         default='~/Anki/sdcv/',
                         help='specify the root path of exported file.')
    return _parser.parse_args()


def main():
    global ARGS
    ARGS = parseArguments()
    process(ARGS)

if __name__ == '__main__':
    main()
