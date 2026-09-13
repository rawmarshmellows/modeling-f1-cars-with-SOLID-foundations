# ...continuing from the previous snippet (error message as worded by Python 3.12+)
# TextBlasterSmsChannel_v2 subclasses ChannelInterface, but still has no connect()
ChannelFactory.create_textblaster_sms_channel_v2()
# raises: TypeError: Can't instantiate abstract class TextBlasterSmsChannel_v2 without an implementation for abstract method 'connect'
