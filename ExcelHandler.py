# import sys


class ExcelHandler:

    def __init__(self, logger, l_ifile_buf_csvreadlns, exl_type):
        self.logger = logger
        self.log_ref = ''
        self.l_ifile_buf_csvreadlns = l_ifile_buf_csvreadlns

    def chk_title_line(self):
        l_line1_split_cma =  self.l_ifile_buf_csvreadlns[0].split(',')
        # if not ('ACCOUNT' in line1 or 'BRANCH' in line or 'AMOUNT' in line):
        # return
        pass

    def rmv_title_line(self):
        try:
            pass
        except Exception as e:
            self.logger.error(e)

    def handle_title_line(self):
        if self.chk_title_line():
            self.rmv_title_line()

    def chk_fields_count(self):
        try:
            for line in l_buf_f_csv_edit_readlines:
                print(line)
                # if not ('ACCOUNT' in line or 'BRANCH' in line or 'AMOUNT' in line):
                #     if len(line) != 1:  # "1"=~EOF
                #         log_ref = '..REGEX FIND+REPLACE..'
                #         re_comma_amount_matches = pattern.findall(line)  # regex find: "12,345"
                #         if re_comma_amount_matches:
                #             for match in re_comma_amount_matches:
                #                 match_fix = match.replace('"', '')
                #                 match_fix = match_fix.replace(',', '')
                #                 logger.info('%s ,macth_fix: %s' % (log_ref, match_fix))
                #                 line = line.replace(match, match_fix)
                #                 sw_csv_edited = True
                #                 cnt_chg_dec_nums += 1
                #                 logger.info('%s ,C H A N G E D  %s - %s ! ! !' % (log_ref,
                #                                                                   match,
                #                                                                   match_fix)
                #                             )
                #
                #         while line.count(',') > 9:  # unnecessary commas
                #             line = line[::-1].replace(',', '', 1)[::-1]  # reverse + replace_1_occ + reverse
                #             sw_csv_edited = True
                #             cnt_chg_commas += 1
                #
                #     buf_f_csv_edit_new += line
        except Exception as e:
            self.logger.error(e)

    def exl_handle(self):
        self.handle_title_line()
