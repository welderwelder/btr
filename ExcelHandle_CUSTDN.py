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
# ***
# *** bash script needs to `prepare` filenames for **globe**ease of use**: stick `AAA-IN` prefix + timestamp
# ***
l_folders_chk_mnt = []
# FileFP_INPUT_WildCard = env.FILE_PATH_CUSTDN_INPUT + 'AAA-IN' + '*' + cur_yymmdd + '*'
l_folders_chk_mnt.append('/home/mona/')
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
    sw_exit_on_err = True

    #
    prog_ctrl = ProgController(logger, sw_exit_on_err)
    prog_ctrl.chk_mount(l_folders_chk_mnt)
    prog_ctrl.chk_controller('/home/mona/PycharmProjects/btr/')    # env.FILE_PATH_CONTROLLER

    #
    file_handler = FileHandler(logger)
    l_ifile_csvreadlns = file_handler.read_csv_input_file(FileFP_INPUT_WildCard)


#
#
if __name__ == '__main__':
    main()