from notifications.channels import ChannelFactory


def test_email_channel_connects():
    channel = ChannelFactory.create_email_channel_v1()  # built exactly the way the notifier builds it
    channel.connect()
    assert channel.is_connected


test_email_channel_connects()
