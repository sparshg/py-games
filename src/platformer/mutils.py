import decimal

class MUtils:
    def __init__(self):
        pass
    def sign_of(self, num):
        if num < 0:
            return -1
        else:
            return 1
    def percision_of(self, num):
        percision = decimal.Decimal(num)
        percision = len(str(num).split('.')[1])
        return percision

mutils = MUtils()
