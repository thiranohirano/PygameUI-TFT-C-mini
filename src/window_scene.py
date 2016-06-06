# coding=utf-8

import pygameuic as ui

class WindowScene(ui.Scene):

    def __init__(self):
        ui.Scene.__init__(self)

        btn = ui.Button(ui.col_rect_mini(7, 0, 1, 1, padding=3), 'X')
        btn.on_clicked.connect(self.back)
        self.add_child(btn)

    def back(self, btn):
        ui.use_scene(0)
