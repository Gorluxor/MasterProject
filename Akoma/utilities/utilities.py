from form_akoma.Metadata import Metadata


def get_meta(filename: str, path: str = "..//data/meta/allmeta.csv"):
    """

    :param filename: name of scraped document
    :param path: path to metadata csv file
    :return: Metadata.class or None if not found
    """
    csv = open(path, mode="r", encoding="utf-8")
    for line in csv.readlines():
        values = line.strip().split("#")
        if filename == values[14]:
            csv.close()
            return Metadata(values)
    csv.close()
    return None


def get_root_dir():
    from os import path
    pather = path.dirname(__file__)
    path_this = path.normpath(pather)
    i = path_this.rfind("\\")
    b = path_this[:i]
    return b


if __name__ == "__main__":
    a = get_meta("1.html")
    print(a.act_name)

    print(get_root_dir())
    print("End")
