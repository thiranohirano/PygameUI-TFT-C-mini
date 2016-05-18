# coding=utf-8
import pygame
import object_rectangle
import button
import imagebutton
import resource

SCROLL_BUTTON_HEIGHT = 16

def get_relative_point(point1, rect, add_point=(0, 0)):
    x, y = point1
    return x - rect.x + add_point[0], y - rect.y + add_point[1]

class ScrollFrame(object_rectangle.ObjectRectangle):
    def __init__(self, rect, content_view):
        object_rectangle.ObjectRectangle.__init__(self, rect)
        self.content_view = content_view
        self.border_widths = self.content_view.border_widths
        self.border_color = self.content_view.border_color
        self.content_view.border_widths = 0
        self.content_view.border_color = None
        self.content_view.rect.w -= self.border_widths * 2
        self.content_view.rect.h -= self.border_widths * 2
        self.items = []
        self.items.append(self.content_view)
        self.selected_index = None

    def all_dirty_item(self):
        self.content_view.dirty = True

    def mouse_down(self, point):
        relative_point = get_relative_point(point, self.rect, (-self.border_widths, -self.border_widths))
        for index, item in enumerate(self.items):
            item_rect = pygame.Rect(self.rect.x, self.rect.y + item.rect.y, item.rect.w, item.rect.h)
            if item_rect.collidepoint(point):
                self.select(index)
                item.mouse_down(relative_point)
                break

    def mouse_up(self, point):
        relative_point = get_relative_point(point, self.rect)
        for index, item in enumerate(self.items):
            item_rect = pygame.Rect(self.rect.x, self.rect.y + item.rect.y, item.rect.w, item.rect.h)
            if item_rect.collidepoint(point):
                self.deselect()
                item.mouse_up(relative_point)
                break

    def deselect(self):
        if self.selected_index is not None:
            self.items[self.selected_index].selected = False
        self.selected_index = None

    def select(self, index):
        self.deselect()
        self.selected_index = index

        if index is not None:
            item = self.items[self.selected_index]
            item.selected = True

    def _draw(self, screen):
        if not object_rectangle.ObjectRectangle._draw(self, screen):
            return False

        self.all_dirty_item()
        items_surface = pygame.Surface(
            (self.rect.w - self.border_widths * 2, self.rect.h - self.border_widths * 2)).convert()

        self.content_view.draw_blit(items_surface)
        self.surface.blit(items_surface, (self.border_widths, self.border_widths))
        return True

class ScrollView(object_rectangle.ObjectRectangle):

    def __init__(self, frame, content_view):
        # height = frame.size[1] + SCROLL_BUTTON_HEIGHT * 2
        # rect = pygame.Rect(frame.x, frame.y - SCROLL_BUTTON_HEIGHT, frame.w, height)
        rect = frame
        object_rectangle.ObjectRectangle.__init__(self, rect)

        self.content_frame = ScrollFrame(pygame.Rect(0, SCROLL_BUTTON_HEIGHT, frame.w, frame.h - SCROLL_BUTTON_HEIGHT * 2), content_view)
        self.content_view = content_view
        self._content_offset = (0, 0)

        # self.up_btn = button.Button(pygame.Rect(0, 0, rect.w, SCROLL_BUTTON_HEIGHT), u"△")
        # self.up_btn.border_widths = None
        self.up_image = resource.get_image("up")
        self.up_btn = imagebutton.ImageButton(pygame.Rect(0, 0, rect.w, SCROLL_BUTTON_HEIGHT), self.up_image, pygame.Rect(0, 0, SCROLL_BUTTON_HEIGHT * 2, SCROLL_BUTTON_HEIGHT * 2))
        self.up_btn.on_clicked.connect(self.up)
        # self.down_btn = button.Button(pygame.Rect(0, rect.h - SCROLL_BUTTON_HEIGHT, rect.w, SCROLL_BUTTON_HEIGHT), u"▽")
        # self.down_btn.border_widths = None
        self.down_image = resource.get_image("down")
        self.down_btn = imagebutton.ImageButton(pygame.Rect(0, rect.h - SCROLL_BUTTON_HEIGHT, rect.w, SCROLL_BUTTON_HEIGHT), self.down_image, pygame.Rect(0, 0, SCROLL_BUTTON_HEIGHT * 2, SCROLL_BUTTON_HEIGHT * 2))
        self.down_btn.on_clicked.connect(self.down)

        self.items = []
        self.items.append(self.up_btn)
        self.items.append(self.down_btn)
        self.items.append(self.content_frame)

        self.selected_index = None

    @property
    def content_offset(self):
        return self._content_offset

    @content_offset.setter
    def content_offset(self, new_offset):
        self._content_offset = new_offset
        self.content_view.rect.topleft = self._content_offset
        self.dirty = True

    def up(self, btn):
        x, y = self._content_offset
        y += 20
        if y > 0:
            y = 0
        self._content_offset = (x, y)
        self.content_view.rect.topleft = self._content_offset

    def down(self, btn):
        x, y = self._content_offset
        y -= 20
        if y < self.content_frame.rect.h - self.content_view.rect.h:
            y = self.content_frame.rect.h - self.content_view.rect.h
            if y > 0:
                y = 0
        self._content_offset = (x, y)
        self.content_view.rect.topleft = self._content_offset

    def all_dirty_item(self):
        for item in self.items:
            item.dirty = True

    def mouse_down(self, point):
        relative_point = get_relative_point(point, self.rect)
        for index, item in enumerate(self.items):
            item_rect = pygame.Rect(self.rect.x, self.rect.y + item.rect.y, item.rect.w, item.rect.h)
            if item_rect.collidepoint(point):
                self.select(index)
                item.mouse_down(relative_point)
                break

    def mouse_up(self, point):
        relative_point = get_relative_point(point, self.rect)
        for index, item in enumerate(self.items):
            item_rect = pygame.Rect(self.rect.x, self.rect.y + item.rect.y, item.rect.w, item.rect.h)
            if item_rect.collidepoint(point):
                self.deselect()
                item.mouse_up(relative_point)
                break

    def deselect(self):
        if self.selected_index is not None:
            self.items[self.selected_index].selected = False
        self.selected_index = None

    def select(self, index):
        self.deselect()
        self.selected_index = index

        if index is not None:
            item = self.items[self.selected_index]
            item.selected = True

    def _draw(self, screen):
        if not object_rectangle.ObjectRectangle._draw(self, screen):
            return False

        self.all_dirty_item()
        self.up_btn.draw_blit(self.surface)
        self.content_frame.draw_blit(self.surface)
        self.down_btn.draw_blit(self.surface)
        return True
