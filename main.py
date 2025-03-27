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