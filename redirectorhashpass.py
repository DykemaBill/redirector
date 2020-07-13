import sys, bcrypt
from base64 import b64encode, b64decode

# Hash password
def main(mypassword):
    if mypassword:

        # Encode the password
        pass_encoded = b64encode(mypassword.encode("utf-8"))
        # Generate a one-time salt for this password in byte format
        pass_salt = bcrypt.gensalt()
        # Create hash of the password using the salt
        pass_hashed = bcrypt.hashpw(pass_encoded, pass_salt)
        # Decode salt and password hashed to make it easier to store
        pass_salt_decoded = pass_salt.decode("utf-8")
        pass_hashed_decoded = pass_hashed.decode("utf-8")
        # Combine them together
        pass_to_store = pass_salt_decoded + "-" + pass_hashed_decoded
        
        print ("Here is your password in clear text: " + mypassword)
        print ("Here is your salt and hashed password: " + str(pass_to_store))

        # Hash test
        # Get the new password
        test_password = mypassword
        # Encode the new password
        test_password_encoded = b64encode(test_password.encode("utf-8"))
        # Get the salt previously used
        test_pass_salt_decoded = pass_to_store.split('-')[0]
        # Convert the previously used salt from its decoded state to a byte
        test_pass_salt = test_pass_salt_decoded.encode("utf-8")
        # Create hash of new password using previously used salt
        test_pass_hashed = bcrypt.hashpw(test_password_encoded, test_pass_salt)
        # Decode the hash since that is how it would be stored
        test_pass_hashed_decoded = test_pass_hashed.decode("utf-8")

        if test_pass_hashed_decoded == pass_hashed_decoded:
            print ("We validated that the hash worked!")
        else:
            print ("Something went wrong, the hash did not work!")

    else:
        print ("You did not give me a password to hash!")

if __name__ == "__main__":
    main(sys.argv[1])