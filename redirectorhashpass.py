import sys, os, hashlib
from base64 import b64encode, b64decode

# Hash password
# From https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
def main(mypassword):
    if mypassword:

        # Hash password
        pass_salt_iterations = 100000
        pass_salt = os.urandom(32) # Secret salt for hash
        pass_hashed = hashlib.pbkdf2_hmac('sha256', mypassword.encode('utf-8'), pass_salt, pass_salt_iterations)

        # Encode password to make it easier to store
        pass_salt_encoded = b64encode(pass_salt.encode("utf-8"))
        pass_hashed_encoded = b64encode(pass_hashed.encode("utf-8"))
        
        print ("Here is your password in clear text: " + mypassword)

        # You would keep the following encode salt and encoded hashed password stored together
        print ("Here is your hashed password salt: " + str(pass_salt_encoded))
        print ("Here is your hashed password: " + str(pass_hashed_encoded))

        # Hash test
        test_pass_salt_iterations = pass_salt_iterations
        testpassword = mypassword
        test_pass_salt = pass_salt
        test_pass_salt_encoded = b64encode(test_pass_salt.encode("utf-8"))
        test_pass_hashed = hashlib.pbkdf2_hmac('sha256', testpassword.encode('utf-8'), test_pass_salt, test_pass_salt_iterations)
        test_pass_hashed_encoded = b64encode(test_pass_hashed.encode("utf-8"))

        if test_pass_hashed_encoded == pass_hashed_encoded:
            print ("We validated that the encoded hash worked!")
        else:
            print ("Something went wrong, the encoded hash did not work!")

    else:
        print ("You did not give me a password to hash!")

if __name__ == "__main__":
    main(sys.argv[1])