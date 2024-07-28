import hashlib

class Helper():
    
    def hash_password(self, password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        return hash_object.hexdigest()
    
    def format_number(self, number):
        if isinstance(number, float):
            if number.is_integer():
                return int(number)
            else:
                return f"{number:.2f}"
        return number