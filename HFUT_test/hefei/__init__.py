import time

year, month, day = time.strftime("%Y-%m-%d", time.localtime()).split('-')
print year