import os

def creating_folders(names: list):
    if not os.path.isdir("dataset"):
        os.mkdir("dataset")
    os.chdir("dataset")
    if not os.path.isdir(names[0]) and not os.path.isdir(names[1]):
        os.makedirs(names[0])
        os.makedirs(names[1])

def main() -> None:
    name1, name2 = "rose", "tulip"
    creating_folders((name1, name2))

if __name__ == "__main__":
    main()