"""Pong example using TOW.PY"""

from towpy import TextObject
from towpy.component import ColliderComponent, MovementComponent, ControlComponent
from towpy import TextOnlyWindow
import pygame


class Ball(TextObject):

    SPRITE = ["@@", "@@"]

    def __init__(self, start_pos):
        TextObject.__init__(self, Ball.SPRITE, start_pos)
        self.start_pos = start_pos

    def set_position(self, pos):
        self.start_pos = pos
        self.position = list(self.start_pos)

    def reverse_ball(self, paddle=None):
        self.movementcomponent.reverse_x()
        # x2 - x1, y2 - y1
        ball_center_y = self.position[1] + (self.size[1] // 2)
        paddle_center_y = paddle.position[1] + (paddle.size[1] // 2)

        self.movementcomponent.current_speed_y += (
            (ball_center_y - paddle_center_y) / paddle.size[1] / 4
        )

    def reset_ball(self, void=None):
        self.position = list(self.start_pos)
        self.movementcomponent.stop_y()


class Paddle(TextObject):

    SPRITE = ["==", "||", "||", "||", "||", "=="]

    def __init__(self, start_pos, player_controlled=False, ball=None):
        TextObject.__init__(self, Paddle.SPRITE, start_pos)
        self.set_position(start_pos)
        self.player_controlled = player_controlled
        self.ball = ball

    def set_position(self, pos):
        self.start_pos = pos
        self.position = list(self.start_pos)

    def reset_paddle(self, other_object=None):
        self.position = list(self.start_pos)

    def update(self, dt):
        if not self.player_controlled:
            self.movementcomponent.follow(self.ball, 15)


class Score(TextObject):
    SPRITE = ["0"]

    def __init__(self, start_pos):
        TextObject.__init__(self, Score.SPRITE, start_pos)
        self.score = 0

    def add_score(self):
        self.score += 1
        self.set_sprite(str(self.score))


tow = TextOnlyWindow(size=(80, 32))

divider = TextObject(["|"] * 80, [0, 0])
ball = Ball([0, 0])
paddle1 = Paddle([0, 0], player_controlled=True)
paddle2 = Paddle([0, 0], ball=ball, player_controlled=True)
score1 = Score([tow.WIDTH // 4, 0])
score2 = Score([tow.WIDTH - (tow.WIDTH // 4), 0])

divider.position = [(tow.WIDTH // 2) - (divider.size[0] // 2), 0]
ball.set_position(
    [(tow.WIDTH // 2) - (ball.size[0] // 2), (tow.HEIGHT // 2) - (ball.size[1] // 2),]
)
paddle1.set_position([20, (tow.HEIGHT // 2) - (paddle1.size[1] // 2)])
paddle2.set_position(
    [tow.WIDTH - 20 - paddle2.size[0], (tow.HEIGHT // 2) - (paddle2.size[1] // 2),]
)

paddle1.add_component(MovementComponent((0, 0.3)))
paddle2.add_component(MovementComponent((0, 0.3)))
ball.add_component(MovementComponent(0.3))
ball.movementcomponent.move_left()

control_component = ControlComponent()
control_component.on_key_hold(pygame.K_w, paddle1.movementcomponent.move_up)
control_component.on_key_hold(pygame.K_s, paddle1.movementcomponent.move_down)
control_component.on_key_hold(
    [pygame.K_w, pygame.K_s], paddle1.movementcomponent.stop, reverse=True
)
paddle1.add_component(control_component)

control_component = ControlComponent()
control_component.on_key_hold(pygame.K_UP, paddle2.movementcomponent.move_up)
control_component.on_key_hold(pygame.K_DOWN, paddle2.movementcomponent.move_down)
control_component.on_key_hold(
    [pygame.K_UP, pygame.K_DOWN], paddle2.movementcomponent.stop, reverse=True
)
paddle2.add_component(control_component)

ball_collider = ColliderComponent()
ball_collider.add_collider(paddle1, ball.reverse_ball, pass_back=True)
ball_collider.add_collider(paddle2, ball.reverse_ball, pass_back=True)
ball_collider.add_collider((0, 0, tow.WIDTH, 1), ball.movementcomponent.reverse_y)
ball_collider.add_collider(
    (0, tow.HEIGHT - 1, tow.WIDTH, 1), ball.movementcomponent.reverse_y
)
ball_collider.add_collider(
    (0, 0, 1, tow.HEIGHT),
    [ball.reset_ball, paddle1.reset_paddle, paddle2.reset_paddle, score2.add_score],
)
ball_collider.add_collider(
    (tow.WIDTH - 1, 0, 1, tow.HEIGHT),
    [ball.reset_ball, paddle1.reset_paddle, paddle2.reset_paddle, score1.add_score],
)
ball.add_component(ball_collider)

tow.add_object(divider)
tow.add_object(ball)
tow.add_object(paddle1)
tow.add_object(paddle2)
tow.add_object(score1)
tow.add_object(score2)

tow.run()
