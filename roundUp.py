# -*- coding: utf-8 -*-

def roundUp(x, y=None):
    """ This method returns x rounded to n digits from the decimal point. """
    pos = str(x).find('.')
    if pos > 0:
        left, right = str(x)[:pos], str(x)[pos+1:]
        if y != None:
            if len(right) > y:
                if int(right[y]) > 4:
                    right = right[:y-1] + str(int(right[y-1])+1) 
                right = right[:y]
            return float(left + '.' + right)
        else:
            if int(right[0])>4:
                left = left[:len(left)-1] + str(int(left[len(left)-1]) + 1)
            return float(left)
    else:
        return float(x)

    



# if __name__ == '__main__':                     
#     # x = input('Enter the number: ')
#     # y = input('Enter the rank: ')
#     # print 'You enter the number: {}  \nYou enter the rank: {}'.format(x,y) 
#     print roundUp(x, y)
