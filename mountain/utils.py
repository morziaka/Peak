def get_path_upload_photo(instance, file):
    return f'photos/pass_{instance.mpass.id}/{file}'