"""
This module is used for generating the file containing all the hashes

To use it, execute `python generate.py`
"""
from os import remove as rmfile
from urllib.request import urlretrieve
from urllib.error import URLError, HTTPError
from socket import create_connection
from os.path import isfile
import sqlite3
from sqlite3 import Error

def dbConnect():
	conn = sqlite3.connect('History_Data.db')
	return conn
	print("Connected Successfully")

def dbCreate():
	conn=dbConnect()
	conn.execute(''' CREATE TABLE if not exists Bad_Hash (id INTEGER PRIMARY KEY AUTOINCREMENT ,md5 STRING);''')
	#print("Table Created Successfully")

def dbInsert(d):
	conn=dbConnect()
	c=conn.cursor()
	c.execute('INSERT INTO Bad_Hash(id,md5) values(NULL,"'+d+'");')
	conn.commit()
	conn.close()
	print("Inserted TO DB : "+d)

# Check for internet connection
print("Checking for an internet connection...")
try:
    create_connection(("www.google.com", 443))
    print("Internet connection established!")
except OSError:
    print("Please connect to the internet!")
    exitexec(1)



# Clear Temporary File
if isfile("newhashes.txt"):
    print("Removing temporary hashes file...")
    print("Action completed!", end="\n")

dbCreate()
# Find all possible files
for i in range(3, 350):
    print("Trying https://virusshare.com/hashes/VirusShare_{0}.md5...".format(
        str(i).zfill(5)))
    try:

        # Try to download file
        urlretrieve(
            "https://virusshare.com/hashes/VirusShare_{0}.md5".format(
                str(i).zfill(5)), "newhashes.txt")
        print("Download success!")
        print("Appending...")
        with open("newhashes.txt", "r") as ff:
            for ii in enumerate(ff.readlines()):
                if not str(ii[1]).startswith("#"):
                    dbInsert(str(ii[1]))    
        print("DB load Complete!")
        print("Removing temporary file...")

        # Remove temporary file
        rmfile("newhashes.txt")
        print("Operation for file " + str(i).zfill(5) + " complete.", end="\n")

    # Catch HTTP response code
    except HTTPError as e:

        # Check if code is 404
        if e.code == 404:
            print("File " + str(i).zfill(5) + " not found.")
            print("Stopping...")
            break

        # Otherwise raise an error
        else:
            print("An error has occured: Recieved URL response code " + e.code)

            # Exit the execution with a value of 1
            exitexc(1)

    # Catch server error
    except URLError as e:

        # Raise an error
        print("Unable to reach the server: Reason provided is " + str(e.reason))

        # Exit the execution with a value of 1
        exitexc(1)

    # Catch any other exception
    except Exception as exc:

        # Raise an error
        print("ERROR: An error of type {0} occured because {1}".format(
            type(exc).__name__, str(exc.args[0])))

        # Exit the execution with a value of 1
        exitexc(1)

# Notify user of completion
print("Hashes file creation complete.")
