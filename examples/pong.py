"""Pong example using TOW.PY"""

from textobject import TextObject
from component import ColliderComponent, MovementComponent, ControlComponent
from tow import TextOnlyWindow
import pygame


class Ball(TextObject):

    SPRITE = ["@@", "@@"]

    def __init__(self, start_pos):
        TextObject.__init__(self, Ball.SPRITE, start_pos)
        self.start_pos = start_pos
        self.position_gridded = True

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
        # Need to create a new list for position otherwise we will change startpos
        self.position = list(self.start_pos)
        self.movementcomponent.move(-self.movementcomponent.speed_x, 0)


class Paddle(TextObject):

    SPRITE = ["==", "||", "||", "||", "||", "=="]

    def __init__(self, start_pos, player_controlled=False, ball=None):
        TextObject.__init__(self, Paddle.SPRITE, start_pos)
        self.start_pos = start_pos
        self.player_controlled = player_controlled
        self.position_gridded = True
        self.speed = 0.3
        self.ball = ball

    def reset_paddle(self, other_object=None):
        self.position = list(self.start_pos)

    def move_up(self):
        self.movementcomponent.move(0, -self.speed)

    def move_down(self):
        self.movementcomponent.move(0, self.speed)

    def stop(self):
        self.movementcomponent.move(0, 0)

    def update(self, dt):
        if not self.player_controlled:
            ball_distance = (self.position[1] + (self.dimensions[1] // 2)) - (
                self.ball.position[1] + (self.ball.dimensions[1] // 2)
            )
            if ball_distance > self.dimensions[1] // 4:
                self.movementcomponent.move(0, -self.speed)
            elif ball_distance < -(self.dimensions[1] // 4):
                self.movementcomponent.move(0, self.speed)
            else:
                self.movementcomponent.stop()


tow = TextOnlyWindow()

ball = Ball([tow.WIDTH // 2, tow.HEIGHT // 2])

paddle1 = Paddle([20, 175], player_controlled=True)
paddle1.add_component(MovementComponent())

control_component = ControlComponent()
control_component.on_key_hold(pygame.K_w, paddle1.move_up)
control_component.on_key_hold(pygame.K_s, paddle1.move_down)
control_component.on_key_hold([pygame.K_w, pygame.K_s], paddle1.stop, reverse=True)
paddle1.add_component(control_component)

tow.add_object(paddle1)

paddle2 = Paddle([540, 175], ball=ball, player_controlled=True)
paddle2.add_component(MovementComponent())

control_component = ControlComponent()
control_component.on_key_hold(pygame.K_UP, paddle2.move_up)
control_component.on_key_hold(pygame.K_DOWN, paddle2.move_down)
control_component.on_key_hold([pygame.K_UP, pygame.K_DOWN], paddle2.stop, reverse=True)
paddle2.add_component(control_component)

tow.add_object(paddle2)

ball_collider = ColliderComponent()
ball_collider.add_collider(paddle1, ball.reverse_ball)
ball_collider.add_collider(paddle2, ball.reverse_ball)
ball_collider.add_collider((0, 0, tow.WIDTH, 1), ball.bounce)
ball_collider.add_collider((0, tow.HEIGHT - 1, tow.WIDTH, 1), ball.bounce)
ball_collider.add_collider(
    (0, 0, 1, tow.HEIGHT), [ball.reset_ball, paddle1.reset_paddle, paddle2.reset_paddle]
)
ball_collider.add_collider(
    (tow.WIDTH - 1, 0, 1, tow.HEIGHT),
    [ball.reset_ball, paddle1.reset_paddle, paddle2.reset_paddle],
)
ball.add_component(ball_collider)

movement_component = MovementComponent()
ball.add_component(movement_component)
movement_component.speed_x = 0.3

tow.add_object(ball)

tow.run()
