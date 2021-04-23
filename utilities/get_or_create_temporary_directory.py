import os

def get_temporary_directory(file_of_calling_program, dir_name=".cache"):
    """
    Make sure that the temp directory, '.temp_data' exists and if not is created. This is created in the path of the
    calling program.

    :param file_of_calling_program: Use __file__ when calling
    :return: the temporary directory
    """

    script_dir = os.path.dirname(file_of_calling_program)
    cache_dir = os.path.join(script_dir, dir_name)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    return cache_dir
