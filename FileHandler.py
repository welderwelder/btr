import glob
import csv
import sys
import datetime
import pandas as pd
import json
from pathlib import Path
import os


class FileHandler:

    def __init__(self, logger, input_folder, exl_type):
        self.logger = logger
        self.log_ref = ''
        self.file_status = 0
        self.input_folder = input_folder
        self.exl_type = exl_type
        self.input_filename = ''
        self.input_filename_no_path = ''
        self.output_filename = ''
        self.col_list = []
        self.df_ifile_read = None
        self.val_conv = None
        self.file_owner = ''


    def get_input_filename(self):
        now = datetime.datetime.now()
        cur_yymmdd = now.strftime('%y%m%d')
        #
        # *** bash script needs to `prepare` filenames for **globe**ease of use**: stick `AAA-IN` prefix + timestamp
        #
        file_fp_search_wildcard = self.input_folder + 'AAA-IN-' + cur_yymmdd + '*'
        try:
            l_glob_fnd_files = glob.glob(file_fp_search_wildcard)
            if len(l_glob_fnd_files) is 1:
                self.input_filename = l_glob_fnd_files[0]
                self.file_status = 1
            elif len(l_glob_fnd_files) is 0:
                self.file_status = 0
            else:
                self.file_status = 2
        except Exception as e:
            self.logger.error(e)


    def vld_file_status(self):
        try:
            if self.file_status == 0:
                # TODO: mail(not found)
                self.logger.error('%s %s %s' % (self.input_folder, self.input_filename, self.file_status))
                sys.exit()
            elif self.file_status == 2:
                # TODO: mail(multi)
                self.logger.error('%s %s %s' % (self.input_folder, self.input_filename, self.file_status))
                sys.exit()
            else:
                path = Path(self.input_filename)
                self.file_owner = path.owner()
                self.input_filename_no_path = os.path.basename(path)

        except Exception as e:
            self.logger.error(e)


    def read_ifile(self):
        try:
            with open(self.input_filename, mode='r', errors='ignore', encoding='iso-8859-8') as i_file:
                # DataFrame !!!
                self.df_ifile_read = pd.read_csv(i_file)
                # https://www.kite.com/python/answers/how-to-read-specific-column-from-csv-file-in-python
                # https://www.youtube.com/watch?v=vmEHCJofslg
                # print(self.df_ifile_read)
                # ifile_read = i_file.readlines()                            # each line=list item
                # csv_rdr_obj = csv.reader(i_file)
                # print(next(csv_rdr_obj))
        except Exception as e:
            self.logger.error('%s %s %s' % (e, self.input_filename, self.input_folder))

    def save_output_file(self, df_new):
        try:
            self.output_filename = self.input_filename.replace('AAA', 'BBB')
            # with open(self.output_filename, mode='r', errors='ignore', encoding='iso-8859-8') as i_file:
            #     self.df_ifile_read = pd.read_csv(i_file)
            df_new.to_csv(self.output_filename, index=False, header=False)
            # pass
        except Exception as e:
            self.logger.error('%s %s %s' % (e, self.input_filename, self.input_folder))


    def get_col_list(self):
        try:
            file_fp_get_col_list = self.input_folder + '/EZR/col_list.json'
            with open(file_fp_get_col_list, mode='r', errors='ignore') as exl_types_jfile:
                col_list_json = json.load(exl_types_jfile)
                self.col_list = col_list_json.get(self.exl_type)
        except Exception as e:
            self.logger.error('%s %s %s' % (e, file_fp_get_col_list, self.input_folder))


    def get_val_conversion(self):
        try:
            file_fp_get_val_conv = self.input_folder + '/EZR/val_conv.json'
            with open(file_fp_get_val_conv, mode='r', errors='ignore', encoding='iso-8859-8') as val_conv_jfile:
                self.val_conv = json.load(val_conv_jfile)
        except Exception as e:
            self.logger.error('%s %s %s' % (e, file_fp_get_val_conv, self.input_folder))


    def handle_input_file(self):

        self.get_input_filename()

        self.vld_file_status()

        self.read_ifile()

        self.get_col_list()

        self.get_val_conversion()

        # return self.df_ifile_read, self.col_list, self.val_conv


    def set_output(self):
        # TODO:
        pass

