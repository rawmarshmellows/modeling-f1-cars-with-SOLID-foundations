import subprocess
import sys

from snippets.catalog import ROOT

MONDAY_MORNING = """\
from notifications.billing import CreditBalanceFactory
from notifications.channels import ChannelFactory
from notifications.notifiers.notifier_v5 import Notifier_v5

Notifier_v5(channel=ChannelFactory.create_textblaster_sms_channel_v3(), template=None, recipients=None, credit_balance=None)
Notifier_v5(channel=ChannelFactory.create_textblaster_sms_channel_v1(), template=None, recipients=None, credit_balance=None)
"""


def test_a_type_checker_rejects_a_channel_that_never_signed_the_contract(tmp_path):
    monday_morning = tmp_path / "monday_morning.py"
    monday_morning.write_text(MONDAY_MORNING)
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--no-incremental", str(monday_morning)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    report = result.stdout
    assert "monday_morning.py:5" not in report, report  # the channel that implements ChannelInterface is accepted
    assert (
        'monday_morning.py:6: error: Argument "channel" to "Notifier_v5" has incompatible type "TextBlasterSmsChannel_v1"'
        in report
    ), report
    # mypy also spots the factory that builds the channel which signed the contract without implementing connect()
    assert 'Cannot instantiate abstract class "TextBlasterSmsChannel_v2"' in report, report
