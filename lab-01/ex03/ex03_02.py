def dao_nguoc_list(lst):
    return lst[:: -1]
input_lst = input('Nhap danh sach cac so cach bang dau phay :')
numbers = list(map(int, input_lst.split(',')))


list_dao_nguoc = dao_nguoc_list(numbers)
print('list sau khi dao nguoc: ', list_dao_nguoc)