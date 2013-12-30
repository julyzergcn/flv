
import re

fname = 'urls.txt'

html = open(fname).read()
lst = re.findall('(http://v\.youku\.com.*?)[\'"\r]', html, re.U)

if lst:
    f = open(fname, 'wb')
    for i in lst:
        print i
        f.write(i)
        f.write('\r\n')
    f.close()
