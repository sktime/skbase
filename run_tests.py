import traceback

try:
    import pytest
    pytest.main(['skbase/tests/test_repr_html.py', '-vv', '--color=no'])
except Exception:
    with open('test_output.txt', 'w', encoding='utf-8') as f:
        traceback.print_exc(file=f)
