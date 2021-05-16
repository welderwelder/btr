import glob
import csv
import sys


class FileHandler:

    def __init__(self, logger):
        self.logger = logger
        self.log_ref = ''
        self.file_status = 0

    #
    #
    def get_input_filename(self, file_fp_search_wildcard):
        filename = ''

        try:
            l_glob_fnd_files = glob.glob(file_fp_search_wildcard)
            if len(l_glob_fnd_files) is 1:
                filename = l_glob_fnd_files[0]
                self.file_status = 1
            elif len(l_glob_fnd_files) is 0:
                self.file_status = 0
            else:
                self.file_status = 2

        except Exception as e:
            self.logger.error(e)

        return filename

    #
    #
    def chk_warn_err_input_file_exit(self):

        try:
            if self.file_status == 0:
                # mail(not found)
                sys.exit()
            elif self.file_status == 2:
                # mail(multi)
                sys.exit()

        except Exception as e:
            self.logger.error(e)

    #
    #
    def read_csv_input_file(self, file_fp_search_wildcard):

        try:
            input_filename = self.get_input_filename(file_fp_search_wildcard)

            self.chk_warn_err_input_file_exit()

            with open(input_filename, mode='r', errors='ignore') as i_file:
                l_ifile_csvreadlns = i_file.readlines()                            # each line=list item

        except Exception as e:
            self.logger.error('%s %s' % (e, file_fp_search_wildcard))

        return l_ifile_csvreadlns

