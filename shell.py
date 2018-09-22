import sys
flag = 1
while flag == 1:
    s = input("Enter command: ")
    if s == 'x':
        flag = 0
        print('exit...')
    else:
        print("You entered: {}".format(s))
    sys.stdout.flush()