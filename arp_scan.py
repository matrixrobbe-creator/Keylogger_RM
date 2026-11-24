from scapy.all import ARP, Ether, srp
import sys

def scan_network(ip_range):
    # Création de la trame Ethernet de diffusion (Broadcast)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    # Paquet ARP demandant "qui a cette IP ?" pour toute la plage
    arp_request = ARP(pdst=ip_range)
    
    # Combinaison des deux couches (L2 / L3)
    packet = broadcast / arp_request

    print(f"Scan en cours sur la plage {ip_range}...\n")
    
    # Envoi du paquet et réception des réponses (srp = Send/Receive Packet au niveau 2)
    answered_list = srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in answered_list:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

if __name__ == "__main__":
    # Plage réseau de ta box (adapte si ton masque est différent de /24)
    network_range = "192.168.1.1/24"
    
    results = scan_network(network_range)

    print("Appareils connectés détectés :")
    print("-" * 45)
    print(f"{'Adresse IP':<20} {'Adresse MAC'}")
    print("-" * 45)
    
    for device in results:
        print(f"{device['ip']:<20} {device['mac']}")