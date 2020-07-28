import sys, pyodbc

# Start of program here
def main(sqlserver, sqldb, sqlschema, sqltable, sqlwhere, sqlwhereval, sqlcheck, sqlcheckval, sqluser, sqlpass):

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
                print ("Test result is positive!")
            else:
                print ("Test result is negative!")
        sqlresult = sqlcursor.fetchone()


# Get command line arguments
if __name__ == "__main__":
    if len(sys.argv) == 11:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
    else:
        print ("Syntax: " + sys.argv[0] + " [server] [database] [schema] [table] [fieldfilter] [fieldfiltervalue] [fieldcheck] [fieldcheckvalue] [user] [pass]")