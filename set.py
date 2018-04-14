
def contains_all(input, scopes):
    return all(x in input for x in scopes)

def contains_at_least(input, scopes):
    return any(x in input for x in scopes)

def check_scopes(input, scopes=[], req=[]):
    if not scopes or req:
        raise TypeError("Missing scopes")
    if req:
        return contains_all(input, req)
    return contains_at_least(input, scopes)

if __name__ == "__main__":
    li1 = ["a","b","c"]
    li2 = ["a","b","d"]

    print("check", check_scopes(["a"], li1))
