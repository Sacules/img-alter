from imgalter import mirror_image, drag, retouch
from PIL import Image
import random
import sys


class Executor:
    def __init__(self, funcs, image, frames):
        self.frames = frames
        self.funcs = funcs
        self.image = image

    def execute(self):
        current_frame = self.image
        image_steps = []
        for func in self.funcs:
            for frame in range(self.frames):
                progress = frame/self.frames
                new_frame = func(current_frame, progress, self.frames)
                image_steps.append(new_frame)
                current_frame = new_frame
        return image_steps

    def execute_random(self):
        current_frame = self.image
        image_steps = []
        for i in range(len(self.funcs)):
            for frame in range(self.frames):
                rnd_index = random.randrange(0, len(self.funcs))
                func = self.funcs[rnd_index]
                progress = frame/self.frames
                new_frame = func(current_frame, progress, self.frames)
                image_steps.append(new_frame)
                current_frame = new_frame
        return image_steps


def rots(image, progress, frames):
    return image.rotate(progress*(90//frames))


def mirror_diagonal_2(image, progress, frames):
    return mirror_image(image, progress, "diagonal_2")


def mirror_diagonal_1(image, progress, frames):
    return mirror_image(image, progress, "diagonal_1")


def mirror_horiz(image, progress, frames):
    return mirror_image(image, progress, "horizontal")


def mirror_vert(image, progress, frames):
    return mirror_image(image, progress, "vertical")


def my_retouch(image, progress, frames):
    return retouch(image, progress)


def drag_vert(image, progress, frames):
    return drag(image, progress, "vertical")


def drag_horiz(image, progress, frames):
    return drag(image, progress, "horizontal")


funcs = [mirror_diagonal_1, drag_vert]
im = Image.open(sys.argv[1])

images_array = Executor(funcs, im, 10).execute_random()
tmp = images_array.copy()
images_array.reverse()
tmp += images_array
tmp[0].save(sys.argv[2], save_all=True, append_images=tmp[1:], duration=95, loop=0)