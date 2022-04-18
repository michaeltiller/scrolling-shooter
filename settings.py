class Settings():
    def __init__(self):

        self.screen_width = 800 
        self.screen_height = int(self.screen_width * 0.8)
        self.bg_color = (144,201, 120)
        self.red =(255, 0, 0)
        self.ROWS = 16
        self.COLS = 150
        self.TILE_SIZE = self.screen_height // self.ROWS
        self.TILE_TYPES = 21
        self.level = 1
        self.scroll_thresh = 20
        self.screen_scroll = 0 
        self.bg_scroll = 0
        self.max_level = 2

