import json
import os
import argparse

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
    # compare file changes to the fingerprints create hashlist for files to avoid duplicated checks
    # count matches for each version to be able to find a possible match if some files got deleted or changed.
    pass


def main():
    parser = argparse.ArgumentParser("moodle-scanner")
    parser.add_argument("--host", help="Moodle host")
    parser.add_argument("--extended", help="Check for versions", type=bool)
    args = parser.parse_args()
    iterate_plugins(args.host, args.extended)


if __name__ == '__main__':
    main()
