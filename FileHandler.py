import glob


class FileHandler:

    def __init__(self, logger):
        self.logger = logger
        self.log_ref = ''

    #
    #
    def get_out_filename(self, file_fp_search_wildcard):
        out_filename = ''

        try:
            l_glob_fnd_files = glob.glob(file_fp_search_wildcard)
            if len(l_glob_fnd_files) is 1:
                out_filename = l_glob_fnd_files[0]

        except Exception as e:
            self.logger.error(e)

        return out_filename
