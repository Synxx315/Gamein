import random
import arcade


SPRITE_SCALING_PLAYER = 0.25
PLAYER_JUMP_SPEED = 20
GRAVITY = 1
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
PLAYER_MOVEMENT_SPEED = 15

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")
        
        self.player_list = None
        

        self.player_sprite = None
        self.score = 0

        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = arcade.Sprite("spoonful.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

            

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
    
    def update(self, delta_time):

        self.player_sprite.update()

        if self.player_sprite.center_x < SPRITE_SCALING_PLAYER:
            self.player_sprite.center_x = SPRITE_SCALING_PLAYER

        if self.player_sprite.center_x > SCREEN_WIDTH - SPRITE_SCALING_PLAYER:
            self.player_sprite.center_x = SCREEN_WIDTH - SPRITE_SCALING_PLAYER

        if self.player_sprite.center_y < SPRITE_SCALING_PLAYER:
            self.player_sprite.center_y = SPRITE_SCALING_PLAYER

        if self.player_sprite.center_y > SCREEN_HEIGHT - SPRITE_SCALING_PLAYER:
            self.player_sprite.center_y = SCREEN_HEIGHT - SPRITE_SCALING_PLAYER

        self.physics_engine.update()


    def on_key_press(self, symbol, modifiers):

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, symbol, modifiers):
        
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif symbol == arcade.key.UP:
            self.player_sprite.change_y = 0


def main():
    Window = MyGame()
    Window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

