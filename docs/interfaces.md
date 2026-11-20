# Interfaces

## Physical interfaces

The variable `ethernet_default_settings` is a merge of the following list of dicts:
- `hardware.ethernet_ports`: defines `index` and `type`
- `platform_ethernets`: defines `name`, `mtu`, `speed` and `description` and it has `index` to reference to `hardware.ethernet_ports`

The merge is done by the filter `community.general.lists_mergeby` using `index` as the key to match two dicts, one from each list.

The filter parameter `list_merged=append_rp` makes the filter keeping `index` property only from `hardware.ethernet_ports` to avoid duplicates.

Once merging is done, the data need to be normalized. That is, non-default settings are combined with default settings.

The merge is, again, done by the filter `community.general.lists_mergeby` but this time using `name` as the key to match two dicts,
one from the list `ethernets` and one from the list `ethernet_default_settings`.
The variable `normalized_ethernets` is used to save the results.

The filter parameter `list_merged=append_rp` makes the filter keeping `name` property only from `ethernets` to avoid duplicates.

# Logical interfaces


