# Test SQL password of Ch@ng3MEN0w! using the below key would be gAAAAABfItxvPQigOIgyfD8vV1EUr9iZSlOgYJYN6fex6FTjslRVGuauzwiCSKnIlcfFrWP9vQwakiZILwIDFIOdAT7PjRbOSA==

# Test example
# 
# python3 redirectormssqlcheck.py sqlserver TestDB test Test NameLast Johnson TestID 2 sa gAAAAABfItxvPQigOIgyfD8vV1EUr9iZSlOgYJYN6fex6FTjslRVGuauzwiCSKnIlcfFrWP9vQwakiZILwIDFIOdAT7PjRbOSA==
# 
# (1, 'Bob', 'Smith', datetime.date(1970, 1, 1))
# (2, 'Beth', 'Johnson', datetime.date(1971, 1, 1))
# (3, 'Julie', 'Miller', datetime.date(1972, 1, 1))
# (4, 'John', 'Davis', datetime.date(1973, 1, 1))
#
# You wanted to know if TestID equals 2 for Johnson, TestID equals 2 for Johnson.
# Test result is positive!
#  
# python3 redirectormssqlcheck.py sqlserver TestDB test Test NameLast Johnson TestID 3 sa gAAAAABfItxvPQigOIgyfD8vV1EUr9iZSlOgYJYN6fex6FTjslRVGuauzwiCSKnIlcfFrWP9vQwakiZILwIDFIOdAT7PjRbOSA==
# 
# (1, 'Bob', 'Smith', datetime.date(1970, 1, 1))
# (2, 'Beth', 'Johnson', datetime.date(1971, 1, 1))
# (3, 'Julie', 'Miller', datetime.date(1972, 1, 1))
# (4, 'John', 'Davis', datetime.date(1973, 1, 1))
#
# You wanted to know if TestID equals 3 for Johnson, TestID equals 2 for Johnson.
# Test result is negative!
# 


import sys, pyodbc
import redirectorencryptpass as encryptpass

# Decryption key for DB passwords
decryption_key = '2_uUVgunK59ghEWlPjvmaeCFoDrWiPDzS7dGi7I7mO4='

# Start of SQL check here
def check(sqlserver, sqldb, sqlschema, sqltable, sqlwhere, sqlwhereval, sqlcheck, sqlcheckval, sqluser, sqlpassencrypted):

    # Get SQL password to use by decrypting supplied password
    sqlpass = encryptpass.passdecrypt(decryption_key, sqlpassencrypted)

    # Values to use
    # print ("Server: " + sqlserver)
    # print ("Database: " + sqldb)
    # print ("Schema: " + sqlschema)
    # print ("Table: " + sqltable)
    # print ("Field filter: " + sqlwhere)
    # print ("Field filter value: " + sqlwhereval)
    # print ("Field check: " + sqlcheck)
    # print ("Field check value: " + sqlcheckval)
    # print ("User: " + sqluser)
    # print ("Password: *********")

    # Build connection to SQL
    sqlconn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+sqlserver+';DATABASE='+sqldb+';UID='+sqluser+';PWD='+ sqlpass)
    sqlcursor = sqlconn.cursor()

    # Get SQL Server info
    # sqlcursor.execute("SELECT @@version;") 
    # sqlrow = sqlcursor.fetchone() 
    # while sqlrow:
    #     print(sqlrow[0])
    #     sqlrow = sqlcursor.fetchone()
    
    # Read SQL Server table
    # sqlcursor.execute("SELECT * FROM " + sqldb + "." + sqlschema + "." + sqltable) 
    # sqlrow = sqlcursor.fetchone() 
    # while sqlrow:
    #     print(sqlrow)
    #     sqlrow = sqlcursor.fetchone()

    # Run SQL check
    sqlcursor.execute("SELECT " + sqlcheck + " FROM " + sqldb + "." + sqlschema + "." + sqltable + " WHERE " + sqlwhere + "= '" + sqlwhereval + "'")
    sqlresult = sqlcursor.fetchone()
    while sqlresult:
        if sqlresult[0]:
            print("You wanted to know if " + sqlcheck + " equals " + sqlcheckval + " for " + sqlwhereval + ",", sqlcheck + " equals", sqlresult[0], "for " + sqlwhereval + ".")
            if int(sqlcheckval) == int(sqlresult[0]):
                return True
            else:
                return False
        sqlresult = sqlcursor.fetchone()
    return False


# Get command line arguments
if __name__ == "__main__":
    if len(sys.argv) == 11:
        myCheck = check(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
        if myCheck:
            print ("Test result is positive!")
        else:
            print ("Test result is negative!")

    else:
        print ("Syntax: " + sys.argv[0] + " [server] [database] [schema] [table] [fieldfilter] [fieldfiltervalue] [fieldcheck] [fieldcheckvalue] [user] [passencrypted]")