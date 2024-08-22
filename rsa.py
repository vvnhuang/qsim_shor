from Crypto.PublicKey import RSA

from Crypto.Cipher import PKCS1_OAEP

from Crypto.Random import get_random_bytes
 
# 生成 RSA 密钥对

key = RSA.generate(1024)  # 生成 2048 位的 RSA 密钥
print(key)
private_key = key.export_key()  # 导出私钥
public_key = key.publickey().export_key()  # 导出公钥
print(public_key)
 
# 保存密钥到文件（可选）

with open("private.pem", "wb") as f:

    f.write(private_key)

with open("public.pem", "wb") as f:

    f.write(public_key)
 
# 打印生成的密钥

# print("Private Key:")

# print(private_key.decode())
 
# print("\nPublic Key:")

# print(public_key.decode())
 
# 加密消息

message = b"Hello, this is a secret message!"

cipher_rsa = PKCS1_OAEP.new(key.publickey())

ciphertext = cipher_rsa.encrypt(message)
 
# print("\nEncrypted message:")

# print(ciphertext)
 
# 解密消息

cipher_rsa = PKCS1_OAEP.new(key)

decrypted_message = cipher_rsa.decrypt(ciphertext)
 
# print("\nDecrypted message:")

# print(decrypted_message.decode())

 