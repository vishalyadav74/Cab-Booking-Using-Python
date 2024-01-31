import hashlib
# from Services import Services
class SensitiveData:

    # @Services.timer_func
    def encryption(data):
        sha_hash = hashlib.sha256(data.encode()).hexdigest()
        # print("Encrypted Data:", sha_hash)
        return sha_hash

