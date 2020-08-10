# -*- coding: utf-8 -*-
import base64
import binascii
import math
import random

from Crypto.Cipher import AES

import config


def rsa_encrypt(text, pub_key, modulus):
    """
    此处模拟RSA加密，需要注意的是，网易云对传入加密文本字符串数组是做了倒序处理的，所以我们也要倒序一下
    :param text:
    :param pub_key:
    :param modulus:
    :return:
    """
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16),
             int(pub_key, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def create_secret_key(size):
    """
    创建rsa加密密钥，a-zA-Z0-9随机16位字符串
    :param size:
    :return:
    """
    # return binascii.hexlify(os.urandom(size))[:16]
    b = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    c = ''
    for _ in range(size):
        e = random.random() * len(b)
        e = math.floor(e)
        c += b[e]
    return str.encode(c)


def aes_encrypt(text, sec_key):
    """
    模拟网易云的AES加密方式
    :param text:
    :param sec_key:
    :return:
    """
    pad = 16 - len(text) % 16
    text = text + bytearray([pad] * pad)
    encryptor = AES.new(sec_key, 2, b'0102030405060708')
    ciphertext = encryptor.encrypt(text)
    return base64.b64encode(ciphertext)


def create_params_and_seckey(text, pub_key, MODULUS, nonce):
    """
    这里就是创建params和enSecKey的地方
    :param text:
    :return:
    """
    try:
        sec_key = create_secret_key(16)  # 第二次加密使用的密匙
        result = aes_encrypt(text, nonce)  # 第一次使用默认密匙加密的结果
        enc_text = aes_encrypt(result, sec_key)  # 加密第一次的结果为params
        enc_sec_key = rsa_encrypt(sec_key, pub_key, MODULUS)
        return enc_text, enc_sec_key
    except Exception as e:
        config.logger1.exception("create_params_and_seckey 抛出异常:{}".format(e))


def dict_loop(array, dict):
    """
    简单做下汉字匹配字符，用于function_d函数传参，此处本可以直接用固定参数，因为从调试结果来看，这是个常量
    不过还是实现下网易云的代码，要是哪天常量也被改了呢
    :param array:
    :param dict:
    :return:
    """
    encrypted_data = []
    for i in array:
        encrypted_data.append(dict.get(i))
    # 这里做下字符转换
    return "".join(encrypted_data)


def obtain_params_and_seckey(body):
    params, encSecKey = create_params_and_seckey(body, dict_loop(["流泪", "强"], config.DICTIONARY), dict_loop(config.MD_ARRAY, config.DICTIONARY),
                                                 bytes(dict_loop(["爱心", "女孩", "惊恐", "大笑"], config.DICTIONARY), encoding="utf8"))
    return params, encSecKey


if __name__ == '__main__':
    obtain_params_and_seckey("dadaa")
