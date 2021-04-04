from os import listdir, fsencode, fsdecode, rename
from os.path import isfile, join


def fix_beginning(name):
    global symbols
    pos = len(name) - 1
    while pos >= 0 and name[pos] != '.':
        pos -= 1
    if pos <= 0 or name[pos] != '.':
        return name
    file_format = name[pos:]
    file_name = name[:pos]

    # try to erase number (ends withs a space)
    pos = 0
    break_point = -1
    for c in name:
        if not ('0' <= c <= '9' or c in symbols):
            break
        if c == ' ':
            break_point = pos
        pos += 1

    # check for symbols at the beginning
    pos = 0
    for c in name:
        if c not in symbols:
            break
        pos += 1

    if max(break_point + 1, pos) < len(file_name):
        return file_name[max(break_point + 1, pos):] + file_format
    else:
        return name


def fix_file_name(name):
    global remove_words
    global replace_words

    for word in remove_words:
        if word in name:
            name = name.replace(word, "")

    for word in replace_words:
        if word in name:
            name = name.replace(word, replace_words[word])

    return fix_beginning(name)


def walker(path):
    global dir_counter
    global changed_counter
    global file_counter
    dir_counter += 1
    for p in listdir(path):
        if not isfile(join(path, p)):
            walker(join(path, p))
        else:
            file_counter += 1
            filename = fsdecode(p)
            new_name = fix_file_name(filename)
            if new_name != filename:
                changed_counter += 1
                rename(join(fsdecode(path), filename), join(fsdecode(path), new_name))


def space_to_underline(word):
    return word.replace(' ', '_')


def space_to_dash(word):
    return word.replace(' ', '-')


def no_spaces(word):
    return word.replace(' ', '')


file_counter = 0
changed_counter = 0
dir_counter = 0

# some of them in the brackets and this is so for a reason
extra_words = ['()', '[]', '(1)', '(2)', '(3)', '320',
               'Radio Edit', 'Album Version', 'Original Mix', 'Complete Version', 'Ultra Music', '(Remix)',
               'Official Music Video',
               'Official Video', 'Official track',
               'Официальный музыкальный клип', 'Официальное видео', 'Клип',
               'Official Lyric Video', 'Lyrics', 'Subtitulada Español', 'Spanish & English Subtitles',
               'English Subtitles',
               'zaycev.net', 'muzofon.com', 'best-muzon.ru',
               'mp3crazy.ru', 'get-tune.net', 'iPlayer.fm',
               'vmusice.net', 'myzuka.ru', 'mp3-you.net',
               'myzuka.fm', 'xMusic.me', 'm.muzofon.com',
               'muz-party.net', 'best-muzon.cc', 'myzuka.me',
               'musicore.net', 'mp3crazy.me', 'pesnik.su']

extra_words_extended = [*[space_to_dash(w) for w in extra_words], *[space_to_underline(w) for w in extra_words],
                        *[no_spaces(w) for w in extra_words]]
extra_words_lowercase = [w.lower() for w in extra_words_extended]
extra_words_uppercase = [w.upper() for w in extra_words_lowercase]

# dict to remove duplicates
extra_words_all_cases = list(
    dict.fromkeys([*extra_words, *extra_words_extended, *extra_words_lowercase, *extra_words_uppercase]))

extra_words_always_square_brackets = ['[' + w + ']' for w in extra_words_all_cases]
extra_words_always_round_brackets = ['(' + w + ')' for w in extra_words_all_cases]
extra_words_brackets = [*extra_words_always_square_brackets, *extra_words_always_round_brackets,
                        *extra_words_all_cases]

extra_words_end_underline = [w + '_' for w in extra_words_brackets]
extra_words_always_underline = [*['_' + w for w in [*extra_words_end_underline, *extra_words_brackets]],
                                *extra_words_end_underline]

extra_words_end_space = [w + ' ' for w in extra_words_brackets]
extra_words_always_space = [*[' ' + w for w in [*extra_words_end_space, *extra_words_brackets]],
                            *extra_words_end_space]
extra_words_space = [*extra_words_always_space, *extra_words_brackets]

extra_words_always_dash = ['-' + w for w in extra_words_space]

# dict to remove duplicates
remove_words = [*extra_words_always_underline, *extra_words_always_dash, *extra_words_space]

file_formats = ['mp3', 'flac', 'm4a']

dot_file_formats = {}

for f in file_formats:
    dot_file_formats[f] = '.' + f

replace_words = {'_-_': ' - ',
                 ' — ': ' - ',
                 '  ': ' '}

symbols = ['.', ',', '_', '-', ' ', '`']
useless_at_the_end = ['[', '(', *symbols]

for f in file_formats:
    replace_words[f + dot_file_formats[f]] = dot_file_formats[f]
    for t in useless_at_the_end:
        replace_words[t + dot_file_formats[f]] = dot_file_formats[f]


def main():
    """
    This program is designed to rename music files.
    It removes:
     - common clarifications (Original Mix, Radio Edit, etc)
     - number at the beginning the name (it usually represents song's number in playlist or album)
     - extra symbols
     - endings like mp3.mp3
     - site names
     - etc
    It also changes '_-_' to ' - ', but does not fix underlines between words
    Note is does not check file's format, i.e. it will rename 1__ - text.txt to text.txt
    Look to program's code to find the exact rules of renaming
    By using this program user confirms that he/she understands damage it can deal to user's file structure
    """
    print(main.__doc__)
    print("WARNING: Changes can't be reversed. Make a backup")
    print("Enter the path to the directory:")

    walker(fsencode(input()))

    print(str(dir_counter) + " directories visited")
    print(str(file_counter) + " files examined")
    print(str(changed_counter) + " files renamed")


if __name__ == "__main__":
    main()
