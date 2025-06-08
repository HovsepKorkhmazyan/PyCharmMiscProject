import os


def get_cnt(fname):
    try:
        with open(fname) as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{fname}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def create_univ_obj(line):
    tmp = {}
    data = line.strip().split()
    if len(data) < 4:
        print(f"Warning: Line '{line.strip()}' does not contain enough data.")
        return None
    tmp["Name"] = data[0]
    tmp["Year"] = data[1]
    tmp["Location"] = data[2]
    tmp["Students"] = data[3]
    return tmp


def get_univ_list(ml):
    univ = []
    for line in ml:
        university = create_univ_obj(line)
        if university:
            univ.append(university)
    return univ


def create_univ_files(ulist, fpath):
    for university in ulist:
        filename = os.path.join(fpath, university["Name"].lower() + ".txt")
        with open(filename, "w") as f:
            for k, v in university.items():
                f.write(f"{k} : {v}\n")


def main():
    fname = "data.txt"
    fcnt = get_cnt(fname)
    universities = get_univ_list(fcnt)

    if not universities:
        print("No valid university data to process.")
        return

    cwd = os.getcwd()
    dirname = "universities"
    full = os.path.join(cwd, dirname)

    if not os.path.isdir(full):
        os.mkdir(full)

    create_univ_files(universities, full)

    print(f"Successfully created {len(universities)} university files in '{full}'")


if __name__ == "__main__":
    main()
