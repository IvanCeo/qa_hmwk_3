# import uuid
# from datetime import date

# print(date.today() == date('2025-05-13'))

# print(str(uuid.uuid1()))

# # ee21cb76-3005-11f0-a671-803253436fb5
# # fc482609-3005-11f0-9e79-803253436fb5

# test = {'1': 1, 3: 12}

# if '1' not in test:
#     print('no')

import hashlib
data = "Hello, Python!"
hash_object = hashlib.md5(data.encode())
md5_hash = hash_object.hexdigest()
print(md5_hash)
