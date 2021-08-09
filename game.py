import arcade

SPRITE_SCALING_PLATFORM = 0.25
SPRITE_SCALING_PLAYER = 0.25
SPRITE_SCALING_ENEMY = 0.15
PLAYER_JUMP_SPEED = 11
GRAVITY = 0.5
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
PLAYER_MOVEMENT_SPEED = 3.5
RIGHT_FACING = 0
LEFT_FACING = 1
ENEMY_SPEED = 3.5
PLAYER_FRAMES = 4
PLAYER_FRAMES_PER_TEXTURE = 4
TILE_SCALING = 1.75

def load_texture_pair(filename):
    
    return [
    arcade.load_texture(filename),
    arcade.load_texture(filename, flipped_horizontally=True)]

class Character(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.virtual_texture = 0
        self.idle_texture_pair = load_texture_pair("bach.png")
        self.texture = self.idle_texture_pair[self.character_face_direction]
        self.scale = SPRITE_SCALING_PLAYER

        self.walk_textures = []
        for i in range(4):
            texture = load_texture_pair(f"./Assets/Animations/sprite_{i}.png")
            self.walk_textures.append(texture)
        
        self.texture = self.idle_texture_pair[0]
    
    def update_animation(self, delta_time = 1/60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction] 
        else:
            self.virtual_texture += 1
            if self.virtual_texture > PLAYER_FRAMES * PLAYER_FRAMES_PER_TEXTURE:
                self.cur_texture = 0
                self.virtual_texture = 0
            if (self.virtual_texture +1) % PLAYER_FRAMES_PER_TEXTURE == 0:
                self.cur_texture = self.virtual_texture // PLAYER_FRAMES_PER_TEXTURE
                self.texture = self.walk_textures[self.cur_texture][
                    self.character_face_direction
                ]


class Enemy(arcade.Sprite):
    def __init__(self, x, y):

        super().__init__("Enemy.png", SPRITE_SCALING_ENEMY)
        self.center_x = x
        self.center_y = y
        self.change_x = ENEMY_SPEED
        self.start_x = x
        # self.change_y = ENEMY_SPEED
        self.start_y = y
        self.patrol = 500

    def update(self):
        self.center_x += self.change_x
        if self.center_x > self.start_x + self.patrol:
            self.change_x = -ENEMY_SPEED
        elif self.center_x < self.start_x - self.patrol:
            self.change_x = ENEMY_SPEED
        self.change_y -= GRAVITY
        self.center_y += self.change_y
        
        
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

        self.player_sprite = Character()
        self.player_sprite.center_x = 550
        self.player_sprite.center_y = 698
        self.player_list.append(self.player_sprite)

        

        map_name = ":resources:tmx_maps/map.tmx"

        platforms_layer_name = 'Ground'

        my_map = arcade.tilemap.read_tmx("Assets\Maps\Gangsta map.tmx")


        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                     layer_name=platforms_layer_name,
                                                     scaling=TILE_SCALING,
                                                     use_spatial_hash=True)

        enemy = Enemy(2040, 1032)
        self.enemy_list.append(enemy)

        self.background = arcade.load_texture("Background.png")

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
        
        # TODO Add enemies to list
        # When you start using TMX files, you will have them placed on the map in tiles and load them here:

            

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(self.get_viewport()[0], self.get_viewport()[2],
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
    
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()



    def update(self, delta_time):

        self.set_viewport(self.player_sprite.center_x - SCREEN_WIDTH/2, self.player_sprite.center_x + SCREEN_WIDTH/2, self.player_sprite.center_y - SCREEN_HEIGHT/2, self.player_sprite.center_y + SCREEN_HEIGHT/2)
        self.physics_engine.update()
        self.player_sprite.update()
        self.enemy_list.update()



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

        for enemy in self.enemy_list:
            
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1

    def on_mouse_press(self, x, y, button, modifiers):
        map_mouse_x = self.get_viewport()[0] + x
        map_mouse_y = self.get_viewport()[2] + y
        print(f'{map_mouse_x = } {map_mouse_y = } ')

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.UP:
            # if self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, symbol, modifiers):
        
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.change_y = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

