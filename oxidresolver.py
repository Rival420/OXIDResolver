#!/usr/bin/python3

import sys
import argparse
import logging

from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_NONE
from impacket.dcerpc.v5.dcomrt import IObjectExporter


def create_arg_parser():
    """Creates and returns an ArgumentParser object to parse command line arguments."""
    parser = argparse.ArgumentParser(description='IOXIDResolver: A tool to resolve IOXID')
    parser.add_argument('-t', '--target', default='192.168.1.1', help='Target IP address')
    return parser


def get_rpc_transport(target_ip, auth_level=RPC_C_AUTHN_LEVEL_NONE):
    """Creates and returns a DCE/RPC transport object."""
    string_binding = r'ncacn_ip_tcp:{}'.format(target_ip)
    rpc_transport = transport.DCERPCTransportFactory(string_binding)
    portmap = rpc_transport.get_dce_rpc()
    portmap.set_auth_level(auth_level)
    portmap.connect()
    return portmap


def retrieve_network_interface(portmap, target_ip):
    """Retrieves and prints the network interface of the target IP address."""
    obj_exporter = IObjectExporter(portmap)
    bindings = obj_exporter.ServerAlive2()

    logging.info(f"Retrieving network interface of {target_ip}")

    for binding in bindings:
        network_addr = binding['aNetworkAddr']
        logging.info(f"Address: {network_addr}")


def main():
    """Main function to parse arguments and control script flow."""
    parser = create_arg_parser()
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        portmap = get_rpc_transport(args.target)
        retrieve_network_interface(portmap, args.target)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
