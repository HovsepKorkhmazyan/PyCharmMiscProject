import os

def main():
    dir_path = "dir1"
    output_file = "results.txt"

    if not os.path.isdir(dir_path):
        print(f"Directory '{dir_path}' not found.")
        return

    with open(output_file, "w") as outfile:
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write("\n")

    print(f"Compiled contents written to '{output_file}'.")

if __name__ == "__main__":
    main()
