from cli2htm import convert
from fixtures_inline import TESTS as TESTS_INLINE
from fixtures_notinline import TESTS as TEST_NOTINLINE

def create_test(test, expected, **options):
    def f():
        assert convert(test, **options) == expected
    return f

def inject_tests():
    for i in range(len(TESTS_INLINE)):
        name = 'test_%d'%(i)
        test, expected = TESTS_INLINE[i]
        globals()[name] = create_test(test, expected, inline_style=True)

    for i in range(len(TEST_NOTINLINE)):
        name = 'test_notinline_%d'%(i)
        test, expected = TEST_NOTINLINE[i]
        globals()[name] = create_test(test, expected, inline_style=False)

inject_tests()
