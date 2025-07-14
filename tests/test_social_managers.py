from hololive_coliseum.currency_manager import CurrencyManager
from hololive_coliseum.title_manager import TitleManager
from hololive_coliseum.reputation_manager import ReputationManager
from hololive_coliseum.friend_manager import FriendManager
from hololive_coliseum.guild_manager import GuildManager
from hololive_coliseum.mail_manager import MailManager


def test_currency_manager():
    cm = CurrencyManager(10)
    cm.add(5)
    assert cm.get_balance() == 15
    assert cm.spend(7)
    assert cm.get_balance() == 8
    assert not cm.spend(20)


def test_title_and_reputation():
    tm = TitleManager()
    tm.unlock("Hero")
    assert tm.set_active("Hero")
    assert tm.get_active() == "Hero"
    rm = ReputationManager()
    assert rm.get("f") == 0
    rm.modify("f", 5)
    assert rm.get("f") == 5


def test_friend_and_guild():
    fm = FriendManager()
    fm.add_friend("alice")
    assert fm.is_friend("alice")
    fm.remove_friend("alice")
    assert not fm.list_friends()
    gm = GuildManager()
    gm.add_member("bob")
    gm.set_rank("bob", "leader")
    assert gm.get_rank("bob") == "leader"
    gm.remove_member("bob")
    assert gm.list_members() == {}


def test_mail_manager():
    mm = MailManager()
    mm.send_mail("c", "hi")
    assert mm.inbox("c") == ["hi"]
    mm.clear("c")
    assert mm.inbox("c") == []
