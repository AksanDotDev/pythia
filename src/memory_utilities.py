from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from memory import Config, Host


def get_config(session, key):
    if value := session.query(Config.config_val).filter(
                Config.config_key == key
            ).one_or_none():
        return value.config_val
    else:
        return None


def get_host_ip(session, hostname):
    value = session.query(Host.ip_address).filter(
            Host.hostname == hostname
        ).one_or_none()
    if value and value.ip_address:
        return value.ip_address
    else:
        return None


def get_host_mac(session, hostname):
    value = session.query(Host.mac_address).filter(
            Host.hostname == hostname
        ).one_or_none()
    if value and value.mac_address:
        return value.mac_address
    else:
        return None


def get_host_url(session, hostname):
    value = session.query(Host.url_address).filter(
            Host.hostname == hostname
        ).one_or_none()
    if value and value.url_address:
        return value.url_address
    else:
        return None
