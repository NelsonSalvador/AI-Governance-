from app.governance import can_access, redact
from app.pipeline import handle


def test_access_denied_for_low_clearance():
    out = handle("show me the client file", role="analyst", classification="client")
    assert "error" in out


def test_advisor_can_access_client_data():
    out = handle("portfolio review", role="advisor", classification="client")
    assert "answer" in out


def test_redaction_masks_email():
    red, found = redact("mail me at anna@example.com")
    assert "anna@example.com" not in red
    assert "EMAIL" in found


def test_clearance_map():
    assert can_access("advisor", "client")
    assert not can_access("analyst", "restricted")
