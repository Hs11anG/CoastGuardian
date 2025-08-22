import pygame

class Scene:
    """
    所有場景的抽象基礎類別 (Abstract Base Class)
    """
    def __init__(self, manager):
        self.manager = manager

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

class SceneManager:
    """
    管理所有場景的狀態機
    """
    def __init__(self, scenes: dict, initial_scene: str):
        self.scenes = {name: scene_class(self) for name, scene_class in scenes.items()}
        self.current_scene = self.scenes[initial_scene]
        print(f"Starting with scene: {initial_scene}")

    def switch_to_scene(self, scene_name: str):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            print(f"Switched to scene: {scene_name}")

    def handle_events(self, events):
        self.current_scene.handle_events(events)

    def update(self):
        self.current_scene.update()

    def draw(self, screen):
        self.current_scene.draw(screen)
        
