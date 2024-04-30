import os
import sys

# First, attempt to load the entviz package from the system.
# If it fails, try loading it from the source tree.
try:
    from entviz.app import main
except ModuleNotFoundError:
    MY_FOLDER = os.path.normpath(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
    sys.path.insert(0, os.path.normpath(os.path.join(MY_FOLDER, '..')))
    from entviz.app import main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('')
