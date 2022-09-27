#!/home/emil/Apps/epics/R7.0.4.1/work/ioc/SISSY2EX/SISSY2_PWR_00/remote_pwr/bin/python3
# EASY-INSTALL-ENTRY-SCRIPT: 'cothread==2.18.1','console_scripts','pvtree.py'
__requires__ = 'cothread==2.18.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('cothread==2.18.1', 'console_scripts', 'pvtree.py')()
    )
