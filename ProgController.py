import os
import platform                                                         # chk run platform (server name)
import sys


class ProgController:

    def __init__(self, logger, sw_exit_on_err):
        self.mount_vld = False
        self.ctrl_vld = False
        self.logger = logger
        self.log_ref = ''
        self.cur_prog_name = self.logger.extra.get('app_name')          # get prog name from logger extra var
        self.sw_exit_on_err = sw_exit_on_err

    #
    #
    def chk_mount(self, l_folders):
        # FOR EACH USED SUB-DIR: NEED TO VERIFY SUCCESSFUL MOUNTING (POTENTIAL ERRORS COULD BE CAUSED BY WRONG MOUNTING/
        # CHANGES IN DIR STRUCTURE/ AUTHORISATION CHANGE(SERVER/USER) ETC.
        try:
            if l_folders is not []:
                for folder in l_folders:
                    if os.path.exists(folder) is False:
                        self.log_ref = '**ERROR MOUNT**'
                        self.logger.info('%s %s' % (self.log_ref, folder))
                        self.mount_vld = False
                        break
                    else:
                        self.mount_vld = True

        except Exception as e:
            self.logger.error('%s %s' % (self.log_ref, e))
            self.mount_vld = False                  # in case of error AFTER setting ok

        self.chk_mount_exit()

    #
    #
    def chk_mount_exit(self):
        if self.mount_vld is False:
            sys.exit()

    #
    #
    def chk_controller(self, ctrl_folder):
        self.ctrl_vld = False
        worker = ''
        self.log_ref = '..CONTROLLER: PROGRAM ON/OFF SWITCH..'

        try:
            file_fp_ctrl = ctrl_folder + 'CTRL___' + self.cur_prog_name + '.txt'
            run_machine = platform.node().split('.')[0]                     # platform.node() ---> 'slddev-app.fibi.corp'

            with open(file_fp_ctrl, mode='r') as fobj_ctrl:
                for buf_fobj_ctrl_line in fobj_ctrl.readlines():            # slpdev - app, worker=0(P)
                    if run_machine in buf_fobj_ctrl_line:                   # W5180076, worker=1 (win, local)
                        worker = buf_fobj_ctrl_line.split('worker=')[1][0]
                        if worker is '1':
                            self.ctrl_vld = True
                            break
                if worker == '':
                    self.logger.info('%s %s' % (self.log_ref, 'machine not found in CTRL'))

        except Exception as e:
            self.logger.error('%s %s' % (self.log_ref, e))
            self.ctrl_vld = False                  # in case of error AFTER setting ok

        self.chk_controller_exit()

    #
    #
    def chk_controller_exit(self):
        if self.sw_exit_on_err is True:
            if self.ctrl_vld is False:
                sys.exit()
