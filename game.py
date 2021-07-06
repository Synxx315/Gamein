import arcade

SPRITE_SCALING_PLATFORM = 0.25
SPRITE_SCALING_PLAYER = 0.25
SPRITE_SCALING_ENEMY = 0.15
PLAYER_JUMP_SPEED = 9
GRAVITY = 0.5
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
PLAYER_MOVEMENT_SPEED = 5
RIGHT_FACING = 0
LEFT_FACING = 1
ENEMY_SPEED = 2.5

def load_texture_pair(filename):
    
    return [
    arcade.load_texture(filename),
    arcade.load_texture(filename, flipped_horizontally=True)]

class Character(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.idle_texture_pair = load_texture_pair("bach.png")
        self.texture = self.idle_texture_pair[self.character_face_direction]
        self.scale = SPRITE_SCALING_PLAYER
        return
    
    def update_animation(self, delta_time = 1/60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        self.texture = self.idle_texture_pair[self.character_face_direction] 

class Enemy(arcade.Sprite):
    def __init__(self, x, y):

        super().__init__("Enemy.png", SPRITE_SCALING_ENEMY)
        self.center_x = x
        self.center_y = y
        self.change_x = ENEMY_SPEED
        self.start_x = x
        self.change_y = ENEMY_SPEED
        self.start_y = y
        self.patrol = 50

    def update(self):
        self.center_x += self.change_x
        if self.center_x > self.start_x + self.patrol:
            self.change_x = -ENEMY_SPEED
        elif self.center_x < self.start_x - self.patrol:
            self.change_x = ENEMY_SPEED
        
        
    # def on_draw(self):
    #     pass




class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")
        
        self.player_list = None
        self.physics_engine = None
        self.player_sprite = None
        self.wall_list = None
        self.enemy_sprite = None

        self.set_mouse_visible(True)

        self.background = None

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        wall = arcade.Sprite("New Piskel (2).png", SPRITE_SCALING_PLATFORM)
        wall.center_x = 300
        wall.center_y = 200
        self.wall_list.append(wall)

        self.player_sprite = Character()
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)
    
        enemy = Enemy(125, 300)
        self.enemy_list.append(enemy)

        self.background = arcade.load_texture("Background.png")

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        # TODO Add enemies to list
        # When you start using TMX files, you will have them placed on the map in tiles and load them here:

            

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
    
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()

    def update(self, delta_time):

        self.physics_engine.update()
        self.player_sprite.update()
        self.enemy_list.update()

        if self.player_sprite.center_x < SPRITE_SCALING_PLAYER:
            self.player_sprite.center_x = SPRITE_SCALING_PLAYER

        if self.player_sprite.center_x > SCREEN_WIDTH - SPRITE_SCALING_PLAYER:
            self.player_sprite.center_x = SCREEN_WIDTH - SPRITE_SCALING_PLAYER

        if self.player_sprite.center_y < SPRITE_SCALING_PLAYER:
            self.player_sprite.center_y = SPRITE_SCALING_PLAYER

        if self.player_sprite.center_y > SCREEN_HEIGHT - SPRITE_SCALING_PLAYER:
            self.player_sprite.center_y = SCREEN_HEIGHT - SPRITE_SCALING_PLAYER

        self.player_sprite.update_animation(delta_time)

        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        for enemy in enemy_hit_list:
            if enemy_hit_list:
                # figgure oput if player has jumped on enemy 
                if self.player_sprite.center_y - self.player_sprite.height /2 >= enemy.center_y + enemy.height/2 - 10:
                    enemy.kill()
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                else:
                    self.setup()


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
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

