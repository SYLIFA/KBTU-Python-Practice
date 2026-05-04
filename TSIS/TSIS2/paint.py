import pygame
import datetime

# --- КОНСТАНТЫ ---
WIDTH, HEIGHT = 1000, 700
SIDEBAR_WIDTH = 160
CANVAS_WIDTH = WIDTH - SIDEBAR_WIDTH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (80, 80, 80)
BLUE, RED, GREEN = (0, 0, 255), (255, 0, 0), (0, 255, 0)

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("KBTU Paint Pro")
        
        # Холст для рисования
        self.canvas = pygame.Surface((CANVAS_WIDTH, HEIGHT))
        self.canvas.fill(WHITE)
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 14)
        self.title_font = pygame.font.SysFont("Verdana", 16, bold=True)
        
        # Состояние программы
        self.drawing = False
        self.tool = 'pencil' 
        self.color = BLACK
        self.thickness = 2
        self.start_pos = (0, 0)
        
        # Список инструментов и палитра
        self.tools = ['pencil', 'line', 'rect', 'circle', 'fill', 'eraser', 'text']
        self.colors = [BLACK, RED, GREEN, BLUE, (255, 255, 0), (255, 165, 0), (128, 0, 128)]
        
        # Переменные для текста
        self.text_active = False
        self.text_str = ""
        self.text_pt = (0, 0)

    def save_canvas(self):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pygame.image.save(self.canvas, f"paint_save_{now}.png")
        print(f"✅ Сохранено в папку проекта")

    def flood_fill(self, x, y, new_col):
        if not (0 <= x < CANVAS_WIDTH and 0 <= y < HEIGHT): return
        target_col = self.canvas.get_at((x, y))
        if target_col == new_col: return
        
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if self.canvas.get_at((cx, cy)) == target_col:
                self.canvas.set_at((cx, cy), new_col)
                for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < CANVAS_WIDTH and 0 <= ny < HEIGHT:
                        stack.append((nx, ny))

    def draw_ui(self):
        # Отрисовка боковой панели
        pygame.draw.rect(self.screen, GRAY, (0, 0, SIDEBAR_WIDTH, HEIGHT))
        pygame.draw.line(self.screen, DARK_GRAY, (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, HEIGHT), 3)
        
        y_offset = 20
        self.screen.blit(self.title_font.render("TOOLS", True, BLACK), (20, y_offset))
        y_offset += 30
        
        # Кнопки инструментов
        for t in self.tools:
            rect = pygame.Rect(20, y_offset, 120, 30)
            is_active = (self.tool == t)
            pygame.draw.rect(self.screen, DARK_GRAY if is_active else WHITE, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            self.screen.blit(self.font.render(t.capitalize(), True, WHITE if is_active else BLACK), (30, y_offset + 5))
            y_offset += 35
            
        y_offset += 20
        self.screen.blit(self.title_font.render("SIZE", True, BLACK), (20, y_offset))
        y_offset += 30
        # Кнопки размеров
        for size in [2, 5, 10]:
            rect = pygame.Rect(20, y_offset, 35, 30)
            is_active = (self.thickness == size)
            pygame.draw.rect(self.screen, DARK_GRAY if is_active else WHITE, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            self.screen.blit(self.font.render(str(size), True, WHITE if is_active else BLACK), (30, y_offset + 5))
            y_offset += 35

        y_offset += 20
        self.screen.blit(self.title_font.render("COLORS", True, BLACK), (20, y_offset))
        y_offset += 30
        grid_x, grid_y = 20, y_offset
        for c in self.colors:
            rect = pygame.Rect(grid_x, grid_y, 30, 30)
            pygame.draw.rect(self.screen, c, rect)
            if self.color == c:
                pygame.draw.rect(self.screen, WHITE, rect, 2)
            else:
                pygame.draw.rect(self.screen, BLACK, rect, 1)
            grid_x += 40
            if grid_x > 120:
                grid_x = 20
                grid_y += 40

    def handle_ui_click(self, pos):
        # Логика выбора инструментов кликом
        y_offset = 50
        for t in self.tools:
            if pygame.Rect(20, y_offset, 120, 30).collidepoint(pos):
                self.tool = t
                return True
            y_offset += 35
            
        y_offset = 320 # Координаты кнопок размера
        for size in [2, 5, 10]:
            if pygame.Rect(20, y_offset, 35, 30).collidepoint(pos):
                self.thickness = size
                return True
            y_offset += 35

        y_offset = 455 # Координаты палитры
        grid_x, grid_y = 20, y_offset
        for c in self.colors:
            if pygame.Rect(grid_x, grid_y, 30, 30).collidepoint(pos):
                self.color = c
                return True
            grid_x += 40
            if grid_x > 120:
                grid_x = 20
                grid_y += 40
        return False

    def draw_shape(self, surface, start, end, tool, color, thickness):
        if tool == 'line':
            pygame.draw.line(surface, color, start, end, thickness)
        elif tool == 'rect':
            r = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), 
                            abs(start[0]-end[0]), abs(start[1]-end[1]))
            pygame.draw.rect(surface, color, r, thickness)
        elif tool == 'circle':
            radius = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
            pygame.draw.circle(surface, color, start, radius, thickness)

    def run(self):
        last_pos = None
        while True:
            self.screen.fill(WHITE)
            self.screen.blit(self.canvas, (SIDEBAR_WIDTH, 0))
            self.draw_ui()
            
            m_pos = pygame.mouse.get_pos()
            canvas_m_pos = (m_pos[0] - SIDEBAR_WIDTH, m_pos[1])

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.save_canvas()
                    
                    if self.text_active:
                        if event.key == pygame.K_RETURN:
                            txt_surf = self.font.render(self.text_str, True, self.color)
                            self.canvas.blit(txt_surf, self.text_pt)
                            self.text_active, self.text_str = False, ""
                        elif event.key == pygame.K_BACKSPACE: self.text_str = self.text_str[:-1]
                        else: self.text_str += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if m_pos[0] < SIDEBAR_WIDTH:
                        self.handle_ui_click(m_pos)
                    else:
                        if self.tool == 'fill':
                            self.flood_fill(canvas_m_pos[0], canvas_m_pos[1], self.color)
                        elif self.tool == 'text':
                            self.text_active, self.text_pt = True, canvas_m_pos
                        else:
                            self.drawing, self.start_pos = True, canvas_m_pos
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.drawing:
                        if self.tool not in ['pencil', 'eraser']:
                            self.draw_shape(self.canvas, self.start_pos, canvas_m_pos, self.tool, self.color, self.thickness)
                        self.drawing, last_pos = False, None

            # ЛОГИКА РИСОВАНИЯ
            if self.drawing:
                if self.tool == 'pencil' or self.tool == 'eraser':
                    c = self.color if self.tool == 'pencil' else WHITE
                    t = self.thickness if self.tool == 'pencil' else self.thickness * 4
                    if last_pos:
                        pygame.draw.line(self.canvas, c, last_pos, canvas_m_pos, t)
                    last_pos = canvas_m_pos
                else:
                    # Превью фигуры на основном экране
                    self.draw_shape(self.screen, (self.start_pos[0] + SIDEBAR_WIDTH, self.start_pos[1]), 
                                   m_pos, self.tool, self.color, self.thickness)

            if self.text_active:
                self.screen.blit(self.font.render(self.text_str + "|", True, self.color), 
                                (self.text_pt[0] + SIDEBAR_WIDTH, self.text_pt[1]))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    PaintApp().run()