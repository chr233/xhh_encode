import base64, hmac
'''
# @Author       : Chr_
# @Date         : 2022-11-07 13:51:16
# @LastEditors  : Chr_
# @LastEditTime : 2022-11-07 13:51:17
# @Description  : 
'''

# # urlpath = '/account/data_report/'
# # urlpath = '/task/list/'
# # urlpath='/account/game_servers/'
# urlpath='/task/shared/'
# # timecasp = '1647164504'
# # timecasp = '1647164500'
# # timecasp='1647531107'
# # timecasp='1647531690'
# timecasp='1647532036'
# # nonce = '6lncT8WvJH8y6DBXKVSslaPWlq7G945s'
# # nonce = 'JiuY3hLXBSUdrAcEb1L0WwPLR4zU4sRs'
# # nonce='Rrfm9StYj1JfmFRmeebC1EI67dtnXo7X'
# # nonce='tMURs8h8hgjUVostJ7KIsDre1LVQIBgt'
# nonce='oPgiofse6BGT83n3dy57DRdpe5BBHB7r'

def hkeyencode(urlpath,timecasp,nonce):
    # 时间戳增加
    def time_add(none):
        v14 = 0
        v17 = 0
        while v14 < len(none):
            v18 = ord(none[v14])
            v19 = v18 - 48
            v14 = v14 + 1
            if v19 < 0xA:
                v17 = v17 + 1
        return v17

    nonce_str = nonce.upper()
    sha1_key = base64.b64encode(urlpath.encode()).decode()
    time_addi = time_add(nonce)
    
    # 修复错误
    sha1_str = ((hex(int(timecasp) + time_addi)[2:]).rjust(16,'0')).upper()
    
    sha1 = hmac.new(sha1_key.encode(), bytes.fromhex(sha1_str), digestmod='sha1').hexdigest()
    sha1_index = int(int('0x' + sha1[-2:], 16) & 0xf)
    hkey_index_befor = int(sha1[sha1_index * 2:sha1_index * 2 + 8], 16) & 0x7fffffff
    hkey_str = '6789BCDFGH2345JKMNPQRTVWXY' + nonce_str


    # 索引循环主要函数
    def sub_3780(a1, a2):
        a1_eor_a2 = a1 ^ a2
        if a2 == 1:
            if (a1_eor_a2 ^ a1) < 0:
                a1 = -a1
        else:
            temp = a1
            if a1 < 0:
                temp = -a1
            if temp <= a2:
                if temp < a2:
                    a1 = 0
                if temp == a2:
                    a1 = (a1_eor_a2 >> 31) | 1
            elif (a2 & (a2 - 1)) != 0:
                v5 = _clz(a2) - _clz(temp)
                v6 = a2 << v5
                v7 = 1 << v5
                a1 = 0
                while True:
                    if temp >= v6:
                        temp = temp - v6
                        a1 = a1 | v7
                    if temp >= v6 >> 1:
                        temp = temp - (v6 >> 1)
                        a1 = a1 | v7 >> 1
                    if temp >= v6 >> 2:
                        temp = temp - (v6 >> 2)
                        a1 = a1 | v7 >> 2
                    if temp >= v6 >> 3:
                        temp = temp - (v6 >> 3)
                        a1 = a1 | v7 >> 3
                    v8 = temp == 0
                    if temp != 0:
                        v7 = v7 >> 4
                        v8 = v7 == 0
                    if v8:
                        break
                    v6 = v6 >> 4
                if a1_eor_a2 < 0:
                    a1 = -a1
            else:
                a1 = temp >> (31 - _clz(a2))
                if a1_eor_a2 < 0:
                    a1 = -a1
        return a1


    # arm指令
    def _clz(x):
        total_bits = 32
        res = 0
        while (x & (1 << (total_bits - 1))) == 0:
            x = (x << 1)
            res = res + 1
        return res


    hkey_part5 = ''
    for i in range(0, 5):
        V20 = sub_3780(hkey_index_befor, 58)
        hkey_index = hkey_index_befor - 58 * V20
        hkey_index_befor = V20
        hkey_part5 = hkey_part5 + hkey_str[hkey_index]

    hkey_part4 = hkey_part5[1:]


    # hkey后两位 计算
    def sub_194c(total):
        def sub_18d4(a1):
            v1 = ((a1 * 2) ^ 0x1b) & 0xff
            if a1 & 0x80 == 0:
                v1 = a1 * 2
            v2 = ((v1 * 2) ^ 0x1b) & 0xff
            if v1 & 0x80 == 0:
                v2 = v1 * 2
            return v2 ^ v1

        def sub_18f8(a2):
            v1 = ((a2 * 2) ^ 0x1b) & 0xff
            if a2 & 0x80 == 0:
                v1 = a2 * 2
            v2 = ((v1 * 2) ^ 0x1b) & 0xff
            if v1 & 0x80 == 0:
                v2 = v1 * 2
            return sub_18d4(v2 ^ v1)

        def sub_191e(a3):
            v2 = (a3 & 0x80) != 0
            v3 = ((a3 * 2) ^ 0x1b) & 0xff
            if not v2:
                v3 = a3 * 2
            v4 = v3 ^ a3 ^ sub_18f8(a3)
            return sub_18d4(a3) ^ v4

        part1 = int('0x' + total[0].encode().hex(), 16)
        part2 = int('0x' + total[1].encode().hex(), 16)
        part3 = int('0x' + total[2].encode().hex(), 16)
        v5 = ((part2 * 2) ^ 0x1b) & 0xff
        if part2 & 0x80 == 0:
            v5 = part2 * 2
        v17 = v5 ^ part2
        v23 = sub_191e(part1)
        v22 = sub_18f8(part2)
        v21 = sub_18d4(part3)
        v6 = int('0x' + total[3].encode().hex(), 16)
        v20 = sub_191e(part2)
        v19 = sub_18f8(part3)
        v18 = sub_18d4(v6)
        v7 = v17 ^ sub_18d4(part1)
        v8 = v7 ^ sub_191e(part3)
        v9 = v8 ^ sub_18f8(v6)
        v10 = sub_18f8(part1)
        v11 = sub_18d4(part2)
        v12 = sub_191e(v6)
        total2 = v9
        v13 = ((part1 * 2) ^ 0x1b) & 0xff
        if part1 & 0x80 == 0:
            v13 = part1 * 2
        total1 = v13 ^ part1 ^ v20 ^ v19 ^ v18
        v14 = ((v6 * 2) ^ 0x1b) & 0xff
        if v6 & 0x80 == 0:
            v14 = v6 * 2
        total0 = v14 ^ v23 ^ v22 ^ v21 ^ v6
        v15 = ((part3 * 2) ^ 0x1b) & 0xff
        if part3 & 0x80 == 0:
            v15 = part3 * 2
        total3 = v12 ^ v15 ^ part3 ^ v10 ^ v11
        return total0 + total1 + total2 + total3


    hkey_part2 = sub_194c(hkey_part4)
    hund = sub_3780(hkey_part2, 100)
    hkey_part = hkey_part2 - hund * 100
    hkey = ''
    if hkey_part < 10:
        hkey=hkey_part5 + f'0{hkey_part}'
        return hkey
    else:
        hkey = hkey_part5 + f'{hkey_part}'
        # print(hkey)
        return hkey

# print(hkeyencode(urlpath,timecasp,nonce))