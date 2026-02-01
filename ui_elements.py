import pygame as pyg


class UIElement:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.rect = pyg.Rect(x, y, width, height)
        self.color = color

    def on_click(self, event):
        return self.rect.collidepoint(event.pos)


class Label(UIElement):
    def __init__(
        self,
        x,
        y,
        color=(0, 0, 0),
        text="",
        font_size=18,
        bg_color=(255, 255, 255),
        width=None,
        height=None,
    ):
        self.color = color
        self.bg_color = bg_color
        self.font = pyg.font.Font(None, font_size)
        self.text = text
        self.text_surf = self.font.render(self.text, True, self.color)

        if width is None:
            width = self.text_surf.get_width()
        if height is None:
            height = self.text_surf.get_height()

        self.rect = pyg.Rect(x, y, width, height)

    def set_text(self, text):
        if text == self.text:
            return

        self.text = text
        self.text_surf = self.font.render(self.text, True, self.color)

    def draw(self, surface):
        pyg.draw.rect(surface, self.bg_color, self.rect)

        # center text every frame
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, text_rect)


class Button(UIElement):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font_size=18,
        color=(255, 255, 255),
        bg_color=(0, 0, 0),
        on_click=None,
    ):
        super().__init__(x, y, width, height, color)
        self.text = text
        self.font = pyg.font.Font(None, font_size)
        self.color = color
        self.bg_color = bg_color
        self.on_click_callback = on_click

        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        pyg.draw.rect(surface, self.bg_color, self.rect)
        pyg.draw.rect(surface, self.color, self.rect, 2)
        surface.blit(self.text_surf, self.text_rect)


class ProgressBar(UIElement):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        max_value,
        color=(0, 255, 0),
        bg_color=(100, 100, 100),
    ):
        super().__init__(x, y, width, height, color)
        self.max_value = max_value
        self.current_value = max_value
        self.bg_color = bg_color

    def set_value(self, value):
        self.current_value = max(0, min(self.max_value, value))

    def draw(self, surface):
        pyg.draw.rect(surface, self.bg_color, self.rect)

        if self.max_value > 0:
            fill_width = int(
                (self.current_value / self.max_value) * self.rect.width
            )
        else:
            fill_width = 0

        fill_rect = pyg.Rect(
            self.rect.x, self.rect.y, fill_width, self.rect.height
        )
        pyg.draw.rect(surface, self.color, fill_rect)

        pyg.draw.rect(surface, (10, 10, 10), self.rect, 2)
