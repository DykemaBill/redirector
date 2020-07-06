import sys
from base64 import b64encode, b64decode

# Simplecrypt
def main(mypassword):
    if mypassword:

        # Encode password
        passencoded = b64encode(mypassword.encode("utf-8"))
        print ("Here is your encoded password: " + str(passencoded))

        # Unencode byte
        passwordtext = b64decode(passencoded).decode("utf-8")

        print ("Here is your unencoded password: " + str(passwordtext))
        
    else:
        print ("You did not give me a password to encode!")

if __name__ == "__main__":
    main(sys.argv[1])