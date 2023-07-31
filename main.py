import json
import os

import requests

with open('plugins/plugintype_map.json', 'r') as f:
    plugintypes = json.load(f)

url = "https://moodle.example.com"


def get_plugin_type_url(plugintype):
    return plugintypes[plugintype]


def test_plugin(pluginname, plugintype):
    data = requests.get(url + get_plugin_type_url(plugintype) + "/" + pluginname + "/version.php")
    if data.status_code != 200:
        return False
    # changes_map = ["CHANGES.md", "CHANGES.txt", "CHANGES.html", "CHANGES"]
    # for changes in changes_map:
    #    data = requests.get(url + get_plugin_type_url(plugintype) + "/" + pluginname + "/" + changes)
    #    if data.status_code == 200:
    #        print(data.content.decode())

    return True


def main():
    with os.scandir('plugins') as plugintypelists:
        for plugintype in plugintypelists:
            if plugintype.is_dir():
                with os.scandir('plugins/' + plugintype.name) as plugins:
                    for plugin in plugins:
                        if plugin.is_dir():
                            subname = plugin.name[len(plugintype.name) + 1:]
                            if test_plugin(subname, plugintype.name):
                                print(plugin.name)


if __name__ == '__main__':
    main()
