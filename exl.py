# -----------------------CHANGES:------------------------------------------------------------------------------------
# mb0520: AAA - only 'cur' files (if older AAA not moved to subdir ==> erroneous regenerate of ARB)
# - - -
# mb0720: with open excel file mode=r --- NOT work on linux, error: "utf-8 cant decode byte ~heb chars~...".
#         utf8 is default encoding in linux, on win=iso-win~~?.  setting encoding=utf-8 does NOT work also on win!
#         possible solutions: encoding='iso-8859-1' (aka latin-1) always works~(stackoverflow) need to check results!
#         or using parm: errors='ignore'/'replace'
# - - -
# MBA720  logger.error(log_ref) ---> `err` set bash rc to ERRONEOUS!   suspicion: if
# MBB720  calibrate file path's: BRWDSK
# -------------------------------------------------------------------------------------------------------------------
import csv
import datetime
import glob
import sys
# import io                 # file manipulation, ~== os.open() in Py3 --- linux,py2 no work!
import time  # sleep
import re  # regex to locate unwanted chars
import os  # chk under which os we run, file I/O
import platform  # chk run platform (server name)

import json
import logging.config

import env.env as env  # CONSTANTS


#
# -----------------------LOG SETUP:----------------------------------------------------------------------------------
# def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
#     path = default_path
#     value = os.getenv(env_key, None)
#     if value:
#         path = value
#     if os.path.exists(path):
#         with open(path, 'rt') as f:
#             config = json.load(f)
#         logging.config.dictConfig(config)
#     else:
#         logging.basicConfig(level=default_level)
#
#
# setup_logging()
# logger = logging.getLogger(__name__)

#
# ------------------------INIT VARS----------------------------------------------------------------------------------
now = datetime.datetime.now()
cur_yymmdd = now.strftime('%y%m%d')

Running = True

# pattern = re.compile('"\d+,\d+,*\d*"')    # " 1_or_more_digits , 1_or_more_digits ,or_not digit_or_not 123,456
#                                                   12,333 1,000,500
pattern = re.compile('".+"')  # " at_least_1_whatever_character "

abends_cnt = 0



#
# -----------------------SET PATH-s:--------------------------------------------------------------------------------
FileFP_AAA_IN_WildCard = env.FILE_PATH_BRWDSK_AAA_IN + 'AAA-IN' + '*' + cur_yymmdd + '.csv'  # mb0520: only 'cur' files!
FileFP_AAA_IN_HANDLED_TXT = env.FILE_PATH_BRWDSK_AAA_IN_EZR + 'ARB-IN________________HANDLED.txt'
FileFP_CTRL = env.FILE_PATH_BRWDSK_AAA_IN_EZR + 'CTRL_exl.txt'

FileFP_ARB_SKM_WildCard = env.FILE_PATH_BRWDSK_ARB_SKM + 'ARB-SKM-D' + cur_yymmdd + '*'  # +'?' and also:  +'*'



#
# -----------------------CHECK MOUNT, C O N T R O L L E R:--------------------------------------------------------
# FOR EACH USED SUB-DIR: NEED TO VERIFY SUCCESSFUL MOUNTING (POTENTIAL ERRORS COULD BE CAUSED BY WRONG MOUNTING/
# CHANGES IN DIR STRUCTURE/ AUTHORISATION CHANGE(SERVER/USER) ETC.
if os.path.isfile(FileFP_AAA_IN_HANDLED_TXT) is False:
    log_ref = '..MOUNT ERR..'
    logger.error('%s %s' % (log_ref, FileFP_AAA_IN_HANDLED_TXT))
    sys.exit()
else:
    log_ref = '..CONTROLLER CHK ON/OFF SWITCH..'
    worker = ''
    with open(FileFP_CTRL, mode='r') as fobj_ctrl:  # CTRL.txt
        run_machine = platform.node().split('.')[0]  # platform.node() ---> 'slddev-app.fibi.corp'
        for buf_fobj_ctrl_line in fobj_ctrl.readlines():  # slpdev - app, worker=0(P)
            if run_machine in buf_fobj_ctrl_line:  # W5180076, worker=1 (win, local)
                worker = buf_fobj_ctrl_line.split('worker=')[1][0]
                logger.info('%s %s' % ('worker=', worker))
                if worker != '1':
                    logger.info('%s ' % (log_ref))
                    sys.exit()
        if worker == '':
            logger.info('%s %s' % (log_ref, 'machine not found in CTRL'))
            sys.exit()

#
# -----------------------HANDLE EXCEL FILES(REMOVE UNNECESSARY COMMAS, "123,456"):--------------------------------
log_ref = '..MAIN PROCESS START..'
logger.info(log_ref)

while Running:
    time.sleep(1)

    log_ref = '..CHK_ARB_SKM..'
    now = datetime.datetime.now()
    now_hh = int(now.strftime('%H'))
    l_ARB_SKM_files = glob.glob(FileFP_ARB_SKM_WildCard)
    if l_ARB_SKM_files:  # <-------------- STOP condition --------------------
        logger.info(l_ARB_SKM_files)
        Running = False
    elif now_hh >= env.MAX_HH_PROC_RUN:  # <-------------- STOP condition --------------------
        log_ref = '..TIME LIMIT REACHED..'
        logger.info(log_ref)  # logger.error(log_ref)  MBA720 ---> `err` set bash rc to ERRONEOUS!
        Running = False
    # MBA720
    elif now.weekday() == 6:  # <-------------- STOP condition --------------------
        log_ref = '..SUNDAY = NO WORK..'
        logger.info(log_ref)
        Running = False








    log_ref = '..MAIN TRY..'
    try:
        l_glob_AAA_csv_files = glob.glob(FileFP_AAA_IN_WildCard)
        for FileFP_csv_in_AAA_glob in l_glob_AAA_csv_files:
            with open(FileFP_AAA_IN_HANDLED_TXT, mode='r') as file_handled_list:
                buf_file_handled_list = file_handled_list.read()

            if FileFP_csv_in_AAA_glob not in buf_file_handled_list:
                with open(FileFP_csv_in_AAA_glob, mode='r', errors='ignore') as f_csv_edit:  # mb0720
                    l_buf_f_csv_edit_readlines = f_csv_edit.readlines()  # each line=list item
                    log_ref = '..CSV LINE CHK..'
                    sw_csv_edited = False
                    buf_f_csv_edit_new = ''
                    cnt_chg_commas = 0
                    cnt_chg_dec_nums = 0
                    for line in l_buf_f_csv_edit_readlines:
                        if not ('ACCOUNT' in line or 'BRANCH' in line or 'AMOUNT' in line):
                            if len(line) != 1:  # "1"=~EOF
                                log_ref = '..REGEX FIND+REPLACE..'
                                re_comma_amount_matches = pattern.findall(line)  # regex find: "12,345"
                                if re_comma_amount_matches:
                                    for match in re_comma_amount_matches:
                                        match_fix = match.replace('"', '')
                                        match_fix = match_fix.replace(',', '')
                                        logger.info('%s ,macth_fix: %s' % (log_ref, match_fix))
                                        line = line.replace(match, match_fix)
                                        sw_csv_edited = True
                                        cnt_chg_dec_nums += 1
                                        logger.info('%s ,C H A N G E D  %s - %s ! ! !' % (log_ref,
                                                                                          match,
                                                                                          match_fix)
                                                    )

                                while line.count(',') > 9:  # unnecessary commas
                                    line = line[::-1].replace(',', '', 1)[::-1]  # reverse + replace_1_occ + reverse
                                    sw_csv_edited = True
                                    cnt_chg_commas += 1

                            buf_f_csv_edit_new += line
                if sw_csv_edited:
                    log_ref = '..SW_CSV_EDITED..'
                    log_info_txt = '%s %s C H A N G E D  %s comma_recs   %s  dec_nums' % (log_ref,
                                                                                          FileFP_csv_in_AAA_glob,
                                                                                          cnt_chg_commas,
                                                                                          cnt_chg_dec_nums
                                                                                          )
                    logger.info(log_info_txt)

            log_ref = '..COPY FILE..'
            FileFP_ARB_new_csv = FileFP_csv_in_AAA_glob.replace('AAA', 'ARB')
            with open(FileFP_ARB_new_csv, mode='w') as f_csv_edit:
                f_csv_edit.write(buf_f_csv_edit_new)

            log_ref = '..WRITE HANDLED.TXT..'
            with open(FileFP_AAA_IN_HANDLED_TXT, mode='a+') as file_handled_list:
                handle_line = '%s %s %s  %s  --write:-->  %s' % (now,
                                                                 log_ref,
                                                                 FileFP_csv_in_AAA_glob,
                                                                 str(sw_csv_edited),
                                                                 FileFP_ARB_new_csv.rsplit(env.str_split_dir)[-1]
                                                                 )
                file_handled_list.write('%s %s' % (handle_line, '\r\n'))
                logger.info(handle_line)

            log_ref = '..MOVE FILE TO OLD DIR..'
            os.rename(FileFP_csv_in_AAA_glob, FileFP_csv_in_AAA_glob.replace(env.FILE_PATH_BRWDSK_AAA_IN,
                                                                             env.FILE_PATH_BRWDSK_AAA_IN_OLD))

except Exception as e:
    logger.error('%s %s' % (log_ref, e))
    abends_cnt += 1
    if abends_cnt > env.MAX_ABENDS_CNT:
        sys.exit()







#
# -----------------------THE END:------------------------------------------------------------------------------------
log_ref = '..MAIN PROCESS END..'
logger.info(log_ref)

