from typing import Tuple, Callable, NoReturn, Generic
from textobject import TextObject
import pygame

Position = Tuple[int, int]


class Component:
    def __init__(self):
        self.root = None

    def update(self, dt: int) -> NoReturn:
        raise NotImplementedError("This should be an overrided method.")


class MovementComponent(Component):
    def __init__(self):
        self.speed_x, self.speed_y = 0, 0

    def update(self, dt: int) -> NoReturn:
        self.root.position[0] += self.speed_x * dt
        self.root.position[1] += self.speed_y * dt

    def move(self, speed_x: float, speed_y: float) -> NoReturn:
        self.speed_x = speed_x
        self.speed_y = speed_y

    def stop(self) -> NoReturn:
        self.speed_x, self.speed_y = 0, 0

    def reverse_x(self) -> NoReturn:
        self.speed_x *= -1

    def reverse_y(self) -> NoReturn:
        self.speed_y *= -1


class PhysicsComponent(Component):
    def __init__(self, mass: float, max_vel: Generic, dampening: float = 0):
        Component.__init__(self)
        self.mass = mass
        self.dampening = dampening
        self.acc_x, self.acc_y = 0, 0
        self.vel_x, self.vel_y = 0, 0

        if type(max_vel) is tuple and len(max_vel) == 2:
            self.vel_x_max, self.vel_y_max = max_vel
        else:
            self.vel_x_max, self.vel_y_max = max_vel, max_vel

    def update(self, dt: int) -> NoReturn:
        self.vel_x = self.acc_x * self.mass * self.dampening
        self.vel_y = self.acc_y * self.mass * self.dampening

        if self.vel_x > self.vel_x_max:
            self.vel_x = self.vel_x_max
        if self.vel_x < -self.vel_x_max:
            self.vel_x = -self.vel_x_max

        if self.vel_y > self.vel_y_max:
            self.vel_y = self.vel_y_max
        if self.vel_y < -self.vel_y_max:
            self.vel_y = -self.vel_y_max

        self.root.position[0] += self.vel_x * dt
        self.root.position[1] += self.vel_y * dt

    def give_acceleration(self, acc_x: float, acc_y: float) -> NoReturn:
        self.acc_x += acc_x
        self.acc_y += acc_y

    def set_acceleration(self, acc_x: float, acc_y: float) -> NoReturn:
        self.acc_x = acc_x
        self.acc_y


class ColliderComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self.collideables = []

    def update(self, dt: int) -> NoReturn:
        for obj, func in self.collideables:
            run_func = False
            if type(obj) == tuple and len(obj) == 2 and self.point_collision(obj):
                run_func = True
            elif issubclass(type(obj), TextObject) and self.other_collision(obj):
                run_func = True
            elif type(obj) is tuple and len(obj) == 4 and self.rect_collision(obj):
                run_func = True

            if run_func:
                if type(func) is list:
                    for f in func:
                        f(obj)
                else:
                    func(obj)

    def add_collider(self, other: TextObject, func: Callable) -> NoReturn:
        self.collideables.append((other, func))

    def point_collision(self, point_pos: Position) -> bool:
        if (
            self.root.position[0] <= point_pos[0]
            and self.root.position[1] <= point_pos[1]
            and self.root.position[0] + self.root.dimensions[0] >= point_pos[0]
            and self.root.position[1] + self.root.dimensions[1] >= point_pos[1]
        ):
            return True
        return False

    def other_collision(self, other: "TextObject") -> bool:
        if (
            self.root.position[0] <= other.position[0] + other.dimensions[0]
            and self.root.position[0] + self.root.dimensions[0] >= other.position[0]
            and self.root.position[1] <= other.position[1] + other.dimensions[1]
            and self.root.position[1] + self.root.dimensions[1] >= other.position[1]
        ):
            return True
        return False

    def rect_collision(self, rect: Tuple[int, int, int, int]) -> bool:
        if (
            self.root.position[0] <= rect[0] + rect[2]
            and self.root.position[0] + self.root.dimensions[0] >= rect[0]
            and self.root.position[1] <= rect[1] + rect[3]
            and self.root.position[1] + self.root.dimensions[1] >= rect[1]
        ):
            return True
        return False


class ControlComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self.controls = []

    def update(self, dt):
        for under_func, key, call, reverse in self.controls:
            if under_func(key, reverse):
                call()

    def is_key_down(self, key):
        pass

    def is_key_hold(self, key, reverse=False):
        if type(key) is list:
            for k in key:
                if pygame.key.get_pressed()[k] and reverse:
                    return False
            return True
        elif type(key) is int:
            return pygame.key.get_pressed()[key] and not reverse

    def on_key_down(self, key, call, reverse=False):
        self.controls.append((self.is_key_down, key, call, reverse))

    def on_key_hold(self, key, call, reverse=False):
        self.controls.append((self.is_key_hold, key, call, reverse))
