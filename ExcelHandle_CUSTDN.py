# -----------------------CHANGES:------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------------------------
from LogManager import LogManager
from MailManager import MailManager
from ProgController import ProgController

from ExcelHandler import ExcelHandler
import sys                                      # cur prog


# ------------------------INIT VARS----------------------------------------------------------------------------------

cur_prog_name = sys.argv[0].split('.')[0]

Running = True

l_folders_chk_mnt = []


def main():
    lm = LogManager(cur_prog_name)
    logger = lm.get_logger()
    logger.info('..MAIN PROCESS START..')
    sw_exit_on_err = True

    # pc = ProgController(logger, env.FILE_PATH_CONTROLLER, sw_exit_on_err)
    pc = ProgController(logger, '/home/mon', sw_exit_on_err)
    exl_type, input_folder, output_file = pc.chk_parm(sys.argv)
    l_folders_chk_mnt.append(input_folder)
    pc.chk_mount(l_folders_chk_mnt)
    # pc.chk_run_controller()

    mm = MailManager(logger)
    # m a i l e r   inheritance?
    # m a i l e r   inheritance?

    # fh = FileHandler(logger, input_folder, exl_type)
                        # df_ifile_read, col_list, val_conv = fh.handle_input_file()
    # fh.handle_input_file()

    # eh = ExcelHandler(logger, df_ifile_read, col_list, val_conv)
    # eh = ExcelHandler(logger, fh)
    eh = ExcelHandler(logger, input_folder, exl_type, output_file)
    eh.exl_handle()

    logger.info('**MAIN PROCESS END**')


#
if __name__ == '__main__':
    main()