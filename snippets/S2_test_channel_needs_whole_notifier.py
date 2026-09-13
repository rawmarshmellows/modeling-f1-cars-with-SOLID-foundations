from notifications.notifiers.notifier_v1 import Notifier_v1


def test_email_channel_connects():
    notifier = Notifier_v1()  # only the notifier knows which channel to build, so we build all of it
    notifier.connect()
    assert notifier.channel.is_connected


test_email_channel_connects()
