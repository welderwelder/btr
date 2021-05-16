# -----------------------CHANGES:------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------------------------

from LogManager import LogManager
from MailManager import MailManager
from ProgController import ProgController
from FileHandler import FileHandler
from ExcelHandler import ExcelHandler
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

    pc = ProgController(logger, sw_exit_on_err)
    pc.chk_mount(l_folders_chk_mnt)
    # pc.chk_run_controller('/home/mona/PycharmProjects/btr/')    # env.FILE_PATH_CONTROLLER
    exl_type = pc.chk_parm(sys.argv)

    mm = MailManager(logger)
    # m a i l e r   inheritance?
    # m a i l e r   inheritance?

    fh = FileHandler(logger)
    # TODO:
    # FileFP_INPUT_WildCard should be decided by json(?) by exl_type~~
    l_ifile_buf_csvreadlns = fh.read_csv_input_file(FileFP_INPUT_WildCard)

    eh = ExcelHandler(logger, l_ifile_buf_csvreadlns, exl_type)
    eh.exl_handle()


#
#
if __name__ == '__main__':
    main()