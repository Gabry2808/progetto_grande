import arcade
SpriteList = arcade.SpriteList[arcade.Sprite]

def create_weapon_icon_textures() -> tuple[arcade.Texture, arcade.Texture]:
    boomerang_icon_texture = arcade.load_texture("assets/provided/boomerang-sheet.png")
    sword_icon_texture = arcade.load_texture("assets/provided/boomerang-sheet.png")
    return boomerang_icon_texture, sword_icon_texture

def create_weapon_icon(boomerang_icon_texture: arcade.Texture) -> arcade.Sprite:
    return arcade.Sprite(
        boomerang_icon_texture,
        scale=0.8,
    )

def create_weapon_icon_list(weapon_icon: arcade.Sprite) -> SpriteList:
    weapon_icon_list: SpriteList = arcade.SpriteList()
    weapon_icon_list.append(weapon_icon)
    return weapon_icon_list
