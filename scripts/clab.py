#!/usr/bin/env python3

"""clab

Description ...
"""

import sys
import logging
from pathlib import Path
import yaml

CSV = "docs/topology.csv"
MGMT = "clab/mgmt.yml"
GROUPS = "clab/groups.yml"
NODES = "clab/nodes.yml"
TOPOLOGY = "tmp/dc.clab.yml"
LOG = "tmp/clab.log"

logging.basicConfig(
    filename=LOG,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def read_file(filename):
    """TBC"""

    if Path(filename).is_file():
        with open(filename, mode='r', encoding='utf-8') as file:
            return file.readlines()
    else:
        logging.error("open_file(): filename %s not found", filename)
        sys.exit(1)

def make_links(csv):
    """TBC"""

    links = []
    for line in csv:
        if not ",,,," in line:
            node_a, index_a, node_b, index_b = line.strip().split(",")
            links.append({
                'endpoints': [f"{node_a}:eth{index_a}", f"{node_b}:eth{index_b}"]
            })
    return links

def load_yaml(filename, mandatory):
    """TBC"""

    if Path(filename).is_file():
        with open(filename, mode='r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    elif mandatory:
        logging.error("load_yaml(): filename %s not found", filename)
        sys.exit(1)
    else:
        logging.info("load_yaml(): no data loaded")
        return None

def get_section(name, filename, mandatory=False):
    """TBC"""

    section = {}
    custom_settings = load_yaml(filename, mandatory)
    if not custom_settings:
        logging.info("get_section(): %s section empty", name)
        return section
    section.update({name: custom_settings})
    return section

def main():
    """TBC"""

    clab = {
        'name': "dc",
        'prefix': ""
    }
    mgmt = get_section('mgmt', MGMT)
    clab.update(mgmt)

    clab.update({
        'topology': {
            'defaults': {
                'kind': 'linux',
                'image': 'alpine:latest'
            }
        }
    })

    groups = get_section('groups', GROUPS)
    clab['topology'].update(groups)

    nodes = get_section('nodes', NODES, mandatory=True)
    clab['topology'].update(nodes)

    links = make_links(read_file(CSV))
    clab['topology'].update({'links': links})

    with open(TOPOLOGY, mode='w', encoding='utf-8') as file:
        yaml.safe_dump(clab, file, sort_keys=False)

if __name__ == "__main__":
    main()
