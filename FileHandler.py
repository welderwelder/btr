import glob
import csv
import sys
import datetime


class FileHandler:

    def __init__(self, logger, input_folder):
        self.logger = logger
        self.log_ref = ''
        self.file_status = 0
        self.input_folder = input_folder
        self.input_filename = ''

    def get_input_filename(self):
        now = datetime.datetime.now()
        cur_yymmdd = now.strftime('%y%m%d')
        #
        # *** bash script needs to `prepare` filenames for **globe**ease of use**: stick `AAA-IN` prefix + timestamp
        #
        file_fp_search_wildcard = self.input_folder + 'AAA-IN' + '*' + cur_yymmdd + '*'
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

    def chk_warn_err_input_file_exit(self):
        try:
            if self.file_status == 0:
                # TODO: mail(not found)
                self.logger.error('%s %s %s' % (self.input_folder, self.input_filename, self.file_status))
                sys.exit()
            elif self.file_status == 2:
                # TODO: mail(multi)
                self.logger.error('%s %s %s' % (self.input_folder, self.input_filename, self.file_status))
                sys.exit()

        except Exception as e:
            self.logger.error(e)

    def vld_read_csv_input_file(self):
        try:
            self.get_input_filename()

            self.chk_warn_err_input_file_exit()

            with open(self.input_filename, mode='r', errors='ignore') as i_file:
                # l_ifile_buf_csvreadlns = i_file.readlines()                            # each line=list item
                csv_rdr_obj = csv.reader(i_file)
                # TODO: csv.DictReader ?
        except Exception as e:
            self.logger.error('%s %s %s' % (e, self.input_filename, self.input_folder))

        # return l_ifile_buf_csvreadlns
        return csv_rdr_obj

