import socket
class DNSChecker:
    def __init__(self, dnsName):
         self.dnsName = dnsName

    def dnslookUp(self):
        try:
            ip_address = socket.gethostbyname(self.dnsName)
            return f"The {self.dnsName} has record {ip_address}."
        except Exception as error:
            return str(error)