import logging
import inspect
from logging import NullHandler
from operator import contains

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

# TODO: Separate from tricks:
#           string falsyness (eg: "" or scope_req)
#           + iterable (eg: b.union(""))
EMPTY_RESULT = ""

class S():


    def __init__(self, scope):
        # Mind the comma, otherwise set split strings(=iterable) into s t r i n g s
        self.scope_req = set(scope,)

        self.result_in = EMPTY_RESULT
        self.history = list()


    def validate(self, token_scopes):
        return self.result_in(token_scopes)

    @staticmethod
    def lambda_any_in(a, b):
        # Check if it's a function (eg: a lambda)
        # Check for last "and-or" operation, if different from current change management ?
        if callable(a):
            return lambda token_scopes: any(scope in token_scopes for scope in b) or a(token_scopes)
        return lambda token_scopes: any(scope in token_scopes for scope in b.union(a))

    @staticmethod
    def lambda_all_in(a, b):
        if callable(a):
            return lambda token_scopes: all(scope in token_scopes for scope in b) and a(token_scopes)
        return lambda token_scopes: all(scope in token_scopes for scope in b.union(a))

    def __or__(self, other):
        """
            self.scope or other.scope
            self.scope in tokenscopes or other.scope in tokenscopes
            any(x in tokenscopes for x in [scope, other])
        """
        logger.debug("from __or__: self:{}, other{}".format(self.scope_req, other.scope_req))
        self.history.append("{} or {}".format(self.scope_req, other.scope_req))

        # TODO: Merge result_in and scope_req by always rewriting scope_req but losing history ?
        self.result_in = self.lambda_any_in(self.result_in or self.scope_req, other.scope_req)

        return self

    def __and__(self, other):
        """
            self.scope and other.scope
            self.scope in tokenscopes and other.scope in tokenscopes
            all(x in tokenscopes for x in [scope, other])
        """
        logger.debug("from __or__: self:{}, other{}".format(self.scope_req, other.scope_req))
        self.history.append("{} and {}".format(self.scope_req, other.scope_req))

        self.result_in = self.lambda_all_in(self.result_in or self.scope_req, other.scope_req)

        return self

    def __str__(self):
        return str(self.history)

    def __repr__(self):
        return str(self.history)
"""
    (A & B) | C
    all(A, B) | C
    any(all(A,B), C)

    (A | B) & C
    any(A,B) & C
    all(any(A,B), C)
"""
