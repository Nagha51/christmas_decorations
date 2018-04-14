
def supervalidate(whocares):
    """ Everything's fine """
    return True

def access_require(yolo):
    def christmas_deco(func):
        def wrapper(*args, **kwargs):
            if supervalidate(yolo):
                return func(*args, **kwargs)
            return "Get out of this you sneaky dwarf !"
        return wrapper
    return christmas_deco


@access_require("AtLeastaMurloc")
def superfunction(a, b):
    """ My super function """
    return a + b


if __name__ == "__main__":
    superfunction(1, 2)
