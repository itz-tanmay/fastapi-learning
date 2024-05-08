import bcrypt


class CustomBcryptComtext:
    """This Is The Custom Made Hashing Class Made As 'bcrypt' Was Causing An Error."""
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(password, hashed_password):
        # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
