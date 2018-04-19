import logging
from logging import NullHandler

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: Separate from tricks:
#           string falsyness (eg: "" or scope_req)
#           Use something else than tuple to cast to set() safely ?
EMPTY_RESULT = ""


class S():

    def __init__(self, scope):
        self.scope_req = self.set_from_list_or_string(scope)
        self.result_in = EMPTY_RESULT
        self.history = list()

    @staticmethod
    def set_from_list_or_string(scopes):
        if type(scopes) is list:
            # Mind the comma, otherwise set split strings(=iterable) into s t r i n g s
            return set(scopes,)
        if type(scopes) is str:
            return set((scopes,))
        raise TypeError("Invalid type input in constructor S(), allowed: list and str, used: {}"
                        .format(type(scopes)))

    def validate(self, token_scopes):
        return self.result_in(token_scopes)

    @staticmethod
    def func_operator_in(operator, a, b):
        def finally_evaluate(token_scopes):
            local_a, local_b = a, b
            if callable(a):
                local_a = set((a(token_scopes),))
            if callable(b):
                local_b = set((b(token_scopes),))

            merge_required_scope = local_b.union(local_a)
            # Required to get previous True evaluations from the union, otherwise:
            #   True in token_scopes => False
            token_scopes_plus_true = token_scopes + [True]
            detected_scopes = [scope in token_scopes_plus_true for scope in merge_required_scope]
            return operator(detected_scopes)
        return finally_evaluate

    def __or__(self, other):
        """
            self.scope or other.scope
            self.scope in tokenscopes or other.scope in tokenscopes
            any(x in tokenscopes for x in [scope, other])
        """
        logger.debug("from __or__: self:{}, other{}".format(self.scope_req, other.scope_req))
        if other.history:
            self.history.append(other.history)
        self.history.append("{} or {}".format(self.scope_req, other.scope_req))

        # TODO: Merge result_in and scope_req by always rewriting scope_req but losing history ?
        # self.result_in = self.lambda_any_in(self.result_in or self.scope_req, other.scope_req)
        self.result_in = self.func_operator_in(any, self.result_in or self.scope_req,
                                               other.result_in or other.scope_req)
        self.scope_req = ("{} or {}".format(self.scope_req, other.scope_req))

        return self

    def __and__(self, other):
        """
            self.scope and other.scope
            self.scope in tokenscopes and other.scope in tokenscopes
            all(x in tokenscopes for x in [scope, other])
        """
        logger.debug("from __or__: self:{}, other{}".format(self.scope_req, other.scope_req))
        if other.history:
            self.history.append(other.history)
        self.history.append("{} and {}".format(self.scope_req, other.scope_req))

        self.result_in = self.func_operator_in(all, self.result_in or self.scope_req,
                                               other.result_in or other.scope_req)
        self.scope_req = ("{} and {}".format(self.scope_req, other.scope_req))

        return self

    def __str__(self):
        return str(self.history)

    def __repr__(self):
        return str(self.history)
