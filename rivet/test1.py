
#%%
print(3+4)
globals()

var_rivet_dict ={}


def test1():
    b = 44
    c = 22
    d = b+c
    return var_rivet_dict.update(locals())


def test2():
    b = 11
    q = 22
    x = b+q
    return var_rivet_dict.update(locals())


test1()
print(var_rivet_dict)
test2()
print(var_rivet_dict)



α  ω  Ω   ∫ ∬  ⨌