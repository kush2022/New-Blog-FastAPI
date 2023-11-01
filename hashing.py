from passlib.context import CryptContext



pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        hassedPassword = pwd_cxt.hash(password)

        return hassedPassword
    
    def verify(plainPassword, hashedPassword):
        return pwd_cxt.verify(plainPassword, hashedPassword)

