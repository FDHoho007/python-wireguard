import python_wireguard.wireguard as wg
from .key import Key
from .server_connection import ServerConnection

class Client:
    def __init__(self, interface_name, key, local_ip):
        if not wg.valid_interface(interface_name):
            raise ValueError("Invalid interface name {}".format(interface_name))
        if not isinstance(key, Key):
            raise ValueError("Key should be an instance of python_wireguard.Key")

        self.key = key
        self.local_ip = local_ip
        self.interface_name = interface_name
        self.connection = None
        self.interface_created = False
    
    def create_interface(self):
        wg.create_client(self.interface_name, self.key.as_bytes(), self.local_ip)
        self.interface_created = True
    
    def delete_interface(self):
        wg.delete_device(self.interface_name)
        self.interface_created = False
    
    def set_server(self, server_connection):
        '''
        Set the server for this Client.
        '''
        if not isinstance(server_connection, ServerConnection):
            raise ValueError("server_connection should be an instance of python_wireguard.ServerConnection")

    def connect(self):
        if not self.interface_created:
            self.create_interface()
        if self.connection == None:
            raise ValueError("The connection has not been configured for this Client yet. Use 'set_server' to set it.")
        server_connection = self.connection
        key = server_connection.get_key()
        wg.client_add_peer(self.interface_name, key.as_bytes(), server_connection.get_endpoint(), server_connection.get_port())
        wg.enable_device(self.interface_name)