# flacinfo

A script analoguous to `mp3info`, but for flac files.

## Usage

```
usage: flacinfo [-h] [-a ARTIST] [-c COMMENT] [-g GENRE] [-l ALBUM]
                [-m ALBUMNUMBER] [-n TRACK] [-t TITLE] [-y YEAR]
                FILE [FILE ...]

Edit flac files' metadata

positional arguments:
  FILE                  The file(s) to work on

optional arguments:
  -h, --help            show this help message and exit
  -a ARTIST, --artist ARTIST
                        Specify artist name
  -c COMMENT, --comment COMMENT
                        Specify an arbitrary comment
  -g GENRE, --genre GENRE
                        Specify genre (in plain text)
  -l ALBUM, --album ALBUM
                        Specify album name
  -m ALBUMNUMBER, --albumnumber ALBUMNUMBER
                        Specify album number
  -n TRACK, --track TRACK
                        Specify track number
  -t TITLE, --title TITLE
                        Specify track title
  -y YEAR, --year YEAR  Specify album year

When no option modifying the tags is passed, the currently set tags are shown.
```
