import magma as m

from magma.logging import (
    root_logger, stage_logger, unstage_logger, staged_logs
)
from magma.testing.utils import has_info


class _NamedObject:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


def test_basic_staging(caplog):
    msg = _NamedObject("foo")
    logger = root_logger()

    # First do a sanity check that staged logging without any modifications to
    # the staged object logs as expected.
    stage_logger()
    logger.info(msg)
    unstage_logger()
    assert caplog.records[-1].message == "foo"

    # Next check that modifying the object *after* staging & logging, but
    # *before* unstaging, logs the modified obejct.
    stage_logger()
    logger.info(msg)
    msg.name = "bar"
    unstage_logger()
    assert caplog.records[-1].message == "bar"


def test_nested_staging(caplog):
    msg = _NamedObject("foo")
    logger = root_logger()

    # Check that interleaving logging within unstaging works as expected. After
    # the first logger is unstaged, the log should be flushed to console, but
    # the outer logger should remain staged. Therefore, we should see one log
    # with "foo" right after the first unstage, and one log with "bar" after the
    # next unstage.
    stage_logger()
    stage_logger()
    logger.info(msg)
    unstage_logger()
    assert caplog.records[-1].message == "foo"
    logger.info(msg)
    msg.name = "bar"
    unstage_logger()
    assert caplog.records[-1].message == "bar"


def test_staged_logs_context_manager(caplog):
    msg = _NamedObject("foo")
    logger = root_logger()

    # Check that the staged_logs() context manager appropriately stages logs,
    # *and* the target returned from staged_logs() is the list of staged logs
    # itself.
    with staged_logs() as logs:
        logger.info(msg)
        msg.name = "bar"
    assert len(logs) == 1
    assert logs[0][2] is msg
    assert caplog.records[-1].message == "bar"
