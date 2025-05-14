def xoa_phantu(dictionary, key):
    if key in dictionary:
        del dictionary[key]
        return True
    else:
        return False

my_dict = {'a': 1, 'b': 2, 'c' : 3, 'd' : 4}
ky_to = 'b'
result = xoa_phantu(my_dict, ky_to)
if result:
    print("phan tu xoa", my_dict)
else:
    print(" Khong tim thay ")