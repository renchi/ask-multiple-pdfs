import os
import sys
def makedirs(path, exist_ok=True, tmp_ok=False, use_base=False):
    """
    Avoid some inefficiency in os.makedirs()
    :param path:
    :param exist_ok:
    :param tmp_ok:  use /tmp if can't write locally
    :param use_base:
    :return:
    """
    if path is None:
        return path
    # if base path set, make relative to that, unless user_path absolute path
    if use_base:
        if os.path.normpath(path) == os.path.normpath(os.path.abspath(path)):
            pass
        else:
            if os.getenv('GPT_BASE_PATH') is not None:
                base_dir = os.path.normpath(os.getenv('GPT_BASE_PATH'))
                path = os.path.normpath(path)
                if not path.startswith(base_dir):
                    path = os.path.join(os.getenv('GPT_BASE_PATH', ''), path)
                    path = os.path.normpath(path)

    if os.path.isdir(path) and os.path.exists(path):
        assert exist_ok, "Path already exists"
        return path
    try:
        os.makedirs(path, exist_ok=exist_ok)
        return path
    except FileExistsError:
        # e.g. soft link
        return path
    except PermissionError:
        if tmp_ok:
            path0 = path
            path = os.path.join('/tmp/', path)
            print("Permission denied to %s, using %s instead" % (path0, path), flush=True)
            os.makedirs(path, exist_ok=exist_ok)
            return path
        else:
            raise