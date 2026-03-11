import sys
import pytest
import traceback

try:
    with open('pytest_log.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f
        sys.stderr = f
        pytest.main(['skbase/tests/test_repr_html.py', '-vv', '--color=no'])
except Exception:
    with open('pytest_log.txt', 'a', encoding='utf-8') as f:
        traceback.print_exc(file=f)
