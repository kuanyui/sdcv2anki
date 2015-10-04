# -*- coding: utf-8 -*-
import os, re, subprocess

STARDICT_DICT_FILE_PATH = os.path.expanduser("~/dic.txt")

def sdcv(word):
    cmd = subprocess.Popen(['sdcv', '-n', word], stdout=subprocess.PIPE)
    output = cmd.stdout.read()
    output = output.decode('utf-8')
    formattedOut = re.sub(r'(.+)\n', r'\1<br/>', output)
    formattedOut = re.sub(r'-->(.+)<br/>-->(.+)<br/>',
                          r"<h5 style='background-color:#666; color:#88bbff; margin:0;'>\1</h5>"\
                          r"<h3 style='background-color:#666; color:#fff; margin:0;'>\2</h3>"
                          , formattedOut)
    formattedOut = re.sub(r'\n', r'<br/>', formattedOut)
            # print(formattedOut)
    return formattedOut

FIN = [] # [(word, definition), ...]

with open(STARDICT_DICT_FILE_PATH, 'r') as file:
    while True:
        line = file.readline()
        word = line[0:-1]
        if (not word) or (word == '') :
            break
        print("Processing '{}'...\r".format(word), end="\r")
        FIN.append(word + "\t" + sdcv(word) + "\n")

with open(os.path.join(os.path.expanduser(ARGS.output_root_directory), ARGS.output_filename), 'w') as file:
    file.writelines(FIN)
        
    

def parseArguments():
    _parser = argparse.ArgumentParser(
        prog="find_duplicated_files",
        description='Find duplicated files via MD5 checksum and output the list as file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    _parser.add_argument("-o", "--output-filename", nargs="?", metavar="FILE NAME",
                         default='export.txt',
                         help='specify the file whose contains duplicated files list.')
    _parser.add_argument("-r", "--output-root-directory", nargs="?", metavar="DIR",
                         default='~/Anki/sdcv/',
                         help='specify the file whose contains duplicated files list.')
    return _parser.parse_args()


def main():
    global ARGS
    ARGS = parseArguments()

if __name__ == '__main__':
    main()
