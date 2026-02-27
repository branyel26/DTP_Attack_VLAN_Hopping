# DTP Attack - VLAN Hopping (Salto de VLAN)

## Descripción

Este proyecto demuestra un ataque de **DTP (Dynamic Trunking Protocol) Attack** para realizar **VLAN Hopping**. El ataque explota la configuración automática de puertos en switches Cisco para forzar la negociación de un enlace Trunk, permitiendo al atacante acceder al tráfico de múltiples VLANs.

## Topología de Red

![Topología GNS3](Topologia_GNS3.png)

## Entorno del Laboratorio

| Dispositivo | Dirección IP | Función |
|-------------|--------------|---------|
| **Ubuntu (Atacante)** | `10.14.89.5` | Estación de Ataque |
| **Kali (Víctima)** | `10.14.89.4` | Objetivo / Víctima |
| **Router** | `10.14.89.1` | Gateway de la red |
| **Switch** | N/A | Nodo de Red - Víctima de DTP (Capa 2) |

- **Segmento de Red:** 10.14.89.0/26 (Rango útil: .1 a .62)
- **Dominio VTP:** `branyel.local`

## ¿Qué es DTP?

**Dynamic Trunking Protocol (DTP)** es un protocolo propietario de Cisco que permite a los switches negociar automáticamente si un enlace debe ser un puerto de acceso o un enlace trunk. Por defecto, muchos puertos de switch están configurados en modo "dynamic desirable" o "dynamic auto".

## Requisitos

- Python 3.x
- Scapy (`pip install scapy`)
- Permisos de superusuario (root)
- Acceso a un puerto de switch con DTP habilitado

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/DTP_Attack_VLAN_Hopping.git
cd DTP_Attack_VLAN_Hopping

# Instalar dependencias
pip install scapy
```

## Uso

```bash
sudo python3 DTP_Attack.py
```

## Cómo Funciona el Ataque

### Paso 1: Identificar la Interfaz de Red
El script utiliza la interfaz `eth0` por defecto. Modifica la variable `iface` según tu configuración.

### Paso 2: Construir Paquete DTP
El script construye un paquete DTP con las siguientes capas:
- **Dot3:** Trama Ethernet 802.3 con destino multicast de Cisco (`01:00:0c:cc:cc:cc`)
- **LLC:** Logical Link Control
- **SNAP:** Subnetwork Access Protocol con código OUI de Cisco
- **Payload DTP:** Datos del protocolo DTP en modo "Desirable"

### Paso 3: Enviar Paquetes DTP
El script envía paquetes DTP continuamente cada 2 segundos para:
1. Forzar al switch a negociar un enlace trunk
2. Mantener el enlace trunk activo (el switch lo desactivaría si no recibe paquetes DTP)

### Paso 4: Negociación de Trunk
El switch recibe los paquetes DTP "Desirable" y negocia el puerto como enlace trunk.

## Verificación del Ataque

En el switch Cisco, verificar que el puerto ahora es trunk:

```
Switch# show interfaces trunk

Port        Mode             Encapsulation  Status        Native vlan
Gi0/1       desirable        802.1q         trunking      1
```

También puedes verificar con:

```
Switch# show interfaces switchport
```

## Estructura del Paquete DTP

```
┌────────────────────────────────────────────┐
│            Dot3 (IEEE 802.3)               │
│  Destino: 01:00:0c:cc:cc:cc (Cisco SNAP)   │
├────────────────────────────────────────────┤
│              LLC (802.2)                   │
│  DSAP: 0xAA  SSAP: 0xAA  Ctrl: 0x03        │
├────────────────────────────────────────────┤
│           SNAP (Subnetwork)                │
│  OUI: 0x00000C (Cisco)  Code: 0x2004 (DTP) │
├────────────────────────────────────────────┤
│            DTP Payload                     │
│  Version: 1                                │
│  Status: Desirable                         │
│  Type, Neighbor, VTP fields                │
└────────────────────────────────────────────┘
```

## Flujo del Ataque

```
┌─────────────┐     Paquetes DTP      ┌─────────────┐
│  Atacante   │ ═══════════════════▶  │   Switch    │
│ 10.14.89.5  │   (Desirable Mode)    │ 10.14.89.1  │
└─────────────┘                       └─────────────┘
                                             │
                      Negociación Trunk      │
                      ◀══════════════════════┘
                                             
┌─────────────┐       Tráfico VLAN    ┌─────────────┐
│  Atacante   │ ◀═════════════════════│   Switch    │
│ 10.14.89.5  │   (Todas las VLANs)   │ 10.14.89.1  │
└─────────────┘                       └─────────────┘
```

## Impacto del Ataque

Una vez que el puerto se convierte en trunk, el atacante puede:

1. **Capturar tráfico de múltiples VLANs**
2. **Inyectar tráfico en VLANs específicas**
3. **Realizar ataques de hombre en el medio entre VLANs**
4. **Escalar a otros ataques** (VTP Attack, ARP Spoofing inter-VLAN)

## Mitigaciones

### 1. Deshabilitar DTP en puertos de acceso
```
Switch(config-if)# switchport mode access
Switch(config-if)# switchport nonegotiate
```

### 2. Configurar puertos no utilizados como shutdown
```
Switch(config-if)# shutdown
```

### 3. Asignar puertos no utilizados a una VLAN "black hole"
```
Switch(config-if)# switchport access vlan 999
```

### 4. Configurar trunk manualmente cuando sea necesario
```
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport nonegotiate
```

## Estructura del Proyecto

```
DTP_Attack_VLAN_Hopping/
├── DTP_Attack.py        # Script principal del ataque
├── Topologia_GNS3.png   # Diagrama de la topología de red
└── README.md            # Esta documentación
```

## Tecnologías Utilizadas

- **Python 3**
- **Scapy** - Manipulación de paquetes de red
- **GNS3** - Simulador de red
- **Cisco IOS** - Sistema operativo del switch

---

## Descargo de Responsabilidad

> **⚠️ AVISO IMPORTANTE**
> 
> Este script fue desarrollado **exclusivamente con fines educativos** como parte del laboratorio de la materia **Seguridad de Redes** en el **Instituto Tecnológico de Las Américas (ITLA)**.
> 
> El uso de estas herramientas en redes sin autorización explícita es **ilegal** y puede conllevar consecuencias legales severas.
> 
> **Estudiante:** Branyel Pérez  
> **Matrícula:** 2024-1489  
> **Docente:** Jonathan Rondón  
> **Institución:** Instituto Tecnológico de Las Américas (ITLA)
