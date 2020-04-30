import csv
from random import randint
from base64 import b64decode


def get_joke():
    with open('ans.csv', "r") as fin:
        reader = csv.reader(fin)
        ans = []
        # read csv for jokes
        for idx, row in enumerate(reader):
            # profanity filter
            bad = [b'YW5hbA==', b'YW51cw==', b'YXJzZQ==', b'YXNz', b'YmFsbHNhY2s=', b'YmFsbHM=', b'YmFzdGFyZA==', b'Yml0Y2g=', b'YmlhdGNo', b'Ymxvb2R5', b'Ymxvd2pvYg==', b'YmxvdyBqb2I=', b'Ym9sbG9jaw==', b'Ym9sbG9r', b'Ym9uZXI=', b'Ym9vYg==', b'YnVnZ2Vy', b'YnVt', b'YnV0dA==', b'YnV0dHBsdWc=', b'Y2xpdG9yaXM=', b'Y29jaw==', b'Y29vbg==', b'Y3JhcA==', b'Y3VudA==', b'ZGFtbg==', b'ZGljaw==', b'ZGlsZG8=', b'ZHlrZQ==', b'ZmFn', b'ZmVjaw==', b'ZmVsbGF0ZQ==', b'ZmVsbGF0aW8=', b'ZmVsY2hpbmc=', b'ZnVjaw==', b'ZiB1IGMgaw==', b'ZnVkZ2VwYWNrZXI=' b'c2VkdWNl',
                   b'ZnVkZ2UgcGFja2Vy', b'Zmxhbmdl', b'R29kZGFtbg==', b'R29kIGRhbW4=', b'aGVsbA==', b'aG9tbw==', b'amVyaw==', b'aml6eg==', b'a25vYmVuZA==', b'a25vYiBlbmQ=', b'bGFiaWE=', b'bG1hbw==', b'bG1mYW8=', b'bXVmZg==', b'bmlnZ2Vy', b'bmlnZ2E=', b'b21n', b'cGVuaXM=', b'cGlzcw==', b'cG9vcA==', b'cHJpY2s=', b'cHViZQ==', b'cHVzc3k=', b'cXVlZXI=', b'c2Nyb3R1bQ==', b'c2V4', b'c2hpdA==', b'cyBoaXQ=', b'c2gxdA==', b'c2x1dA==', b'c21lZ21h', b'c3B1bms=', b'dGl0', b'dG9zc2Vy', b'dHVyZA==', b'dHdhdA==', b'dmFnaW5h', b'd2Fuaw==', b'd2hvcmU=', b'd3Rm']
            # length/profanity filter
            if "read more" not in "".join(row[1:]) and "\n" not in "".join(row[1:]) and "NSFW" not in "".join(row[1:]):
                p = False
                for i in bad:
                    if b64decode(i).decode('utf-8') in "".join(row[1:]).lower():
                        p = True
                        break
                if not p:
                    if "".join(row[1])[-1] == "." or "".join(row[1])[-1] == "!" or "".join(row[1])[-1] == "?" or "".join(row[1])[-1] == ",":
                        ans.append(" ".join(row[1:]).strip())
                    else:
                        ans.append(". ".join(row[1:]).strip())
        fin.close()
    # return valid jokes
    return ans


with open('jokes.csv', "w+") as fout:
    writer = csv.writer(fout)
    for i in get_joke():
        writer.writerow([i])
    fout.close()
