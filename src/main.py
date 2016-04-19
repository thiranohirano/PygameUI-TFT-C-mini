"""
Created on 2016/03/03

@author: hirano
"""
import sys
import os
import pygame
import pygameuic as ui  # @UnresolvedImport
import startui
import pifiui
import mytheme

if __name__ == '__main__':
    param = sys.argv
    mouse_flag = True
    fullscreen = False
    if len(param) > 1:
        for arg_param in param:
            if arg_param == "-tft":
                mouse_flag = False
                fullscreen = True
            if arg_param == "-startup":
                os.putenv('SDL_FBDEV', '/dev/fb1')
                os.putenv('SDL_MOUSEDRV', 'TSLIB')
                os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    ui.init('pygameui ', (320, 240), mouse_flag, fullscreen)
    mytheme.set_theme()
    ui.append_scene(startui.StartScene())
    ui.append_scene(pifiui.PifiUI())
    ui.use_scene(0)
    ui.run()