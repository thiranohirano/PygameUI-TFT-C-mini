# coding=utf-8
import pygame
import pygameuic as ui

class TestUI(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)

        scroll_rect = ui.col_rect_mini(0, 1, 8, 4)
        # self.ap_listview = ui.StringListView(pygame.Rect(0, 0, scroll_rect.w, scroll_rect.h), ["hoge1", "hoge2"], row_num=0)
        #
        # self.scroll_view = ui.ScrollView(scroll_rect, self.ap_listview)
        # self.ap_listview.minimize = self.scroll_view.content_frame.rect.size
        self.scroll_view = ui.ScrollStringListView(scroll_rect, ["hoge1", "hoge2"])
        self.scroll_view.on_selected.connect(self.hoge)
        self.add_child(self.scroll_view)

        btn = ui.Button(ui.col_rect_mini(7, 0, 1, 1), 'X')
        btn.on_clicked.connect(self.back)
        self.add_child(btn)

    def back(self, btn):
        dummies = ["h", "ho", "hog", "hoge", "hogehoge"]
        self.scroll_view.string_items = dummies
        self.scroll_view.content_offset = (0, 0)

    def hoge(self, slv, item, index):
        print index
