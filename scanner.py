import socket
import sys
from colorama import Fore, Style
import threading
from datetime import datetime

class PortScanner:
    def __init__(self, host, start_port=1, end_port=65535):
        self.host = host
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.common_ports = {
            20: 'FTP-DATA',
            21: 'FTP',
            22: 'SSH',
            23: 'TELNET',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            27017: 'MongoDB',
            3389: 'RDP',
            8080: 'HTTP-ALT'
        }

    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.host, port))
            
            if result == 0:
                service = self.common_ports.get(port, 'Unknown')
                self.open_ports.append((port, service))
                print(f"{Fore.GREEN}[+] Port {port} is OPEN - Service: {service}{Style.RESET_ALL}")
            
            sock.close()
        except socket.gaierror:
            print(f"{Fore.RED}[!] Hostname {self.host} could not be resolved{Style.RESET_ALL}")
            sys.exit()
        except socket.error:
            print(f"{Fore.RED}[!] Could not connect to {self.host}{Style.RESET_ALL}")
            sys.exit()

    def scan_range(self, ports_to_scan=None):
        """Scan a range of ports"""
        if ports_to_scan is None:
            ports_to_scan = range(self.start_port, self.end_port + 1)
        
        print(f"\n{Fore.CYAN}[*] Scanning target: {self.host}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")
        
        # Use threading for faster scanning
        threads = []
        for port in ports_to_scan:
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print(f"\n{Fore.CYAN}[*] Time finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        self.display_results()

    def scan_common_ports(self):
        """Scan only common ports (faster)"""
        print(f"\n{Fore.CYAN}[*] Scanning common ports on {self.host}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")
        
        threads = []
        for port in self.common_ports.keys():
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(f"\n{Fore.CYAN}[*] Time finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        self.display_results()

    def display_results(self):
        """Display scanning results"""
        if self.open_ports:
            print(f"\n{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}OPEN PORTS FOUND:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
            for port, service in sorted(self.open_ports):
                print(f"{Fore.GREEN}Port {port:5d} - {service}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[✓] Total open ports: {len(self.open_ports)}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[!] No open ports found{Style.RESET_ALL}")


def main():
    if len(sys.argv) < 2:
        print(f"{Fore.CYAN}Usage: python scanner.py <target_ip> [options]{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Options:{Style.RESET_ALL}")
        print(f"  --common    : Scan only common ports (faster)")
        print(f"  --range <start> <end> : Scan specific range")
        print(f"\nExamples:")
        print(f"  python scanner.py 127.0.0.1")
        print(f"  python scanner.py 192.168.1.1 --common")
        print(f"  python scanner.py 10.0.0.5 --range 1 1000")
        sys.exit()

    target = sys.argv[1]
    
    if '--common' in sys.argv:
        scanner = PortScanner(target)
        scanner.scan_common_ports()
    elif '--range' in sys.argv:
        idx = sys.argv.index('--range')
        start = int(sys.argv[idx + 1])
        end = int(sys.argv[idx + 2])
        scanner = PortScanner(target, start, end)
        scanner.scan_range(range(start, end + 1))
    else:
        scanner = PortScanner(target)
        scanner.scan_range()


if __name__ == "__main__":
    main()