import gzip, io, os, logging, zipfile

# making everything accessible from the root of the package
from .db import init_session, session_scope
from .time import Timer

logger = logging.getLogger(__name__)


def open(filename, *args, **kwargs):
    """ Open different types of files based on the extension """
    if filename.endswith('.gz'):
        return gzip.open(filename, *args, **kwargs)
    elif filename.endswith('.zip'):
        z = zipfile.ZipFile(filename)
        names = z.namelist()
        if len(names) != 1:
            print(filename)
            print(names)
            raise ValueError('.zip files containing more than one file are not'
                             ' supported')
        return io.TextIOWrapper(z.open(names[0], 'rU'))
    else:
        return io.open(filename, *args, **kwargs)


def are_you_sure(msg='Are you sure?'):
    """ prompts and asks if sure to do X
    """
    while True:
        choice = input(msg + ' (Y/N) ')
        if choice == 'Y':
            return True
        elif choice == 'N':
            return False


def ask_before_overwrite(filename):
    """ if `filename` already exists, will prompt before overwriting """
    return not os.path.exists(filename) or are_you_sure(
        u'The file {} already exists. Overwrite?'.format(filename))
