import pygame
from ui_elements import *
from entity import *
import random


class SceneManager:
    """Manages the active scene. Use `change_scene(SomeSceneClass)` to switch.

    The manager ensures only one active scene instance exists at a time.
    """

    def __init__(self, initial_scene_cls, screen, *args, **kwargs):
        self.screen = screen
        self.current_scene = None
        self.change_scene(initial_scene_cls, *args, **kwargs)

    def change_scene(self, scene_cls, *args, **kwargs):
        """Replace the current scene with a new instance of `scene_cls`.

        `scene_cls` should be a subclass of `Scene`.
        """
        if self.current_scene:
            try:
                self.current_scene.stop()
            except Exception:
                pass
            self.current_scene = None

        # instantiate new scene, giving it a reference to this manager
        self.current_scene = scene_cls(self, *args, **kwargs)
        try:
            self.current_scene.start()
        except Exception:
            pass


class Scene:
    """Base scene class.

    Subclass this and override `start`, `stop`, `handle_event`, `update`, and
    `draw` as needed. The main game loop will call `run_frame` each tick.
    """

    def __init__(self, manager):
        self.manager = manager
        self._running = True

    def start(self):
        """Called when the scene becomes active."""
        pass

    def stop(self):
        """Called when the scene is replaced or the game exits."""
        self._running = False

    def handle_event(self, event):
        """Handle a single pygame event forwarded from the main loop."""
        pass

    def update(self, dt):
        """Update scene state. `dt` is seconds since last frame."""
        pass

    def draw(self, surface):
        """Draw scene to the given surface."""
        pass

    def run_frame(self, surface, dt):
        """A single integrated frame: update then draw."""
        self.update(dt)
        self.draw(surface)


class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 48)

                # create three buttons using ui_elements.Button
        w, h = self.manager.screen.get_size()
        btn_w, btn_h = 320, 60
        cx = (w - btn_w) // 2
        start_y = (h // 2) - btn_h
        self.btns = []
        
        self.play_btn = Button(cx, start_y, btn_w, btn_h, text="Play", font_size=36, bg_color=(0, 0, 0), on_click=self.start_game)
        self.instruct = Button(cx, start_y + btn_h + 12, btn_w, btn_h, text= "How to Play", font_size=36, bg_color=(0,0,0), on_click=self.learn)
        self.credits_btn = Button(cx, start_y + (btn_h + 12) * 2, btn_w, btn_h, text="Credits", font_size=36, bg_color=(0, 0, 0), on_click=self.show_credits)
        self.quit_btn = Button(cx, start_y + (btn_h + 12) * 3, btn_w, btn_h, text="Quit", font_size=36, bg_color=(0, 0, 0), on_click=self.quit_game)
        self.btns.append(self.play_btn)
        self.btns.append(self.credits_btn)
        self.btns.append(self.quit_btn)
        
    def start_game(self):
        from scenes import TestGameScene
        self.manager.change_scene(TestGameScene)
    
    def show_credits(self):
        from scenes import CreditsScene
        self.manager.change_scene(CreditsScene)
    
    def learn(self):
        from scenes import LearnScene
        self.manager.change_scene(LearnScene)
    
    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def start(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            print("Key down")
            if event.key == pygame.K_RETURN:
                # switch to TestGameScene
                from scenes import TestGameScene

                self.manager.change_scene(TestGameScene)

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(" Thing (mouse) down", event.pos)
                    
            if self.play_btn.on_click(event):
                print('test')
                from scenes import BetterScene

                self.manager.change_scene(BetterScene)
                return
            if self.instruct.on_click(event):
                from scenes import LearnScene
                
                self.manager.change_scene(LearnScene)
                return
            if self.credits_btn.on_click(event):
                print('test2')
                from scenes import CreditsScene

                self.manager.change_scene(CreditsScene)
                return
            if self.quit_btn.on_click(event):
                # post a quit event so main loop handles shutdown
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((30, 30, 60))
        # draw title
        title = self.font.render("My Game", True, (230, 230, 230))
        rect = title.get_rect(center=(surface.get_width() // 2, surface.get_height() // 4))
        surface.blit(title, rect)

        # draw buttons
        self.play_btn.draw(surface)
        self.instruct.draw(surface)
        self.credits_btn.draw(surface)
        self.quit_btn.draw(surface)




class TestGameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)
        self.time_thingy = 30.0  # Start with 30 seconds
        self.entities = []
        self.progress_bar = ProgressBar(10, 10, 200, 20, max_value=30)

    def start(self):
        self.time_thingy = 30.0
        self.entities = self.generate_entities()

    def generate_entities(self):
        entities = []
        # Example: Add Baldo and jars
        entities.append(Baldo(100, 100, "Assets/baldo_01.png"))
        entities.append(Jar(200, 200, "Assets/base_02.png", "strawberry"))
        entities.append(Jar(300, 300, "Assets/base_03.png", "marmalade"))
        return entities

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = False  # Track if any entity was clicked
            for entity in self.entities:
                result = entity.on_click(event)
                if result == ENTITY.BALDO:
                    self.label = "WELL DONE, U FOUND BALDO"
                    self.time_thingy = 0  # End the game
                    self.win = True
                    clicked = True
                elif result == ENTITY.JAM:
                    self.label = "+10 seconds"
                    self.time_thingy += 10
                    clicked = True
                elif result == ENTITY.MARMELADE:
                    self.label = "+15 seconds"
                    self.time_thingy += 15
                    clicked = True
                elif result == ENTITY.WALDO:
                    self.label = "get wrekt lol"
                    self.time_thingy -= 5
                    clicked = True
            
            if not clicked:  # No entity was clicked
                self.label = "The aim is to find Baldo, Not Waldo"
                print(" lol u bad at the game")
    def update(self, dt):
        if self.time_thingy <= 0:
            if not self.win:
                print("Game Over!")
            from scenes import MenuScene
            self.manager.change_scene(MenuScene)
            return  # Prevent further updates
    
        self.time_thingy -= dt
        self.progress_bar.set_value(self.time_thingy)
        self.progress_label.set_text(f"Time: {int(self.time_thingy)}")  # Update progress label dynamically
        #self.comment_label.set_text(self.label)  # Update comment label dynamically
        
        
    def draw(self, surface):
        surface.fill((10, 80, 40))
        for entity in self.entities:
            entity.draw(surface)
        self.progress_bar.draw(surface)

class BetterScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        pygame.font.init()

        self.font = pygame.font.SysFont(None, 28)
        self.entities = []

        self.progress_bar = ProgressBar(10, 10, 200, 20, max_value=30)
        self.progress_label = Label(
            self.progress_bar.rect.x + self.progress_bar.rect.width + 5,
            self.progress_bar.rect.y,
            color=(255, 255, 255),
            text="30",
            font_size=24,
            bg_color=(0, 0, 0)
        )

        #self.comment_label = Label(10, 520, (0, 0, 0), "U knobhead", 22)

        self.label = "Sup"
        self.time_thingy = 30.0
        self.win = False

    def start(self):
        self.time_thingy = 30.0
        self.entities.clear()
        self.generate_many_macguyvers_and_baldo()

    def get_random_pos(self):
        x = random.randint(0, 950)
        y = random.randint(3, 539)
        return x, y

    def generate_many_macguyvers_and_baldo(self):
        # Waldo decoys
        for _ in range(random.randint(120, 1800)):
            x, y = self.get_random_pos()
            self.entities.append(Waldo(x, y))

        # Jam jars
        for _ in range(3,8):
            x, y = self.get_random_pos()
            self.entities.append(Jar(x, y, ENTITY.JAM))

        # Marmalade jar
        x, y = self.get_random_pos()
        self.entities.append(Jar(x, y, ENTITY.MARMELADE))

        # Baldo (win condition)
        x, y = self.get_random_pos()
        self.entities.append(Baldo(x, y))

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        for entity in self.entities[:]:  # iterate over a COPY
            result = entity.on_click(event)

            if result is None:
                continue

            if result == ENTITY.BALDO:
                self.label = "WELL DONE, U FOUND BALDO"
                self.time_thingy = 0
                self.win = True
                return

            elif result == ENTITY.JAM:
                self.label = "+10 seconds"
                self.time_thingy += 10
                self.entities.remove(entity)  # optional: remove jar too
                return

            elif result == ENTITY.MARMELADE:
                self.label = "+15 seconds"
                self.time_thingy += 15
                self.entities.remove(entity)  # optional: remove jar too
                return

            elif result == ENTITY.WALDO:
                self.label = "One less Waldo"
                self.time_thingy -= 5
                self.entities.remove(entity)
                return

        self.label = "The aim is to find Baldo, Not Waldo"


    def update(self, dt):
        if self.time_thingy <= 69 and self.time_thingy >= 67:
            self.gato = pygame.mixer.Sound("Assets/gato.mp3")
            self.gato.play()
        if self.time_thingy <= 0:
            if not self.win:
                print("Game Over!")
                self.fail = pyg.mixer.Sound("Assets/bruh.mp3")
                self.fail.play()
                
                from scenes import FailScene
                self.manager.change_scene(FailScene)
                return
            self.win_sound = pygame.mixer.Sound("Assets/win.mp3")    
            self.win_sound.play()
                
                
            from scenes import WinScene
            self.manager.change_scene(WinScene)
            return

        self.time_thingy -= dt
        self.progress_bar.set_value(self.time_thingy)
        self.progress_label.set_text(str(int(self.time_thingy)))
        #self.comment_label.set_text(self.label)
        print(" updated labels")

    def draw(self, surface):
        surface.fill((128, 64, 0))

        for entity in self.entities:
            entity.draw(surface)

        #self.comment_label.draw(surface)
        self.progress_bar.draw(surface)
        self.progress_label.draw(surface)

        
        
        
        



class CreditsScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 28)

    def start(self):
        pass

    def handle_event(self, event):
        # return to menu on any key or click
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            from scenes import MenuScene

            self.manager.change_scene(MenuScene)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((20, 20, 20))
        lines = [
            "Credits",
            "Game Jam Team:",
            "- Dev: Spectral_o6 (Felix Gallé)",
            "- Art: Also Spectral_o6 (inspo by ChatGPT, thx mate)",
            " (press any key or click to return ",
            "to the war crime that is this game)"
        ]
        y = 60
        for ln in lines:
            txt = self.font.render(ln, True, (200, 200, 200))
            rect = txt.get_rect(center=(surface.get_width() // 2, y))
            surface.blit(txt, rect)
            y += 40
        
        
class StartScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
    
    def start(self):
        pass
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            match event.type:
                
                case pygame.BUTTON_LEFT:
                    from scenes import TestGameScene
                    self.manager.change_scene(TestGameScene)
            
    
class LearnScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.slide = 0
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 28)
        self.w, self.h = self.manager.screen.get_size()
        self.create_example_guys()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            from scenes import MenuScene
            
    def create_example_guys(self):
        self.baldo_texture_path = "Assets/baldo_01.png"
        self.baldo_texture = pyg.image.load(self.baldo_texture_path).convert_alpha()
        self.baldo = Baldo(30, (self.h//2)-(self.baldo_texture.get_height()//2), self.baldo_texture_path)
        
        
        self.waldo_texture_path = "Assets/base_5.png"
        self.waldo_texture = pyg.image.load(self.waldo_texture_path).convert_alpha()
        self.waldo = Waldo(self.w-30, (self.h//2)-(self.waldo_texture.get_height()//2))
            
    def draw(self, surface):
        surface.fill((20, 20, 20))
        lines = [
            "How to Play",
            "",
            "~~~~~~~~~~~",
            "",
            "",
            "<<< That is Baldo,",
            " you have to find him.",
            "",
            "That is Waldo >>>",
            "He's there to prevent you from finding Baldo",
            "(Click anywhere to continue)"
        ]
        y = 100
        for ln in lines:
            txt = self.font.render(ln, True, (200, 200, 200))
            rect = txt.get_rect(center=(surface.get_width() // 2, y))
            surface.blit(txt, rect)
            y += 40
        
        self.big_baldo = pyg.transform.scale_by(self.baldo_texture, 12)
        surface.blit(self.big_baldo, (30,(self.h/2)-(self.baldo_texture.get_height())))
        self.big_waldo = pyg.transform.scale_by(self.waldo_texture, 12)
        surface.blit(self.big_waldo, (self.w-180,(self.h/2)-(self.waldo_texture.get_height())))
        #pyg.draw.rect(surface, (255,0,0), pyg.Rect(self.big_baldo.rect.x,self.big_baldo.rect.y,self.big_baldo_texture.get_width(),self.baldo_texture.get_height()),2)
        
class WinScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        pygame.font.init()

        self.w, self.h = self.manager.screen.get_size()

        self.title_font = pygame.font.SysFont(None, 96)
        self.btn_font_size = 36

        btn_w, btn_h = 300, 60
        cx = (self.w - btn_w) // 2
        start_y = self.h // 2 + 20

        self.play_again_btn = Button(
            cx, start_y,
            btn_w, btn_h,
            text="Play Again",
            font_size=self.btn_font_size,
            bg_color=(0, 0, 0),
            on_click=self.play_again
        )

        self.menu_btn = Button(
            cx, start_y + btn_h + 15,
            btn_w, btn_h,
            text="Main Menu",
            font_size=self.btn_font_size,
            bg_color=(0, 0, 0),
            on_click=self.go_menu
        )

    def play_again(self):
        from scenes import BetterScene
        self.manager.change_scene(BetterScene)

    def go_menu(self):
        from scenes import MenuScene
        self.manager.change_scene(MenuScene)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_btn.on_click(event):
                self.play_again()
            elif self.menu_btn.on_click(event):
                self.go_menu()

    def draw(self, surface):
        surface.fill((20, 120, 40))  # celebratory green-ish

        title = self.title_font.render("YOU WON", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.w // 2, self.h // 2 - 120))
        surface.blit(title, title_rect)
        

        self.play_again_btn.draw(surface)
        self.menu_btn.draw(surface)

class FailScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        pygame.font.init()

        self.w, self.h = self.manager.screen.get_size()

        self.title_font = pygame.font.SysFont(None, 96)
        self.msg_font = pygame.font.SysFont(None, 32)
        self.btn_font_size = 36

        # Some savage mocking lines
        self.mock_lines = [
            "Oof… that was embarrassing.",
            "Pro tip: Use your eyes",
            "Even my grandma could do better.",
            "Someone get this player a tutorial.",
            "Skill level: potato.",
            "You just redefined failure.",
            "This is… sad",
            "The controls are fine, you're the problem.",
            "You’re doing a fantastic job… at losing.",
            "Nice, 10/10, would cringe again.",
            "Even AI would beat you at this (tried & tested btw).",
            "Even a blindfolded chicken could find Baldo better.",
            "The aim is simple… too bad.",
            "You’re an inspiration… to a bunch of trolls... or the kardashians.",
            "Maybe it’s time to reconsider your life choices.",
            "Skill? What’s that?",
        ]
        self.mock_msg = random.choice(self.mock_lines)

        # Buttons
        btn_w, btn_h = 300, 60
        cx = (self.w - btn_w) // 2
        start_y = self.h // 2 + 40

        self.try_again_btn = Button(
            cx, start_y,
            btn_w, btn_h,
            text="Try Again",
            font_size=self.btn_font_size,
            bg_color=(0, 0, 0),
            on_click=self.try_again
        )

        self.menu_btn = Button(
            cx, start_y + btn_h + 15,
            btn_w, btn_h,
            text="Main Menu",
            font_size=self.btn_font_size,
            bg_color=(0, 0, 0),
            on_click=self.go_menu
        )

    def try_again(self):
        from scenes import BetterScene
        self.manager.change_scene(BetterScene)

    def go_menu(self):
        from scenes import MenuScene
        self.manager.change_scene(MenuScene)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.try_again_btn.on_click(event): # Check collision.
                from scenes import BetterScene
                self.manager.change_scene(BetterScene)
            elif self.menu_btn.on_click(event):
                from scenes import MenuScene
                self.manager.change_scene(MenuScene)

    def draw(self, surface):
        # Solid red-ish background for failure vibes
        surface.fill((150, 20, 20))

        # YOU FAILED title
        title = self.title_font.render("YOU FAILED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.w // 2, self.h // 2 - 120))
        surface.blit(title, title_rect)

        # Mocking message
        msg = self.msg_font.render(self.mock_msg, True, (255, 220, 220))
        msg_rect = msg.get_rect(center=(self.w // 2, self.h // 2 - 50))
        surface.blit(msg, msg_rect)

        # Buttons
        self.try_again_btn.draw(surface)
        self.menu_btn.draw(surface)