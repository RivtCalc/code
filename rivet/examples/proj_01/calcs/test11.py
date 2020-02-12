
print(3+4)
xx,yy = 0,0

var_rivet_dict ={}


def test1():
    global xx, yy
    b = 44
    c = 22
    d = b+c
    xx = 5
    return var_rivet_dict.update(locals())


def test2():
    global xx, yy
    b = 11
    q = 22
    x = b+q
    xx = 15
    return var_rivet_dict.update(locals())

test1()
print(xx)
#print(var_rivet_dict)
test2()
print(xx)
#print(var_rivet_dict)


aa= """α  ω  Ω   ∫ ∬  ⨌"""
print(aa)