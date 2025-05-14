def kiem_tra_so_nguyen (n):
    if n <= 1:
        return False
    for i in range(2, int (n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
number = int(input('Nhap vao so kiem tra: '))
if kiem_tra_so_nguyen (number):
    print(number, 'la so nguyen to')
else:
    print(number, 'khong phai so nguyen to')
