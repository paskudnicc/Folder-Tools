from os import listdir, fsencode, fsdecode, rename
from os.path import isfile, join


def walker_base_creator(path):
    for p in listdir(path):
        if not isfile(join(path, p)):
            walker_base_creator(join(path, p))
        else:
            filename = fsdecode(p)
            names_set.add(filename)
            names_dir_dict[filename] = fsdecode(path)


def walker_restorer(path):
    for p in listdir(path):
        if not isfile(join(path, p)):
            walker_restorer(join(path, p))
        else:
            filename = fsdecode(p)
            possible_variants = []
            for var in names_set:
                if filename in var:
                    if var in filename and not resolve_manually:
                        continue
                    possible_variants.append(var)
            if len(possible_variants) == 1:
                rename(join(fsdecode(path), filename), join(fsdecode(path), possible_variants[0]))
            elif 1 < len(possible_variants) <= max_suggestions:
                print("[Empty line to skip] Corrupted name: " + filename + ' (' + fsdecode(path) + ')')
                n = 0
                for var in possible_variants:
                    n += 1
                    print("#" + str(n) + " " + var + ' (' + names_dir_dict[var] + ')')
                chosen_number = input()
                if chosen_number.strip():
                    x = int(chosen_number)
                    rename(join(fsdecode(path), filename), join(fsdecode(path), possible_variants[x - 1]))


names_set = set()
names_dir_dict = {}
max_suggestions = 10
resolve_manually = False

print("WARNING: Consider making a backup")
print("Enter list of directories from which to create base of filenames")
print("[S to open settings, empty line to end input]")

while True:
    s = input()
    if not s.strip():
        break
    if s == 'S' or s == 's':
        print("Default limit of suggestions: 10, type another number if you want to, or leave it")

        s = input()
        if s.strip():
            max_suggestions = int(s)

        print("Resolve conflicts manually when exact match exists? I.E 'Name', suggestions: 'Name', 'SomeName'. [Y/N]")

        s = input()
        if s.strip():
            if s == 'Y' or s == 'y':
                resolve_manually = True

    else:
        walker_base_creator(fsencode(s))

print("Enter the directory where to repair filenames")

walker_restorer(fsencode(input()))
