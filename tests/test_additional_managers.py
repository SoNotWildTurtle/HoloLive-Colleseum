import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum.auth_manager import AuthManager
from hololive_coliseum.cheat_detection_manager import CheatDetectionManager
from hololive_coliseum.ban_manager import BanManager
from hololive_coliseum.data_protection_manager import DataProtectionManager
from hololive_coliseum.logging_manager import LoggingManager
from hololive_coliseum.ui_manager import UIManager
from hololive_coliseum.notification_manager import NotificationManager
from hololive_coliseum.input_manager import InputManager
from hololive_coliseum.accessibility_manager import AccessibilityManager
from hololive_coliseum.chat_manager import ChatManager
from hololive_coliseum.voice_chat_manager import VoiceChatManager
from hololive_coliseum.emote_manager import EmoteManager
from hololive_coliseum.sound_manager import SoundManager
from hololive_coliseum.effect_manager import EffectManager


def test_auth_and_ban_managers():
    auth = AuthManager()
    auth.register('u', 'p')
    token = auth.login('u', 'p')
    assert token and auth.verify(token)
    ban = BanManager()
    ban.ban('u')
    assert ban.is_banned('u')
    ban.unban('u')
    assert not ban.is_banned('u')


def test_cheat_detection_and_logging():
    cheat = CheatDetectionManager()
    log = LoggingManager()
    if cheat.check_speed(11, 10):
        log.log('speed')
    assert log.events == ['speed']


def test_data_protection_roundtrip():
    dp = DataProtectionManager(b'k')
    enc = dp.encrypt(b'abc')
    assert dp.decrypt(enc) == b'abc'


def test_ui_and_notification_managers():
    ui = UIManager()
    ui.add('menu')
    ui.remove('menu')
    assert not ui.elements
    nm = NotificationManager()
    nm.push('hi')
    assert nm.pop() == 'hi'


def test_input_and_accessibility():
    im = InputManager({'jump': 1})
    assert im.get('jump') == 1
    im.set('fire', 2)
    assert im.get('fire') == 2
    am = AccessibilityManager()
    orig = am.options['colorblind']
    am.toggle('colorblind')
    assert am.options['colorblind'] != orig


def test_chat_and_voice_managers():
    chat = ChatManager(max_messages=2)
    chat.show()
    assert chat.open
    chat.send('a', 'hi')
    chat.send('b', 'yo')
    chat.send('c', 'hey')
    assert chat.history() == [('b', 'yo'), ('c', 'hey')]
    chat.hide()
    assert not chat.open
    voice = VoiceChatManager()
    voice.join('a', 'c1')
    assert 'a' in voice.channels['c1']
    voice.leave('a', 'c1')
    assert 'c1' not in voice.channels


def test_emote_sound_effect():
    em = EmoteManager()
    em.add('smile', ':)')
    assert em.get('smile') == ':)'
    sound = SoundManager()
    sound.play('ding')
    assert sound.last_played == 'ding'
    sound.stop()
    assert sound.last_played is None
    effect = EffectManager()
    effect.trigger('boom')
    assert 'boom' in effect.active
