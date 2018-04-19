from s_class import S


def access_require(S_rule, token_scopes):
    def christmas_deco(func):
        def wrapper(*args, **kwargs):
            if S_rule.validate(token_scopes):
                return func(*args, **kwargs)
            return "Get out of this you sneaky dwarf !"
        return wrapper
    return christmas_deco


super_token_scopes = ["AtLeastaMurloc", "Peon"]

@access_require(S("AtLeastaMurloc") & S("Peon"), super_token_scopes)
def superfunction(a, b):
    """ My super function """
    return a + b


if __name__ == "__main__":
    print(superfunction(1, 2))
