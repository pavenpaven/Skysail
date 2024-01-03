import pygame
import os
import math

comp = lambda f,g:lambda *x:f(g(*x))

class Animation:
    def __init__(self, frames, size, frame_delay, loop = True): 
        self.frames = frames 
        self.frame_delay = frame_delay
        self.texture = self.frames[0]
        self.loop = loop

    @classmethod
    def from_dir(cls, directory: str, size: tuple[int, int], *args):
        return cls([pygame.transform.scale(
                            pygame.image.load(f"{directory}/{i}"), size)
                        for i in sorted(os.listdir(directory),
                                key = lambda x:int(x.replace(".png", "").split("-")[2]))],
                   size, *args)




    def update(self, framecount: int) -> None:
        if self.loop:
            self.texture = self.frames[math.floor(framecount/self.frame_delay) % len(self.frames)]
            return None
        if math.floor(framecount/self.frame_delay) >= len(self.frames) - 1:
            pass
        else:
            self.texture = self.frames[math.floor(framecount/self.frame_delay)]
