import pytest
from jarvis_agent.security.policy import tokenize,PolicyError
def test_allowed_command(): assert tokenize('df -h')==['df','-h']
def test_reject_shell_injection():
    with pytest.raises(PolicyError): tokenize('df -h; whoami')
def test_reject_unknown_command():
    with pytest.raises(PolicyError): tokenize('curl example.com')
def test_reject_destructive_command():
    with pytest.raises(PolicyError): tokenize('rm -rf /')
