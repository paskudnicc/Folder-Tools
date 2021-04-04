from os import listdir, fsencode, rename, rmdir
from os.path import isfile, join


def walker(path):
    """
    Unpacks all the folders in folder X to folder X, is not recurring
    Does not merge folders (i.e. a/a/ -> fail)
    """

    for f in listdir(path):
        if not isfile(join(path, f)):
            for p in listdir(join(path, f)):
                rename(join(join(path, f), p), join(path, p))
            rmdir(join(path, f))


if __name__ == "__main__":
    print(walker.__doc__)
    print("WARNING: Changes can't be reversed. Make a backup")
    print("Enter the path to the directory:")
    walker(fsencode(input()))
