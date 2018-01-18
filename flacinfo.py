#!/usr/bin/env python3

"""
flacinfo

A script analoguous to `mp3info`, allowing one to easily tag their music
collection, but for flac files.
"""

import argparse
import subprocess
import os
import sys


VORBIS_ARG_NAME = {
    'title': 'TITLE',
    'track': 'TRACKNUMBER',
    'artist': 'ARTIST',
    'album': 'ALBUM',
    'albumnumber': 'DISCNUMBER',
    'genre': 'GENRE',
    'year': 'DATE',
    'comment': 'COMMENT',
}


class NoSuchTag(Exception):
    def __init__(self, tag):
        self.tag = tag
        super(NoSuchTag, self).__init__()

    def __str__(self):
        return "No such Vorbis tag {}".format(self.tag)


def argparser():
    """ Parses the arguments from sys.argv """
    parser = argparse.ArgumentParser(
        description="Edit flac files' metadata",
        epilog=('When no option modifying the tags is passed, the currently '
                'set tags are shown.'))
    parser.add_argument('-a', '--artist',
                        help="Specify artist name")
    parser.add_argument('-c', '--comment',
                        help="Specify an arbitrary comment")
    parser.add_argument('-g', '--genre',
                        help="Specify genre (in plain text)")
    parser.add_argument('-l', '--album',
                        help="Specify album name")
    parser.add_argument('-m', '--albumnumber',
                        help="Specify album number")
    parser.add_argument('-n', '--track',
                        help="Specify track number")
    parser.add_argument('-t', '--title',
                        help="Specify track title")
    parser.add_argument('-y', '--year',
                        help="Specify album year")
    parser.add_argument('file', nargs='+', metavar='FILE',
                        help="The file(s) to work on")
    return parser.parse_args()


def is_flac_file(path):
    """ Checks whether `path` refers to an existing, writeable flac file """
    if not os.path.isfile(path) or not os.access(path, os.W_OK):
        return False
    flac_run = subprocess.run(['metaflac', '--list', path],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    if flac_run.returncode != 0:
        return False  # Metaflac failed to list the files' metadata

    return True


def make_metaflac_args(in_args):
    out_args = []

    for arg in in_args:
        arg_val = in_args[arg]
        if arg not in VORBIS_ARG_NAME or arg_val is None:
            continue
        arg_name = VORBIS_ARG_NAME[arg]

        out_args.append('--remove-tag={}'.format(arg_name))
        out_args.append("--set-tag={}={}".format(arg_name, arg_val))

    return out_args


def edit_flac(args):
    """ Perfoms the requested edition operations """
    metaflac_args = make_metaflac_args(args)
    metaflac_args += args['file']
    metaflac_args.insert(0, 'metaflac')
    metaflac_run = subprocess.run(metaflac_args)

    if metaflac_run.returncode != 0:
        print(('\n\nMetaflac exited with return code {}. There was an error '
               'during the execution, you should look at the output to '
               'investigate it.').format(metaflac_run.returncode),
              file=sys.stderr)
        sys.exit(metaflac_run.returncode)


def reverse_tag(vorbis_tag):
    """ Reverses a Vorbis tag to an argument name """
    for tag in VORBIS_ARG_NAME:
        if VORBIS_ARG_NAME[tag] == vorbis_tag:
            return tag
    raise NoSuchTag(vorbis_tag)


def get_tags(path):
    """ Retrieves the relevant tags for a single file """
    metaflac_args = ['metaflac']
    for tag in VORBIS_ARG_NAME:
        metaflac_args += ['--show-tag', VORBIS_ARG_NAME[tag]]
    metaflac_args.append(path)

    metaflac_run = subprocess.run(metaflac_args, stdout=subprocess.PIPE)
    meta_out = metaflac_run.stdout.decode('utf-8')
    output = {}

    for line in meta_out.split('\n'):
        split = line.split('=')
        tag, value = split[0], '='.join(split[1:])
        if not tag:
            continue
        tag = reverse_tag(tag)
        output[tag] = value
    return output


def show_tags(path):
    """ Shows the relevant tags already present in the given flac file """
    tags = get_tags(path)
    print("File: {}".format(path))

    max_len = max([len(tag) for tag in tags])
    for tag in tags:
        print(' {}: {}{}'.format(tag, ' '*(max_len - len(tag)), tags[tag]))
    print("")


def main():
    args = vars(argparser())

    has_errors = False
    for cur_file in args['file']:
        if not is_flac_file(cur_file):
            print(("Error: file {} does not exist, or is not writeable by "
                   "metaflac").format(cur_file),
                  file=sys.stderr)
            has_errors = True
    if has_errors:
        print("One or more file cannot be manipulated. Aborting.",
              file=sys.stderr)
        sys.exit(1)

    edit_mode = False
    for tag in VORBIS_ARG_NAME:
        if args[tag] is not None:
            edit_mode = True
            break

    if edit_mode:
        edit_flac(args)
    else:
        for path in args['file']:
            show_tags(path)


if __name__ == '__main__':
    main()
