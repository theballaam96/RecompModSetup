import argparse
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--directory", help="Directory of your mod", default=None
    )
    parser.add_argument("-t", "--title", help="Title of your mod", default=None)
    parser.add_argument("-i", "--id", help="Mod ID", default=None)
    parser.add_argument(
        "-dsc", "--description", help="Mod description", default=None
    )
    parser.add_argument(
        "-a", "--authors", help="Authors, delimited by a comma", default=None
    )
    parser.add_argument(
        "-ng",
        "--no_git",
        action="store_true",
        help="If present, will not initialize git submodules",
    )
    args = parser.parse_args()

    # Fallback to interactive prompts if arguments weren't passed via CLI
    directory = args.directory
    if not directory:
        directory = input("Please enter the directory of your mod: ")

    title = args.title
    if not title:
        title = input("Please enter the title of your mod: ")

    mod_id = args.id
    if not mod_id:
        mod_id = input("Please enter the Mod ID: ")

    description = args.description
    if not description:
        description = input("Please enter the description of your mod: ")

    authors = args.authors
    if not authors:
        authors = input(
            "Please enter the authors of your mod, delimited by a comma if there are"
            " multiple: "
        )
    authors = [x.strip() for x in authors.split(",")]

    mod_toml = f"""[manifest]
id = "{mod_id}"
version = "1.0.0"
display_name = "{title}"
description = "{description}"
short_description = "{description[:100]}"
authors = [ {', '.join([f'"{x}"' for x in authors])} ]
game_id = "dk64"
minimum_recomp_version = "1.0.0"

[inputs]
elf_path = "build/mod.elf"
mod_filename = "{mod_id}"
func_reference_syms_file = "Dk64Syms/dump.toml"
data_reference_syms_files = [ "Dk64Syms/data_dump.toml" ]
additional_files = ["thumb.dds"]
"""
    with open("mod.toml", "w") as fh:
        fh.write(mod_toml)

    file_mapping = {
        "gitignore_file.txt": ".gitignore",
        "gitmodules_file.txt": ".gitmodules",
        "license_file.txt": "LICENSE",
        "Makefile": "Makefile",
        "mod.ld": "mod.ld",
        "readme_file.txt": "README.md",
        "build_shell.txt": "build.sh",
        "build_batch.txt": "build.bat",
        "mod.toml": "mod.toml",
    }
    directory_mapping = {
        "include": "include",
        "offline_build": "offline_build",
        "src": "src"
    }

    # Copying files and directories
    cwd = Path.cwd()
    target_path = Path(directory)
    target_path.mkdir(parents=True, exist_ok=True)

    for src_name, dst_name in file_mapping.items():
        src_file = cwd / src_name
        dst_file = target_path / dst_name

        if src_file.is_file():
            shutil.copy2(src_file, dst_file)

    for src_dir, dst_dir in directory_mapping.items():
        src_folder = cwd / src_dir
        dst_folder = target_path / dst_dir

        if src_folder.is_dir():
            if dst_folder.exists():
                shutil.rmtree(dst_folder)
            shutil.copytree(src_folder, dst_folder)

    # Modify Readme
    readme_path = target_path / "README.md"
    if readme_path.is_file():
        content = readme_path.read_text(encoding="utf-8")
        content = content.replace("MOD_TITLE", title)
        content = content.replace("MOD_ID", mod_id)
        content = content.replace("MOD_DESCRIPTION", description)
        readme_path.write_text(content, encoding="utf-8")
        print(f"Successfully modified: {readme_path}")
    # Modify batch
    bat_path = target_path / "build.bat"
    if bat_path.is_file():
        content = bat_path.read_text(encoding="utf-8")
        content = content.replace("fixed_beaver_bother", mod_id)
        bat_path.write_text(content, encoding="utf-8")
        print(f"Successfully modified: {bat_path}")
    # Modify shell
    shell_path = target_path / "build.sh"
    if shell_path.is_file():
        content = shell_path.read_text(encoding="utf-8")
        content = content.replace("fixed_beaver_bother", mod_id)
        shell_path.write_text(content, encoding="utf-8")
        print(f"Successfully modified: {shell_path}")

    if not args.no_git:
        commands = [
            [
                "git",
                "submodule",
                "add",
                "https://github.com/Rainchus/Dk64Syms.git",
                "Dk64Syms",
            ],
            [
                "git",
                "submodule",
                "add",
                "-b",
                "recomp",
                "https://gitlab.com/Rainchus/dk64",
                "dk64_decomp",
            ],
        ]
        for cmd in commands:
            subprocess.run(cmd, cwd=target_path, check=True)


if __name__ == "__main__":
    main()