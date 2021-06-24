import re
import argparse
import pathlib
import sys

# setup argparse
parser = argparse.ArgumentParser(description='Edits the specified file changing the desired html comments to php imports and creating a new file with the changes applied.')
parser.add_argument('file', type=pathlib.Path)

args = parser.parse_args()
filename = args.file.resolve()

# try to open the specified file if possible
try:
    with open(filename, 'r') as file:
        text = file.read()
except PermissionError:
    print('Permission denied\n')
    sys.exit(0)

# find all the matches for the part that should be corrected
matches = [i for i in re.findall('<!--\[html-partial:include:{\"file\":[^\s]+}\]/-->', text)]


# for every match ask the user if it has to be corrected or not
for i in matches:

    # ask the user if the current string has to be corrected
    print("Do you wnt to correct this? (y/n)")
    print(i)
    r = None
    while r != 'n' and r != 'N' and r != 'y' and r != 'Y':
        r = input('> ')
    
    if r == 'y' or r == 'Y':
        # find the beginning and the end of the string to be corrected
        index = text.find(i)
        fine = index + len(i)

        # get the name of the file to be included
        name = re.findall('file\":\"([^\s]+)\"}\]\/-->', i)[0]
        # change the extention from .html to .php
        name = name.replace('.html', '.php')

        # edit only the right part of the text
        newText = text[:index] + f'<? include("{name}"); ?>' + text[fine:]
        text = newText

# write the changes to a new file in the same directory as the original one
with open(str(filename.parent) + '/corrected_' + filename.name, 'w') as f:
    f.write(text)
