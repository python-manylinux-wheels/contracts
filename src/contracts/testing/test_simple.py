import traceback
import pytest

from ..main import parse_contract_string
from ..test_registrar import (good_examples, semantic_fail_examples,
                              syntax_fail_examples, contract_fail_examples)
from .utils import check_contracts_ok, check_syntax_fail, check_contracts_fail

# Import the other tests
from . import test_multiple  # @UnusedImport

# Import all the symbols needed to eval() the __repr__() output.
from ..library import *  # @UnusedWildImport @UnresolvedImport


## If you want to try only some tests, set select to True, and add them below.
## Remove the other mcdp_lang_tests
#good_examples[:] = []
#syntax_fail_examples[:] = []
#semantic_fail_examples[:] = []
#contract_fail_examples[:] = []
#
## Add the ones you want to do here:
#from ..test_registrar import  fail, good, syntax_fail, semantic_fail 


@pytest.mark.parametrize("contract,value,exact", good_examples)
def test_good(contract, value, exact):
    check_contracts_ok(contract, value)


@pytest.mark.parametrize("s", syntax_fail_examples)
def test_syntax_fail(s):
    check_syntax_fail(s)


@pytest.mark.parametrize("contract,value,exact", semantic_fail_examples)
def test_semantic_fail(contract, value, exact):
    check_contracts_fail(contract, value, ContractNotRespected)


@pytest.mark.parametrize("contract,value,exact", contract_fail_examples)
def test_contract_fail(contract, value, exact):
    check_contracts_fail(contract, value, ContractNotRespected)


def get_repr_test_cases():
    test_cases = []
    allc = (good_examples + semantic_fail_examples + contract_fail_examples)
    for contract, value, exact in allc:  # @UnusedVariable
        if isinstance(contract, list):
            test_cases.extend(contract)
        else:
            test_cases.append(contract)
    return test_cases


# Checks that we can eval() the __repr__() value and 
# we get an equivalent object. 
@pytest.mark.parametrize("contract", get_repr_test_cases())
def test_repr(contract):
    check_good_repr(contract)


def get_reconversion_test_cases():
    test_cases = []
    allc = (good_examples + semantic_fail_examples + contract_fail_examples)
    for contract, _, exact in allc:
        if isinstance(contract, list):
            for c in contract:
                test_cases.append((c, exact))
        else:
            test_cases.append((contract, exact))
    return test_cases


#  Checks that we can reconvert the __str__() value and we get the same. 
@pytest.mark.parametrize("contract,exact", get_reconversion_test_cases())
def test_reconversion(contract, exact):
    check_recoversion(contract, exact)


def check_good_repr(c):
    """ Checks that we can eval() the __repr__() value and we get
        an equivalent object. """
    parsed = parse_contract_string(c)
    # Check that it compares true with itself
    assert parsed.__eq__(parsed), 'Repr does not know itself: %r' % parsed

    reprc = parsed.__repr__()

    try:
        reeval = eval(reprc)
    except Exception as e:
        traceback.print_exc()
        raise Exception('Could not evaluate expression %r: %s' % (reprc, e))

    assert reeval == parsed, \
            'Repr gives different object:\n  %r !=\n  %r' % (parsed, reeval)


def check_recoversion(s, exact):
    """ Checks that we can eval() the __repr__() value and we get
        an equivalent object. """
    parsed = parse_contract_string(s)

    s2 = parsed.__str__()
    reconv = parse_contract_string(s2)

    msg = 'Reparsing gives different objects:\n'
    msg += '  Original string: %r\n' % s
    msg += '           parsed: %r\n' % parsed
    msg += '      Regenerated: %r\n' % s2
    msg += '         reparsed: %r' % reconv

    assert reconv == parsed, msg

    if exact:
        # Warn if the string is not exactly the same.
        if s2 != s:
            msg = ('Slight different regenerated strings:\n')
            msg += ('   original: %s\n' % s)
            msg += ('  generated: %s\n' % s2)
            msg += ('   parsed the first time as: %r\n' % parsed)
            msg += ('                and then as: %r' % reconv)
            assert s2 == s, msg




