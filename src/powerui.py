# coding=utf-8

import pygameuic as ui
from subprocess import PIPE, Popen
import threading
import window_scene

class PowerUI(window_scene.WindowScene):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.shutdown_btn = ui.Button(ui.col_rect_mini(2, 1, 4, 2), 'Shutdown')
        self.shutdown_btn.on_clicked.connect(self.shutdown_btn_click)
        self.add_child(self.shutdown_btn)

        self.reboot_btn = ui.Button(ui.col_rect_mini(2, 3, 4, 2), 'Reboot')
        self.reboot_btn.on_clicked.connect(self.reboot_btn_click)
        self.add_child(self.reboot_btn)

    def shutdown_btn_click(self, btn):
        self.show_process_message("Shutdown...", 2)
        threading.Timer(2, self.shutdown_process).start()
        ui.quit()
        command = "/usr/bin/sudo service lightdm stop"
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]

    def shutdown_process(self):
        self.shutdown()

    def reboot_btn_click(self, btn):
        self.show_process_message("Reboot...", 2)
        threading.Timer(2, self.reboot_process).start()
        ui.quit()
        command = "/usr/bin/sudo service lightdm stop"
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]

    def reboot_process(self):
        self.restart()

    # Restart Raspberry Pi
    @staticmethod
    def restart():
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]
        return output

    # Shutdown Raspberry Pi
    @staticmethod
    def shutdown():
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]
        return output