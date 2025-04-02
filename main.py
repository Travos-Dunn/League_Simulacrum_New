import versions
import items
import champions

def main() -> None:
    CHAMP_NAME = "Ahri"
    LEVEL = 18

    BUILD = {
        "3118",
        "3089",
        "3135",
        "3020"
    }

    version = versions.check_version()
    files = versions.update_filenames(version)

    item_data = items.check_items(files["item_data"], version)
    item_list = items.check_item_list(files["item_list"], files["item_data"], version)

    champ_data = champions.check_champs(files["champ_data"], version)
    champ_list = champions.check_champ_list(files["champ_list"], files["champ_data"], version)

if __name__ == "__main__":
    main()
