# -----------------------CHANGES:------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------------------------

from LogManager import LogManager
from ProgController import ProgController
from FileHandler import FileHandler
import sys                                      # cur prog
import datetime


#
# ------------------------INIT VARS----------------------------------------------------------------------------------
now = datetime.datetime.now()
cur_yymmdd = now.strftime('%y%m%d')
cur_prog_name = sys.argv[0].split('.')[0]

Running = True

#
# -----------------------SET PATH-s:--------------------------------------------------------------------------------
# bash script needs to `prepare` filenames for **globe**ease of use**: stick `AAA-IN` prefix + timestamp
l_folders = []
# FileFP_INPUT_WildCard = env.FILE_PATH_CUSTDN_INPUT + 'AAA-IN' + '*' + cur_yymmdd + '*'
l_folders.append('/home/mona/')
FileFP_INPUT_WildCard = '/home/mona/PycharmProjects/btr/' + 'AAA-IN' + '*' + cur_yymmdd + '*'

## FileFP_CTRL = env.FILE_PATH_BRWDSK_AAA_IN_EZR + 'CTRL_exl.txt'
# FileFP_CTRL = env.FILE_PATH_CONTROLLER + 'CTRL_exl_CUSTDN.txt'
#
# FileFP_ARB_SKM_WildCard = env.FILE_PATH_BRWDSK_ARB_SKM + 'ARB-SKM-D' + cur_yymmdd + '*'  # +'?' and also:  +'*'


#
#
def main():
    lm = LogManager(cur_prog_name)
    logger = lm.get_logger()
    logger.info('..MAIN PROCESS START..')

    prog_ctrl = ProgController(logger)
    prog_ctrl.chk_mount(l_folders)
    if prog_ctrl.mount_vld is False:
        sys.exit()
    prog_ctrl.chk_controller('/home/mona/PycharmProjects/btr/')    # env.FILE_PATH_CONTROLLER
    if prog_ctrl.ctrl_vld is False:
        sys.exit()

    file_handler = FileHandler(logger)
    file_handler.get_out_filename(FileFP_INPUT_WildCard)


#
#
if __name__ == '__main__':
    main()