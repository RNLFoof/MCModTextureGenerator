from zipfile import ZipFile


def get_zip_assets(zip_file: ZipFile):
    return list(filter(lambda file: file.filename.startswith(r'assets/'), zip_file.filelist))