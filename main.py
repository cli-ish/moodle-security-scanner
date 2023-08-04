import hashlib
import json
import os
import argparse
import re

import requests

with open('plugins/plugintype_map.json', 'r') as f:
    plugin_types = json.load(f)


def get_plugin_type_url(plugintype):
    return plugin_types[plugintype]


def test_plugin(host, plugin_name, plugin_type, extended_check):
    data = requests.get(host + get_plugin_type_url(plugin_type) + "/" + plugin_name + "/version.php")
    if data.status_code != 200:
        return False

    if extended_check:
        # changes_map = ["CHANGES.md", "CHANGES.txt", "CHANGES.html", "CHANGES"]
        # for changes in changes_map:
        #     data = requests.get(host + get_plugin_type_url(plugin_type) + "/" + plugin_name + "/" + changes)
        #     if data.status_code == 200:
        #         print(data.content.decode())
        #         break
        # git checken
        # index of checken
        pass

    return True


def iterate_plugins(host, extended_check=False):
    with os.scandir('plugins') as plugin_type_lists:
        for plugin_type in plugin_type_lists:
            if plugin_type.is_dir():
                # check index of option if available (some have index.php files by default so don't need to check these)
                with os.scandir('plugins/' + plugin_type.name) as plugins:
                    for plugin in plugins:
                        if plugin.is_dir():
                            sub_name = plugin.name[len(plugin_type.name) + 1:]
                            if test_plugin(host, sub_name, plugin_type.name, extended_check):
                                print(plugin.name)


def nail_moodle_version(host, extended_check=False):
    matching_factor = {}
    hashlist = {}
    with os.scandir('fingerprints') as fingerprints:
        for fingerprint in fingerprints:
            if fingerprint.name.endswith(".md") or fingerprint.name.endswith(".git"):
                continue
            with open(fingerprint.path, 'r') as file:
                for line in file.readlines():
                    parts = line.split("|")
                    if len(parts) < 2:
                        continue
                    hash_check = parts[1].strip("\n").strip("\r")
                    fingerprint_path = parts[0]

                    if fingerprint_path in hashlist.keys():
                        if hash_check == hashlist[fingerprint_path]:
                            if fingerprint.name in matching_factor.keys():
                                matching_factor[fingerprint.name] += 1
                            else:
                                matching_factor[fingerprint.name] = 1
                    else:
                        result = requests.get(host + "/" + fingerprint_path)
                        print("(" + fingerprint.name + ") Fetch:" + host + "/" + fingerprint_path)
                        if result.status_code == 200:
                            data = re.sub(r'[\n\r]+', '', result.content.decode())
                            sha_hash = hashlib.sha256()
                            sha_hash.update(data.encode())
                            hashlist[fingerprint_path] = sha_hash.hexdigest()
                            if hash_check == hashlist[fingerprint_path]:
                                # Todo: dont count this shit, we need more unique files. to ensure that we dont just
                                #  take the most.
                                if fingerprint.name in matching_factor.keys():
                                    matching_factor[fingerprint.name] += 1
                                else:
                                    matching_factor[fingerprint.name] = 1
                        else:
                            hashlist[fingerprint_path] = False


def main():
    parser = argparse.ArgumentParser("moodle-scanner")
    parser.add_argument("--host", help="Moodle host")
    parser.add_argument("--extended", help="Check for versions", type=bool, default=False)
    parser.add_argument("--nail", help="Nail down moodle version", type=bool, default=False)
    args = parser.parse_args()
    if args.nail:
        nail_moodle_version(args.host)

    # iterate_plugins(args.host, args.extended)


if __name__ == '__main__':
    main()
