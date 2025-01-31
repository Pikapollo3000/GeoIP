import requests
import argparse
import webbrowser
from colorama import Fore, Style, init

init(autoreset=True)

def get_ip_info(ip=None):
    url = f"http://ip-api.com/json/{ip or ''}?fields=status,message,continent,country,city,lat,lon,isp,org,as,proxy,hosting,query"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def print_ip_info(data):
    if data.get('status') != 'success':
        print(f"{Fore.RED}Error: {data.get('message', 'Unknown error')}")
        return

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Información de {data['query']} ==={Style.RESET_ALL}")
    
    # Información básica
    print(f"\n{Fore.YELLOW}● Geolocalización{Style.RESET_ALL}")
    print(f"{Fore.GREEN}País: {Fore.WHITE}{data['country']}")
    print(f"{Fore.GREEN}Ciudad: {Fore.WHITE}{data['city']}")
    print(f"{Fore.GREEN}Coordenadas: {Fore.WHITE}{data['lat']}, {data['lon']}")
    
    # Información técnica
    print(f"\n{Fore.YELLOW}● Red{Style.RESET_ALL}")
    print(f"{Fore.GREEN}ISP: {Fore.WHITE}{data['isp']}")
    print(f"{Fore.GREEN}Organización: {Fore.WHITE}{data['org']}")
    print(f"{Fore.GREEN}ASN: {Fore.WHITE}{data['as']}")
    
    # Seguridad
    print(f"\n{Fore.YELLOW}● Detección{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Proxy/VPN: {Fore.WHITE}{'Sí' if data['proxy'] else 'No'}")
    print(f"{Fore.GREEN}Hosting: {Fore.WHITE}{'Sí' if data['hosting'] else 'No'}")

def main():
    parser = argparse.ArgumentParser(description='Geolocalizador de IP con mapa')
    parser.add_argument('-i', '--ip', help='IP a investigar')
    parser.add_argument('-n', '--no-map', action='store_true', help='No abrir el mapa automáticamente')
    args = parser.parse_args()
    
    ip = args.ip or input(f"\n{Fore.BLUE}Ingrese IP (enter para su IP): {Style.RESET_ALL}").strip()
    
    data = get_ip_info(ip or None)
    print_ip_info(data)
    
    if data.get('status') == 'success' and not args.no_map:
        map_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
        print(f"\n{Fore.MAGENTA}Abriendo mapa en Google...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Enlace directo: {Style.RESET_ALL}{map_url}")
        webbrowser.open(map_url)

if __name__ == "__main__":
    main()
