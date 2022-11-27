from zipfile import ZipFile


def get_zip_assets(zip_file: ZipFile):
    # List is used so that the totals can be displayed properly (for tqdm)
    # Could probably be a bit slower but a bit better on memory by doing an object with len and iter but like. who cares
    return list(filter(lambda file: file.filename.startswith(r'assets/'), zip_file.filelist))
