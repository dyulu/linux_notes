#!/usr/bin/python3 -u

#
# Kernel config for a running system:
# /usr/src/linux/.config
# sudo modprobe configs
# zcat /proc/config.gz
# ls /boot/config*
# less /boot/config-$(uname -r)
#

import argparse

""" Kernel config content examples

#
# General setup
#

CONFIG_INIT_ENV_ARG_LIMIT=32
# CONFIG_COMPILE_TEST is not set
CONFIG_LOCALVERSION=""
CONFIG_HAVE_KERNEL_GZIP=y
CONFIG_DEFAULT_HOSTNAME="(none)"

"""
def get_configs(kconfig):
    cfg_items = {}
    with open(kconfig, 'r') as cfg:
        for cfg_item in cfg.readlines():
            cfg_item = cfg_item.strip().replace('=', ' ').split()
            if len(cfg_item) < 2:
                continue

            if 'CONFIG_' in cfg_item[0]:
                cfg_items[cfg_item[0].strip()] = cfg_item[1].strip()
            if 'CONFIG_' in cfg_item[1]:
                cfg_items[cfg_item[1].strip()] = 'NotSet'

        # [print(key, ':', value) for key, value in cfg_items.items()]
        return cfg_items


parser = argparse.ArgumentParser()
parser.add_argument('kconfig1', help='Kernel config file 1')
parser.add_argument('kconfig2', help='Kernel config file 2')
args = parser.parse_args()

cfg1 = get_configs(args.kconfig1)
cfg2 = get_configs(args.kconfig2)

cfg1_keys = set(cfg1.keys())
cfg2_keys = set(cfg2.keys())

print("CONFIG_ in both {} and {} but has different values:\n".format(args.kconfig1, args.kconfig2))
cfg1_cfg2 = cfg1_keys & cfg2_keys
cfg1_cfg2 = sorted(cfg1_cfg2)
for key in  cfg1_cfg2:
    if cfg1[key] != cfg2[key]:
        print("{} {} {}".format(key, cfg1[key], cfg2[key]))

print("\n\nCONFIG_ in {} but not in {}:\n".format(args.kconfig1, args.kconfig2))
cfg1_not_cfg2 = cfg1_keys - cfg2_keys
cfg1_not_cfg2 = sorted(cfg1_not_cfg2)
for key in cfg1_not_cfg2:
    print("{} {}".format(key, cfg1[key]))
    if key in cfg2_keys:
        print("ERROR: {} in {}".format(key, args.kconfig2))

print("\n\nCONFIG_ in {} but not in {}:\n".format(args.kconfig2, args.kconfig1))
cfg2_not_cfg1 = cfg2_keys - cfg1_keys
cfg2_not_cfg1 = sorted(cfg2_not_cfg1)
for key in cfg2_not_cfg1:
    print("{} {}".format(key, cfg2[key]))
    if key in cfg1_keys:
        print("ERROR: {} in {}".format(key, args.kconfig1))
