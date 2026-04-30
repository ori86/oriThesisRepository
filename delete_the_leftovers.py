from pathlib import Path

def main():
    current_dir = Path.cwd()

    # Delete only .csv files in the current folder, not recursively
    for item in current_dir.iterdir():
        if item.is_file() and item.suffix.lower() == ".csv":
            item.unlink()
            #print(f"Deleted CSV: {item.name}")
    print("csv files are deleted")
    # Delete all files inside asm_debug, but not subfolders
    asm_debug_dir = current_dir / "asm_debug"

    if asm_debug_dir.exists() and asm_debug_dir.is_dir():
        for item in asm_debug_dir.iterdir():
            if item.is_file():
                item.unlink()
                #print(f"Deleted from asm_debug: {item.name}")
        print("asm files are deleted")

    else:
        print("asm_debug folder not found.")



if __name__ == '__main__':
    main()