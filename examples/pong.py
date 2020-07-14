"""Pong example using TOW.PY"""

from textobject import TextObject
from component import ColliderComponent, MovementComponent
from tow import TextOnlyWindow
import pygame


class Ball(TextObject):

    SPRITE = ["  "]

    def __init__(self, start_pos):
        TextObject.__init__(self, Ball.SPRITE, start_pos, background=(255, 255, 255))
        self.start_pos = start_pos
        self.position_gridded = False

    def reverse_ball(self, paddle=None):
        self.movementcomponent.reverse_x()
        # x2 - x1, y2 - y1
        ball_center_y = self.position[1] + (self.dimensions[1] // 2)
        paddle_center_y = paddle.position[1] + (paddle.dimensions[1] // 2)

        self.movementcomponent.speed_y += (
            (ball_center_y - paddle_center_y) / paddle.dimensions[1] / 4
        )

    def bounce(self, wall=None):
        self.movementcomponent.reverse_y()

    def reset_ball(self, void=None):
        self.position = self.start_pos

        self.movementcomponent.move(-self.movementcomponent.speed_x, 0)


class Paddle(TextObject):

    SPRITE = ["  ", "  ", "  ", "  ", "  ", "  "]

    def __init__(self, start_pos, player_controlled=False, ball=None):
        TextObject.__init__(self, Paddle.SPRITE, start_pos, background=(255, 255, 255))
        self.start_pos = start_pos
        self.player_controlled = player_controlled
        self.position_gridded = False
        self.speed = 0.3
        self.ball = ball

    def reset_paddle(self, other_object=None):
        self.position = self.start_pos

    def update(self, dt):
        if self.player_controlled:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                self.movementcomponent.move(0, -self.speed)
            elif pressed[pygame.K_s]:
                self.movementcomponent.move(0, self.speed)
            else:
                self.movementcomponent.stop()
        else:
            self.position[1] = self.ball.position[1] - (self.dimensions[1] // 2)


tow = TextOnlyWindow()

b = Ball([tow.WIDTH // 2, tow.HEIGHT // 2])

p1 = Paddle([20, 175], player_controlled=True)
p1.add_component(MovementComponent())
tow.add_object(p1)

p2 = Paddle([540, 175], ball=b)
tow.add_object(p2)

ball_collider = ColliderComponent()
ball_collider.add_collider(p1, b.reverse_ball)
ball_collider.add_collider(p2, b.reverse_ball)
ball_collider.add_collider((0, 0, tow.WIDTH, 1), b.bounce)
ball_collider.add_collider((0, tow.HEIGHT - 1, tow.WIDTH, 1), b.bounce)
ball_collider.add_collider(
    (0, 0, 1, tow.HEIGHT), [b.reset_ball, p1.reset_paddle, p2.reset_paddle]
)
ball_collider.add_collider(
    (tow.WIDTH - 1, 0, 1, tow.HEIGHT), [b.reset_ball, p1.reset_paddle, p2.reset_paddle],
)
b.add_component(ball_collider)

movement_component = MovementComponent()
b.add_component(movement_component)
movement_component.speed_x = 0.2

tow.add_object(b)

tow.run()
