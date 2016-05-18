'''
Created on 2016/03/10

@author: hirano
'''
import pygame
import object_rectangle  # @UnresolvedImport
import callback  # @UnresolvedImport
import label  # @UnresolvedImport
from pygame.rect import Rect
import scroll

class StringListView(object_rectangle.ObjectRectangle):
    '''
    classdocs
    '''
    def __init__(self, rect, items, row_num=0, minimize=(0, 0)):
        '''
        Constructor
        '''
        object_rectangle.ObjectRectangle.__init__(self, rect)
        self.row_num = row_num
        if minimize == (0, 0):
            minimize = rect.size
        self.minimize = minimize
        self.items = []
        self._items_font = None
        self.string_items = items
        self.selected_index = None
        self.on_selected = callback.Signal()
        self.items_surface = pygame.Surface((self.rect.w - self.border_widths * 2, self.rect.h - self.border_widths * 2)).convert()

    @property
    def items_font(self):
        return self._items_font
        
    @items_font.setter
    def items_font(self, new_font):
        self._items_font = new_font
        self.string_items = self._string_items
    
    @property
    def string_items(self):
        return self._string_items
    
    @string_items.setter
    def string_items(self, new_items):
        del self.items[:]
            
        self._string_items = new_items

        x = 0
        y = 0
        w = self.rect.w
        h = 0
        if self.row_num != 0:
            h = (self.rect.h - self.border_widths) / self.row_num

        for item in self._string_items:
            string_list_item = StringListItem(Rect(x, y, w, h), item)
            if self._items_font is not None:
                string_list_item.font = self._items_font
            self.add_item(string_list_item)
            y += string_list_item.rect.h

        self.rect.h = y + self.border_widths * 2
        if self.rect.h < self.minimize[1]:
            self.rect.h = self.minimize[1]
        self.dirty = True

    def render(self):
        self._render(self._string_items)

    def _render(self, string_items):
        x = 0
        y = 0
        w = self.rect.w
        #         h = (window.rect.h - 10 - self.border_widths * 2) // 8 - 5
        #         h = (self.rect.h - self.border_widths) / (self.rect.h // (10 + window.col_rect_mini(0, 0, 1, 1).h) + 1)

        h = 0
        if self.row_num != 0:
            h = (self.rect.h - self.border_widths) / self.row_num

        for item in string_items:
            string_list_item = StringListItem(Rect(x, y, w, h), item)
            if self._items_font is not None:
                string_list_item.font = self._items_font
            y += string_list_item.rect.h

        self.rect.h = y + self.border_widths * 2
        if self.rect.h < self.minimize[1]:
            self.rect.h = self.minimize[1]
        self.items_surface = pygame.Surface(
            (self.rect.w - self.border_widths * 2, self.rect.h - self.border_widths * 2)).convert()

    def add_item(self, item):
        assert item is not None
        self.rm_item(item)
        self.items.append(item)
        
    def rm_item(self, child):
        for index, ch in enumerate(self.items):
            if ch == child:
                del self.items[index]
                break
            
    def all_dirty_item(self):
        for item in self.items:
            item.dirty = True
        
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
            self.on_selected(self, item, index)
            
    def mouse_down(self, point):
        for index, item in enumerate(self.items):
            item_rect = Rect(self.rect.x + self.border_widths, self.rect.y + self.border_widths + item.rect.y, item.rect.w, item.rect.h)
            if item_rect.collidepoint(point):
                self.select(index)
                break
            
    def _draw(self, screen):
        if not object_rectangle.ObjectRectangle._draw(self, screen):
            return False

        self.render()
        self.all_dirty_item()
        self.items_surface.fill(self.background_color)
        for item in self.items:
            item.draw_blit(self.items_surface)
            
        self.surface.blit(self.items_surface, (self.border_widths, self.border_widths))
        return True
    
class StringListItem(label.Label):
    
    def __init__(self, rect, text):
        label.Label.__init__(self, rect, text, halign=label.LEFT)
        if self.rect.h == 0:
            self.rect.h = self.font.size("X")[1] + self.padding[1] * 2

class ScrollStringListView(scroll.ScrollView):

    def __init__(self, rect, items):
        self.list_view = StringListView(Rect((0, 0), rect.size), items)
        scroll.ScrollView.__init__(self, rect, self.list_view)
        list_view_rect = Rect((0, 0), self.content_frame.rect.size)
        self.list_view.minimize = list_view_rect.size
        self.content_view = self.list_view
        self.on_selected = callback.Signal()
        self.list_view.on_selected = self.on_selected

    @property
    def string_items(self):
        return self.list_view.string_items

    @string_items.setter
    def string_items(self, new_items):
        self.list_view.string_items = new_items
        self.content_offset = (0, 0)

