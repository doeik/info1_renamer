import sys
import os
import io


def copyShit(filepath, code):
    with io.open(filepath, "w") as bla:
        for line in code:
            bla.write(line)


def fetchSourceCode(filepath):
    with io.open(filepath, "r") as textfile:
        content = textfile.readlines()
    for linecount, line in enumerate(content):
        if "class" in line:
            tmpsplit = line.split()
            for i, substr in enumerate(tmpsplit):
                if substr == "class":
                    classname = tmpsplit[i + 1].replace("{", "")
                    break
            bracket_count = 0
            for i, line2 in enumerate(content[linecount:]):
                bracket_count += line2.count("{")
                bracket_count -= line2.count("}")
                if bracket_count == 0:
                    copyShit(os.path.join(
                        os.path.dirname(filepath), classname + ".java"), content[linecount:linecount + i + 1])
                    break


def findAndReplace(path):
    for dirpath, subdirs, filenames in os.walk(path):
        for name in filenames:
            if name.endswith(".java"):
                old_file = os.path.join(dirpath, name)
                newname = name.replace("upload_", "")
                os.rename(old_file, os.path.join(dirpath, newname))
            elif name.endswith(".txt"):
                fetchSourceCode(os.path.join(dirpath, name))


def main():
    currentDir = "."
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            currentDir = sys.argv[1]
    findAndReplace(currentDir)


if __name__ == "__main__":
    main()
