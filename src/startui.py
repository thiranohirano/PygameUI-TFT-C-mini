# -*- coding:utf-8 -*-
"""
Created on 2016/03/03

@author: hirano
"""
import time
import pygame
import mycolors
import pygameuic  as ui  # @UnresolvedImport
import socket
from subprocess import PIPE, Popen
import threading


class StartScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
        self.main_frame = ui.ObjectRectangle(
            ui.window.rect)
        self.main_frame.enabled = False
        self.main_frame.border_color = mycolors.belize_hole
        self.main_frame.border_widths = 9
        self.add_child(self.main_frame)

        self.ip_label = ui.Label(ui.col_rect_mini(0, 0, 8, 1), self.get_ip())
        self.add_child(self.ip_label)

        self.obj_r = ui.Button(ui.col_rect_mini(0, 1, 3, 1), 'Proc')
        self.obj_r.on_clicked.connect(self.hoge)
        self.add_child(self.obj_r)

        self.obj_r2 = ui.Button(ui.col_rect_mini(0, 2, 3, 1), 'vkey')
        self.obj_r2.on_clicked.connect(self.hoge2)
        self.add_child(self.obj_r2)

        self.obj_r4 = ui.Button(ui.col_rect_mini(5, 1, 3, 2), 'WiFi')
        self.obj_r4.on_clicked.connect(self.wifi_button)
        self.add_child(self.obj_r4)

        self.reboot_btn = ui.Button(ui.col_rect_mini(0, 4, 3, 2), 'Reboot')
        self.reboot_btn.on_clicked.connect(self.reboot_button_click)
        self.add_child(self.reboot_btn)

        self.shutdown_btn = ui.Button(ui.col_rect_mini(5, 4, 3, 2), 'Shutdown')
        self.shutdown_btn.on_clicked.connect(self.shutdown_button_click)
        self.add_child(self.shutdown_btn)

    def hoge(self, obj):
        self.show_process_spinner(self.search_process, 'Scanning for WiFi networks...')

    def hoge2(self, obj):
        text = self.show_virtual_keyboard()
        print text

    @staticmethod
    def wifi_button(obj):
        ui.use_scene(1)

    def reboot_button_click(self, btn):
        #         self.add_fullscreen_label("Reboot...")
        self.show_process_message("Reboot...", 2)
        ui.quit()

    def shutdown_button_click(self, btn):
        self.show_process_message("Shutdown...", 2)
        threading.Timer(1, self.shutdown_process).start()
        #         self.add_fullscreen_label("Shutdown...")
        ui.quit()

    def add_fullscreen_label(self, text):
        label = ui.Label(ui.col_rect(0, 0, 12, 8), text)
        label.font = pygame.font.SysFont('Courier New', 28, bold=True)
        self.add_child(label)
        return label

    def shutdown_process(self):
        self.shutdown()

    # Get Your External IP Address
    def get_ip(self):
        ip_msg = "Not connected"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.connect(('<broadcast>', 0))
            ip_msg = u"IPアドレス:" + s.getsockname()[0]
        except Exception:
            pass
        return ip_msg

    # Restart Raspberry Pi
    def restart(self):
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]
        return output

    def dummyrestart(self):
        time.sleep(1)

    # Shutdown Raspberry Pi
    def shutdown(self):
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]
        return output

    def search_process(self):
        print 'hoge'
        time.sleep(3)
        print 'hoge'
