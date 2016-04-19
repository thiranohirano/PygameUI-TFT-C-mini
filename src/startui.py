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
import os
import datetime

class StartScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
        # self.main_frame = ui.ObjectRectangle(
        #     ui.window.rect)
        # self.main_frame.enabled = False
        # self.main_frame.border_color = mycolors.belize_hole
        # self.main_frame.border_widths = 9
        # self.add_child(self.main_frame)

        self.ip_label = ui.Label(ui.col_rect_mini(0, 0, 8, 1), self.get_ip())
        self.add_child(self.ip_label)

        self.date_label = ui.Label(ui.col_rect_mini(0, 1, 5, 1, padding=2), '', halign=ui.LEFT)
        self.date_label.font = pygame.font.Font(ui.resource.get_font_path("VL-PGothic-Regular"), 24)
        self.add_child(self.date_label)

        self.time_label = ui.Label(ui.col_rect_mini(0, 2, 5, 2), '', halign=ui.LEFT)
        self.time_label.font = pygame.font.Font(ui.resource.get_font_path("VL-PGothic-Regular"), 48)
        self.add_child(self.time_label)

        self.obj_r = ui.Button(ui.col_rect_mini(5, 3, 3, 1), 'Proc')
        self.obj_r.on_clicked.connect(self.hoge)
        self.add_child(self.obj_r)

        self.obj_r2 = ui.Button(ui.col_rect_mini(5, 4, 3, 1), 'vkey')
        self.obj_r2.on_clicked.connect(self.hoge2)
        self.add_child(self.obj_r2)

        self.obj_r4 = ui.Button(ui.col_rect_mini(5, 1, 3, 2), 'WiFi')
        self.obj_r4.on_clicked.connect(self.wifi_button)
        self.add_child(self.obj_r4)

        # self.reboot_btn = ui.Button(ui.col_rect_mini(0, 4, 3, 2), 'Reboot')
        # self.reboot_btn.on_clicked.connect(self.reboot_button_click)
        # self.add_child(self.reboot_btn)

        # self.shutdown_btn = ui.Button(ui.col_rect_mini(5, 4, 3, 2), 'Shutdown')
        # self.shutdown_btn.on_clicked.connect(self.shutdown_button_click)
        # self.add_child(self.shutdown_btn)

        self.stop_flag = False

        scriptdir = os.path.dirname(os.path.abspath(__file__))
        print scriptdir
        images_folder = "images"
        self.power_image = pygame.image.load(os.path.join(scriptdir, images_folder, "appbar.power.png")).convert_alpha()
        self.shutdown_img_btn = ui.ImageButton(ui.col_rect_mini(7, 5, 1, 1, margin=1, padding=1), self.power_image)
        self.shutdown_img_btn.on_clicked.connect(self.shutdown_button_click)
        self.add_child(self.shutdown_img_btn)

        self.refresh_image = pygame.image.load(os.path.join(scriptdir, images_folder, "appbar.refresh.png")).convert_alpha()
        self.change_lxde_img_btn = ui.ImageButton(ui.col_rect_mini(0, 5, 1, 1, margin=1, padding=1), self.refresh_image)
        self.change_lxde_img_btn.on_clicked.connect(self.change_lxde_btn_click)
        self.add_child(self.change_lxde_img_btn)

    def loaded(self):
        self.ip_label.text = self.get_ip()
        datetime_now = datetime.datetime.now()
        self.date_label.text = datetime_now.strftime('%Y/%m/%d')
        self.time_label.text = datetime_now.strftime('%H:%M')
        self.stop_flag = False
        ip_timer = threading.Timer(2, self.show_ip)
        ip_timer.start()
        datetime_timer = threading.Timer(1, self.show_datetime)
        datetime_timer.start()
        print "loaded"

    def closed(self):
        self.stop_flag = True
        print "closed"

    def show_ip(self):
        self.ip_label.text = self.get_ip()
        if not self.stop_flag:
            ip_timer = threading.Timer(2, self.show_ip)
            ip_timer.start()

    def show_datetime(self):
        datetime_now = datetime.datetime.now()
        self.date_label.text = datetime_now.strftime('%Y/%m/%d')
        self.time_label.text = datetime_now.strftime('%H:%M')
        if not self.stop_flag:
            datetime_timer = threading.Timer(1, self.show_datetime)
            datetime_timer.start()

    def hoge(self, obj):
        self.show_process_spinner(self.search_process, 'Scanning for WiFi networks...')

    def hoge2(self, obj):
        text = self.show_virtual_keyboard()
        print text

    @staticmethod
    def wifi_button(obj):
        ui.use_scene(1)

    def change_lxde_btn_click(self, btn):
        self.show_process_message("Change LXDE...", 2)
        ui.quit()

    def shutdown_button_click(self, btn):
        ui.use_scene(2)

    # Get Your External IP Address
    @staticmethod
    def get_ip():
        ip_msg = "Not connected"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.connect(('<broadcast>', 0))
            ip_msg = u"IPアドレス:" + s.getsockname()[0]
        except Exception:
            pass
        return ip_msg

    @staticmethod
    def search_process():
        print 'hoge'
        time.sleep(3)
        print 'hoge'
