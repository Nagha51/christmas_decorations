import pytest
import logging
from logging import NullHandler
from s_class import S


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


@pytest.fixture(autouse=True)
def print_test_name(request):
    logger.debug("\n\n --- {} --- ".format(request.node.name))


def test_set_from_list_or_string_str():
    assert type(S.set_from_list_or_string("abc")) is set
    assert len(S.set_from_list_or_string("abc")) == 1


def test_set_from_list_or_string_list():
    assert type(S.set_from_list_or_string(["abc", "bcd"])) is set
    assert len(S.set_from_list_or_string(["abc", "bcd"])) == 2


def test_set_from_list_raises():
    with pytest.raises(TypeError):
        S.set_from_list_or_string(("not supported tuple",))


def test_1_or_ok():
    token_scopes = ["b"]
    s_a, s_b = S("a"), S("b")
    s_comb = s_a | s_b
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_1_or_ko():
    token_scopes = ["c"]
    s_a, s_b = S("a"), S("b")
    s_comb = s_a | s_b
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False


def test_2_or_ok():
    token_scopes = ["c"]
    s_a, s_b, s_c = S("a"), S("b"), S("c")
    s_comb = s_a | s_b | s_c
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_2_or_ko():
    token_scopes = ["d"]
    s_a, s_b, s_c = S("a"), S("b"), S("c")
    s_comb = s_a | s_b | s_c
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False


def test_1_and_ok():
    token_scopes = ["a", "b"]
    s_a, s_b = S("a"), S("b")
    s_comb = s_a & s_b
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_1_and_ko():
    token_scopes = ["a", "c"]
    s_a, s_b = S("a"), S("b")
    s_comb = s_a & s_b
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False


def test_2_and_ok():
    token_scopes = ["a", "b", "c"]
    s_a, s_b, s_c = S("a"), S("b"), S("c")
    s_comb = s_a & s_b & s_c
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_2_and_ko():
    token_scopes = ["a", "b", "c"]
    s_a, s_b, s_d = S("a"), S("b"), S("d")
    s_comb = s_a & s_b & s_d
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False


def test_or_and_ok():
    token_scopes = ["a", "b", "c"]
    s_a, s_b, s_c = S("a"), S("b"), S("c")
    s_comb = (s_a | s_b) & s_c
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_or_and_ko_or():
    token_scopes = ["a", "b", "c"]
    s_d, s_f, s_c = S("d"), S("f"), S("c")
    s_comb = (s_d | s_f) & s_c
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False


def test_or_and_ko_and():
    token_scopes = ["a", "b", "c"]
    s_a, s_d, s_f = S("a"), S("d"), S("f")
    s_comb = (s_a | s_d) & s_f
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False


def test_and_or_ok_or():
    token_scopes = ["a", "b", "c"]
    s_a, s_q, s_c = S("a"), S("q"), S("c")
    s_comb = (s_a & s_q) | s_c
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_and_or_ko():
    token_scopes = ["a", "b", "c"]
    s_a, s_q, s_z = S("a"), S("q"), S("z")
    s_comb = (s_a & s_q) | s_z
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False


def test_and_or_and_ok_and1():
    token_scopes = ["a", "b", "c"]
    s_a, s_c, s_b, s_z = S("a"), S("c"), S("b"), S("z")
    s_comb = (s_a & s_c) | (s_b & s_z)
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_and_or_and_ok_and2():
    token_scopes = ["a", "b", "c"]
    s_a, s_c, s_b, s_z = S("a"), S("c"), S("b"), S("z")
    s_comb = (s_a & s_z) | (s_b & s_c)
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_list_and_or_and_ok_and1():
    token_scopes = ["a", "b", "c"]
    s_ab, s_c, s_b, s_z = S(["a", "b"]), S("c"), S("b"), S("z")
    s_comb = (s_ab & s_c) | (s_b & s_z)
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == True


def test_list_and_or_and_ko():
    token_scopes = ["a", "b", "c"]
    s_az, s_c, s_b, s_z = S(["a", "z"]), S("c"), S("b"), S("z")
    s_comb = (s_az & s_c) | (s_b & s_z)
    logger.debug(s_comb.history)
    assert s_comb.validate(token_scopes) == False
