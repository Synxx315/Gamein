import random
import arcade

SPRITE_SCALING_PLATFORM = 0.25
SPRITE_SCALING_PLAYER = 0.25
PLAYER_JUMP_SPEED = 9
GRAVITY = 0.5
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
PLAYER_MOVEMENT_SPEED = 5

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")
        
        self.player_list = None
        self.physics_engine = None
        self.player_sprite = None
        self.wall_list = None

        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        wall = arcade.Sprite("New Piskel (2).png", SPRITE_SCALING_PLATFORM)
        wall.center_x = 300
        wall.center_y = 200
        self.wall_list.append(wall)

        self.player_sprite = arcade.Sprite("spoonful.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

            

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
        self.wall_list.draw()
    


    def update(self, delta_time):

        self.physics_engine.update()
        self.player_sprite.update()

        if self.player_sprite.center_x < SPRITE_SCALING_PLAYER:
            self.player_sprite.center_x = SPRITE_SCALING_PLAYER

        if self.player_sprite.center_x > SCREEN_WIDTH - SPRITE_SCALING_PLAYER:
            self.player_sprite.center_x = SCREEN_WIDTH - SPRITE_SCALING_PLAYER

        if self.player_sprite.center_y < SPRITE_SCALING_PLAYER:
            self.player_sprite.center_y = SPRITE_SCALING_PLAYER

        if self.player_sprite.center_y > SCREEN_HEIGHT - SPRITE_SCALING_PLAYER:
            self.player_sprite.center_y = SCREEN_HEIGHT - SPRITE_SCALING_PLAYER




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


def main():
    Window = MyGame()
    Window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

