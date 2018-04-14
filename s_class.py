import logging
import inspect
from logging import NullHandler
from operator import contains

tk_scopes = ["a", "b"]

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


class S():

    def __init__(self, scope):
        if type(scope) is not list:
            scope = list(scope)
        self.scope_req = scope
        self.result_in = self
        self.history = list()

    def __or__(self, other):
        """
            self.scope or other.scope
            self.scope in tokenscopes or other.scope in tokenscopes
            any(x in tokenscopes for x in [scope, other])
        """
        logger.debug("from __or__: res:{}, self:{}, other{}".format(self.result_in, self.scope_req, other.scope_req))
        self.history.append("{} or {}".format(self.scope_req, other.scope_req))
        self.scope_req.extend(other.scope_req)
        self.result_in = lambda token_scopes: any(scope in token_scopes for scope in self.scope_req)
        logger.debug("from __or__: res:{}, self:{}, other{}".format(self.result_in, self.scope_req, other.scope_req))
        logger.debug("Lambda: {}".format(inspect.getsource(self.result_in)))
        return self

    def __and__(self, other):
        """
            self.scope and other.scope
            self.scope in tokenscopes and other.scope in tokenscopes
            all(x in tokenscopes for x in [scope, other])
        """
        logger.debug("from __or__: res:{}, self:{}, other{}".format(self.result_in, self.scope_req, other.scope_req))
        self.history.append("{} and {}".format(self.scope_req, other.scope_req))
        self.scope_req.extend(other.scope_req)
        self.result_in = lambda token_scopes: all(scope in token_scopes for scope in self.scope_req)
        logger.debug("from __or__: res:{}, self:{}, other{}".format(self.result_in, self.scope_req, other.scope_req))
        logger.debug("Lambda: {}".format(inspect.getsource(self.result_in)))
        return self

    def __str__(self):
        return str(self.history)

    def __repr__(self):
        return str(self.history)
"""
    A or B or C
    A or B => False
    False or C

    (A or B) and C
    A or B => False
    False and C
"""

if __name__ == "__main__":
    a, b, c = "a", "b", "c"
    token=["d"]

    if (a in token and b in token) or c in token:
        print("yep")
    else:
        print("nope")

    space = S("a") | S("b")