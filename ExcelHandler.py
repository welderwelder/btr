import sys
import csv
import datetime
from FileHandler import FileHandler


class ExcelHandler:

    # def __init__(self, logger, csv_rdr_obj, exl_type):
    # def __init__(self, logger, df_ifile_read, col_list, val_conv):
    def __init__(self, logger, input_folder, exl_type, output_file):
        self.logger = logger
        self.log_ref = ''
        self.input_folder = input_folder
        self.exl_type = exl_type

        self.fh = FileHandler(logger, input_folder, exl_type)
        self.fh.handle_input_file()

        self.df_ifile_read = self.fh.df_ifile_read               # DataFrame
        self.col_list = self.fh.col_list
        self.val_conv = self.fh.val_conv

        self.output_file = output_file
        self.df_new = None


    def normalize_fields(self):
        try:
            # df_new = self.df_ifile_read[[                 # Use loc to slice subsets, will not raise warning
            df_new = self.df_ifile_read.loc[:, [
                                                 "order",
                                                 "custody_rate",
                                                 "bank_code",
                                                 "branch_code",
                                                 "acc_code",
                                                 "asset_code",
                                                 "vol"
                                                 ]]

            # df.loc[(df.Event == 'Dance'), 'Event'] = 'Hip-Hop'
            # df["column1"].replace({"a": "x", "b": "y"}, inplace=True)
            # df_new["order"].replace({"קניה": "108", "b": "y"}, inplace=True)
            df_new["order"].replace(self.val_conv, inplace=True)

            df_new["rec_type"] = 2

            now = datetime.datetime.now()
            cur_yymmdd = now.strftime('%Y%m%d')
            df_new["date"] = cur_yymmdd
            df_new["next_date"] = ''
            df_new["transmit"] = '2'                       # "2"=with transmit
            df_new["f12"] = ''
            df_new["f13"] = ''
            df_new["contrary-bank-f14"] = ''
            df_new["contrary-branch-f15"] = ''
            df_new["contrary-acc-f16"] = ''
            cur_ts = now.strftime('%y.%m.%d-%H:%M:%S')
            dspace = '  '
            desc = ''.join([self.fh.input_filename_no_path, dspace,
                            cur_ts, dspace,
                            self.exl_type, dspace,
                            self.fh.file_owner
                            ])
            df_new["desc"] = desc

            column_names = [
                            "rec_type",                     # 1
                            "order",                        # 2
                            "transmit",                     # 3
                            "date",                         # 4
                            "next_date",                    # 5
                            "custody_rate",                 # 6
                            "bank_code",                    # 7
                            "branch_code",                  # 8
                            "acc_code",                     # 9
                            "asset_code",                   # 10
                            "vol",                          # 11
                            "f12",                          # 12
                            "f13",                          # 13
                            "contrary-bank-f14",            # 14
                            "contrary-branch-f15",          # 15
                            "contrary-acc-f16",             # 16
                            "desc"                          # 17
                            ]
            df_new = df_new.reindex(columns=column_names)                   # df = df[["C", "A", "B"]]

            print(df_new)
            self.df_new = df_new

        except Exception as e:
            self.logger.error(e)
            sys.exit()


    def handle_title_line(self):
        # if self.chk_title_line():
        #     self.rmv_title_line()
        self.df_ifile_read.columns = self.col_list
        # print(self.df_ifile_read)


    def exl_handle(self):

        self.handle_title_line()

        self.normalize_fields()

        self.fh.save_output_file(self.df_new)


    #
    # def chk_title_line(self):
    #     l_line1_split_cma = self.df_ifile_read[0].split(',')
    #     print(l_line1_split_cma)
    #     # fields = next(self.csv_rdr_obj)
    #     # print(fields)
    #     # if not ('ACCOUNT' in line1 or 'BRANCH' in line or 'AMOUNT' in line):
    #     pass

    # def rmv_title_line(self):
    #     try:
    #         pass
    #     except Exception as e:
    #         self.logger.error(e)

    # def chk_fields_count(self):
    #     try:
    #         for line in l_buf_f_csv_edit_readlines:
    #             print(line)
    #             # if not ('ACCOUNT' in line or 'BRANCH' in line or 'AMOUNT' in line):
    #             #     if len(line) != 1:  # "1"=~EOF
    #             #         log_ref = '..REGEX FIND+REPLACE..'
    #             #         re_comma_amount_matches = pattern.findall(line)  # regex find: "12,345"
    #             #         if re_comma_amount_matches:
    #             #             for match in re_comma_amount_matches:
    #             #                 match_fix = match.replace('"', '')
    #             #                 match_fix = match_fix.replace(',', '')
    #             #                 logger.info('%s ,macth_fix: %s' % (log_ref, match_fix))
    #             #                 line = line.replace(match, match_fix)
    #             #                 sw_csv_edited = True
    #             #                 cnt_chg_dec_nums += 1
    #             #                 logger.info('%s ,C H A N G E D  %s - %s ! ! !' % (log_ref,
    #             #                                                                   match,
    #             #                                                                   match_fix)
    #             #                             )
    #             #
    #             #         while line.count(',') > 9:  # unnecessary commas
    #             #             line = line[::-1].replace(',', '', 1)[::-1]  # reverse + replace_1_occ + reverse
    #             #             sw_csv_edited = True
    #             #             cnt_chg_commas += 1
    #             #
    #             #     buf_f_csv_edit_new += line
    #     except Exception as e:
    #         self.logger.error(e)
