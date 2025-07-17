import os
import pygame


def test_level_manager_sets_up_groups(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.ai_players = 1
    game.selected_character = "Gawr Gura"
    game.level_manager.setup_level()
    assert isinstance(game.player, game.player.__class__)
    assert len(game.enemies) == 1
    assert game.spawn_manager.spawns
    pygame.quit()
