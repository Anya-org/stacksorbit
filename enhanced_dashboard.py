#!/usr/bin/env python3
"""
Enhanced Monitoring Dashboard for StacksOrbit
Real-time monitoring with comprehensive analytics and user-friendly interface
"""

import os
import sys
import json
import time
import curses
import threading
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Import our modules
from deployment_monitor import DeploymentMonitor
from enhanced_conxian_deployment import EnhancedConfigManager

try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
    USE_COLORS = True
except ImportError:
    USE_COLORS = False

class EnhancedDashboard:
    """Enhanced real-time monitoring dashboard"""

    def __init__(self, config: Dict, network: str = 'testnet'):
        self.config = config
        self.network = network
        self.monitor = DeploymentMonitor(network, config)

        # Dashboard state
        self.is_running = False
        self.current_view = 'overview'
        self.update_interval = 2  # seconds

        # Data storage
        self.metrics = {
            'start_time': datetime.now(),
            'api_requests': 0,
            'errors': 0,
            'deployments': 0,
            'transactions': 0
        }

        # Real-time data
        self.current_data = {
            'api_status': {'status': 'checking'},
            'account_info': None,
            'deployed_contracts': [],
            'network_stats': {},
            'recent_transactions': []
        }

    def start_dashboard(self):
        """Start the enhanced monitoring dashboard"""
        print(f"{Fore.CYAN}🚀 Starting Enhanced StacksOrbit Dashboard{Style.RESET_ALL}")
        print(f"🌐 Network: {self.network}")
        print(f"📊 Monitoring address: {self.config.get('SYSTEM_ADDRESS', 'Not configured')}")
        print(f"📝 Press 'q' to quit, 'h' for help\n")

        # Start background monitoring
        self.is_running = True
        monitor_thread = threading.Thread(target=self._background_monitoring, daemon=True)
        monitor_thread.start()

        try:
            self._interactive_dashboard()
        except KeyboardInterrupt:
            self.stop_dashboard()

    def _background_monitoring(self):
        """Background monitoring thread"""
        while self.is_running:
            try:
                self._update_monitoring_data()
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)

    def _update_monitoring_data(self):
        """Update all monitoring data"""
        self.metrics['api_requests'] += 1

        # Update API status
        try:
            self.current_data['api_status'] = self.monitor.check_api_status()
        except Exception as e:
            self.current_data['api_status'] = {'status': 'error', 'error': str(e)}
            self.metrics['errors'] += 1

        # Update account info
        address = self.config.get('SYSTEM_ADDRESS')
        if address:
            try:
                self.current_data['account_info'] = self.monitor.get_account_info(address)
            except Exception as e:
                self.metrics['errors'] += 1

        # Update deployed contracts
        if address:
            try:
                self.current_data['deployed_contracts'] = self.monitor.get_deployed_contracts(address)
            except Exception as e:
                self.metrics['errors'] += 1

        # Update network stats
        try:
            self.current_data['network_stats'] = self._get_network_stats()
        except Exception as e:
            self.metrics['errors'] += 1

    def _get_network_stats(self) -> Dict:
        """Get comprehensive network statistics"""
        api_status = self.current_data['api_status']

        return {
            'block_height': api_status.get('block_height', 0),
            'network_id': api_status.get('network_id', 'unknown'),
            'tps': api_status.get('tps', 0),
            'uptime': self._calculate_uptime(),
            'total_requests': self.metrics['api_requests'],
            'error_rate': self._calculate_error_rate()
        }

    def _calculate_uptime(self) -> str:
        """Calculate dashboard uptime"""
        uptime_seconds = (datetime.now() - self.metrics['start_time']).total_seconds()
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _calculate_error_rate(self) -> float:
        """Calculate error rate percentage"""
        if self.metrics['api_requests'] == 0:
            return 0.0
        return (self.metrics['errors'] / self.metrics['api_requests']) * 100

    def _interactive_dashboard(self):
        """Interactive dashboard interface"""
        while self.is_running:
            self._display_dashboard()

            # Wait for user input
            try:
                import select
                import termios
                import tty

                # Set terminal to raw mode for single key input
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin.fileno())

                # Wait for input with timeout
                if select.select([sys.stdin], [], [], 1)[0]:
                    key = sys.stdin.read(1)
                    self._handle_keypress(key)

            except (ImportError, OSError):
                # Fallback for Windows or when raw input not available
                key = input("\nCommand (h for help, q to quit): ").lower().strip()
                self._handle_keypress(key)

            finally:
                try:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                except:
                    pass

    def _display_dashboard(self):
        """Display the current dashboard"""
        os.system('clear' if os.name == 'posix' else 'cls')

        print(f"{Fore.CYAN}🚀 StacksOrbit - Enhanced Monitoring Dashboard{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Network: {self.network} | Uptime: {self.current_data['network_stats'].get('uptime', '00:00:00')} | Last Update: {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}")
        print("=" * 80)

        if self.current_view == 'overview':
            self._display_overview()
        elif self.current_view == 'contracts':
            self._display_contracts()
        elif self.current_view == 'network':
            self._display_network()
        elif self.current_view == 'transactions':
            self._display_transactions()
        elif self.current_view == 'analytics':
            self._display_analytics()

        print(f"\n{Style.DIM}Commands: [o]verview [c]ontracts [n]etwork [t]ransactions [a]nalytics [h]elp [q]uit{Style.RESET_ALL}")

    def _display_overview(self):
        """Display overview dashboard"""
        print(f"\n{Fore.YELLOW}📊 OVERVIEW{Style.RESET_ALL}")

        # API Status
        api_status = self.current_data['api_status']
        status_color = Fore.GREEN if api_status.get('status') == 'online' else Fore.RED
        print(f"API Status: {status_color}{api_status.get('status', 'unknown').upper()}{Style.RESET_ALL}")

        if api_status.get('status') == 'online':
            print(f"  Block Height: {api_status.get('block_height', 0)}")
            print(f"  Network: {api_status.get('network_id', 'unknown')}")

        # Account Status
        account_info = self.current_data['account_info']
        if account_info:
            balance_microstx = int(account_info.get('balance', 0))
            balance_stx = balance_microstx / 1000000
            nonce = account_info.get('nonce', 0)
            locked_balance = int(account_info.get('locked', 0)) / 1000000

            print(f"\n👤 Account: {Fore.CYAN}{self.config.get('SYSTEM_ADDRESS', 'Unknown')}{Style.RESET_ALL}")
            print(f"  Balance: {Fore.GREEN}{balance_stx:,.6f} STX{Style.RESET_ALL}")

            if locked_balance > 0:
                print(f"  Locked: {Fore.YELLOW}{locked_balance:,.6f} STX{Style.RESET_ALL}")

            available_stx = balance_stx - locked_balance
            print(f"  Available: {Fore.BLUE}{available_stx:,.6f} STX{Style.RESET_ALL}")
            print(f"  Nonce: {nonce}")

            # Deployment cost warnings
            self._show_deployment_cost_warnings(available_stx)

        # Deployment Summary
        deployed_count = len(self.current_data['deployed_contracts'])
        print(f"\n📦 Deployed Contracts: {Fore.BLUE}{deployed_count}{Style.RESET_ALL}")

        # Recent Activity
        print(f"\n🔄 Recent Activity:")
        print(f"  API Requests: {self.metrics['api_requests']}")
        print(f"  Errors: {self.metrics['errors']}")
        print(f"  Error Rate: {self.current_data['network_stats'].get('error_rate', 0):.1f}%")

    def _display_contracts(self):
        """Display contracts dashboard"""
        print(f"\n{Fore.YELLOW}📦 CONTRACTS{Style.RESET_ALL}")

        contracts = self.current_data['deployed_contracts']

        if not contracts:
            print(f"{Fore.YELLOW}No contracts deployed yet{Style.RESET_ALL}")
            return

        print(f"Total deployed contracts: {len(contracts)}\n")

        # Group contracts by category
        categories = self._categorize_contracts(contracts)

        for category, category_contracts in categories.items():
            print(f"{Fore.CYAN}{category.upper()}{Style.RESET_ALL} ({len(category_contracts)}):")
            for contract in category_contracts[:5]:  # Show first 5
                contract_id = contract.get('contract_id', '')
                status = self._check_contract_status(contract_id)
                status_icon = "✅" if status else "⚠️"
                print(f"  {status_icon} {contract_id}")

            if len(category_contracts) > 5:
                print(f"  ... and {len(category_contracts) - 5} more")
            print()

    def _display_network(self):
        """Display network dashboard"""
        print(f"\n{Fore.YELLOW}🌐 NETWORK{Style.RESET_ALL}")

        api_status = self.current_data['api_status']
        network_stats = self.current_data['network_stats']

        print(f"API Status: {Fore.GREEN if api_status.get('status') == 'online' else Fore.RED}{api_status.get('status', 'unknown').upper()}{Style.RESET_ALL}")
        print(f"Network ID: {api_status.get('network_id', 'unknown')}")
        print(f"Block Height: {api_status.get('block_height', 0)}")
        print(f"Burn Height: {api_status.get('burn_block_height', 0)}")
        print(f"Server Version: {api_status.get('server_version', 'unknown')}")

        print(f"\n📊 Performance Metrics:")
        print(f"  TPS: {api_status.get('tps', 0)}")
        print(f"  Uptime: {network_stats.get('uptime', '00:00:00')}")
        print(f"  Total API Requests: {network_stats.get('total_requests', 0)}")
        print(f"  Error Rate: {network_stats.get('error_rate', 0):.1f}%")

        # Network health indicators
        print(f"\n🏥 Health Indicators:")
        error_rate = network_stats.get('error_rate', 0)
        if error_rate < 1:
            health = f"{Fore.GREEN}Excellent{Style.RESET_ALL}"
        elif error_rate < 5:
            health = f"{Fore.YELLOW}Good{Style.RESET_ALL}"
        else:
            health = f"{Fore.RED}Poor{Style.RESET_ALL}"
        print(f"  Overall Health: {health}")

    def _display_transactions(self):
        """Display transactions dashboard"""
        print(f"\n{Fore.YELLOW}🔄 TRANSACTIONS{Style.RESET_ALL}")

        address = self.config.get('SYSTEM_ADDRESS')
        if not address:
            print(f"{Fore.YELLOW}No address configured{Style.RESET_ALL}")
            return

        account_info = self.current_data['account_info']
        if not account_info:
            print(f"{Fore.YELLOW}No account information available{Style.RESET_ALL}")
            return

        print(f"Account: {Fore.CYAN}{address}{Style.RESET_ALL}")
        print(f"Current Nonce: {account_info.get('nonce', 0)}")

        # Get recent transactions
        try:
            api_url = self.monitor.api_url
            response = requests.get(f"{api_url}/v2/accounts/{address}/transactions?limit=10", timeout=10)
            transactions = response.json().get('results', [])

            if transactions:
                print(f"\n📋 Recent Transactions:")
                for i, tx in enumerate(transactions[:5], 1):
                    tx_id = tx.get('tx_id', '')[:16] + '...'
                    tx_type = tx.get('tx_type', 'unknown')
                    tx_status = tx.get('tx_status', 'unknown')

                    status_icon = {
                        'success': '✅',
                        'pending': '⏳',
                        'error': '❌'
                    }.get(tx_status, '❓')

                    print(f"  {i}. {status_icon} {tx_type} - {tx_id}")

                    # Show timestamp
                    try:
                        tx_time = datetime.fromisoformat(tx['burn_block_time'].replace('Z', '+00:00'))
                        time_ago = datetime.now() - tx_time
                        print(f"     {time_ago.seconds // 60} minutes ago")
                    except:
                        pass

            else:
                print(f"{Fore.YELLOW}No recent transactions found{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error fetching transactions: {e}{Style.RESET_ALL}")

    def _display_analytics(self):
        """Display analytics dashboard"""
        print(f"\n{Fore.YELLOW}📈 ANALYTICS{Style.RESET_ALL}")

        # Deployment analytics
        deployed_contracts = self.current_data['deployed_contracts']
        categories = self._categorize_contracts(deployed_contracts)

        print("📦 Deployment Analytics:")
        print(f"  Total Contracts: {len(deployed_contracts)}")

        for category, contracts in categories.items():
            percentage = (len(contracts) / len(deployed_contracts)) * 100 if deployed_contracts else 0
            print(f"  {category.capitalize()}: {len(contracts)} ({percentage:.1f}%)")

        # Performance analytics
        print(f"\n⚡ Performance Analytics:")
        network_stats = self.current_data['network_stats']
        print(f"  API Response Time: {self._get_avg_response_time():.2f}s")
        print(f"  Error Rate: {network_stats.get('error_rate', 0):.1f}%")
        print(f"  Uptime: {network_stats.get('uptime', '00:00:00')}")

        # Activity analytics
        print(f"\n📊 Activity Analytics:")
        print(f"  Total API Requests: {self.metrics['api_requests']}")
        print(f"  Total Errors: {self.metrics['errors']}")
        print(f"  Monitoring Duration: {network_stats.get('uptime', '00:00:00')}")

        # Recommendations
        print(f"\n💡 Recommendations:")
        self._generate_analytics_recommendations()

    def _categorize_contracts(self, contracts: List[Dict]) -> Dict[str, List]:
        """Categorize contracts by type"""
        categories = {
            'core': [],
            'tokens': [],
            'dex': [],
            'dimensional': [],
            'oracle': [],
            'governance': [],
            'security': [],
            'monitoring': [],
            'other': []
        }

        for contract in contracts:
            contract_id = contract.get('contract_id', '')
            contract_name = contract_id.split('.')[-1]

            # Categorize based on contract name patterns
            categorized = False
            for category, patterns in categories.items():
                if category == 'other':
                    continue

                if any(pattern in contract_name.lower() for pattern in self._get_category_patterns(category)):
                    categories[category].append(contract)
                    categorized = True
                    break

            if not categorized:
                categories['other'].append(contract)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def _get_category_patterns(self, category: str) -> List[str]:
        """Get pattern keywords for contract categorization"""
        patterns = {
            'core': ['core', 'engine', 'manager', 'risk', 'liquidation', 'funding'],
            'tokens': ['token', 'cxd', 'cxlp', 'cxvg', 'cxtr', 'cxs'],
            'dex': ['dex', 'factory', 'router', 'pool', 'vault', 'swap'],
            'dimensional': ['dim', 'dimensional', 'position', 'concentrated'],
            'oracle': ['oracle', 'aggregator', 'btc', 'adapter'],
            'governance': ['governance', 'proposal', 'timelock', 'upgrade'],
            'security': ['circuit', 'pausable', 'access', 'rate', 'limiter'],
            'monitoring': ['analytics', 'monitor', 'dashboard', 'metrics']
        }

    def _show_deployment_cost_warnings(self, available_stx: float):
        """Show deployment cost warnings based on available balance"""
        # Estimate deployment costs (rough estimates)
        base_cost_per_contract = 0.5  # STX per contract
        max_contracts = 20  # Estimated max contracts to deploy
        total_estimated_cost = base_cost_per_contract * max_contracts

        print(f"\n💰 Deployment Cost Estimate:")
        print(f"  Estimated: {Fore.YELLOW}{total_estimated_cost:,.2f} STX{Style.RESET_ALL} (for ~20 contracts)")

        if available_stx < 1.0:
            print(f"  {Fore.RED}⚠️  WARNING: Insufficient funds for deployment!{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}💡 Add STX to your wallet before deploying{Style.RESET_ALL}")
        elif available_stx < total_estimated_cost:
            print(f"  {Fore.YELLOW}⚠️  WARNING: Limited funds for full deployment{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}💡 Consider adding more STX or deploying fewer contracts{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}✅ Sufficient funds for deployment{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}💡 Ready to deploy!{Style.RESET_ALL}")

    def _get_avg_response_time(self) -> float:
        """Get average API response time (simulated)"""
        # In a real implementation, this would track actual response times
        return 0.5 + (self.metrics['errors'] * 0.1)  # Simulated slower response with errors

    def _generate_analytics_recommendations(self):
        """Generate analytics-based recommendations"""
        error_rate = self.current_data['network_stats'].get('error_rate', 0)

        if error_rate > 5:
            print(f"  {Fore.RED}• High error rate detected - check network connectivity{Style.RESET_ALL}")
        elif error_rate > 1:
            print(f"  {Fore.YELLOW}• Moderate error rate - monitor network stability{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}• Network performance is excellent{Style.RESET_ALL}")

        # Deployment completeness
        deployed_contracts = self.current_data['deployed_contracts']
        if len(deployed_contracts) < 10:
            print(f"  {Fore.YELLOW}• Few contracts deployed - consider full deployment{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}• Good deployment coverage{Style.RESET_ALL}")

    def _check_contract_status(self, contract_id: str) -> bool:
        """Check if contract is responsive"""
        try:
            api_url = self.monitor.api_url
            response = requests.get(f"{api_url}/v2/contracts/interface/{contract_id}", timeout=5)
            return response.status_code == 200
        except:
            return False

    def _handle_keypress(self, key: str):
        """Handle user keypress"""
        if key == 'q':
            self.stop_dashboard()
        elif key == 'h':
            self._show_help()
        elif key == 'o':
            self.current_view = 'overview'
        elif key == 'c':
            self.current_view = 'contracts'
        elif key == 'n':
            self.current_view = 'network'
        elif key == 't':
            self.current_view = 'transactions'
        elif key == 'a':
            self.current_view = 'analytics'
        elif key == 'r':
            self._refresh_data()
        elif key == 's':
            self._save_snapshot()

    def _show_help(self):
        """Show help information"""
        print(f"\n{Fore.CYAN}📖 Dashboard Help{Style.RESET_ALL}")
        print("=" * 50)
        print("Navigation:")
        print("  o - Overview dashboard")
        print("  c - Contracts dashboard")
        print("  n - Network dashboard")
        print("  t - Transactions dashboard")
        print("  a - Analytics dashboard")
        print()
        print("Actions:")
        print("  r - Refresh data")
        print("  s - Save snapshot")
        print("  h - Show this help")
        print("  q - Quit dashboard")
        print()
        print("Press any key to continue...")
        input()

    def _refresh_data(self):
        """Manually refresh all data"""
        print("🔄 Refreshing data...")
        self._update_monitoring_data()

    def _save_snapshot(self):
        """Save current dashboard state to file"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'network': self.network,
            'current_data': self.current_data,
            'metrics': self.metrics,
            'current_view': self.current_view
        }

        snapshot_path = Path("logs") / f"dashboard_snapshot_{int(time.time())}.json"
        snapshot_path.parent.mkdir(exist_ok=True)

        with open(snapshot_path, 'w') as f:
            json.dump(snapshot, f, indent=2)

        print(f"💾 Dashboard snapshot saved to {snapshot_path}")

    def stop_dashboard(self):
        """Stop the dashboard"""
        print(f"\n{Fore.YELLOW}🛑 Stopping dashboard...{Style.RESET_ALL}")
        self.is_running = False

        # Save final summary
        self._save_monitoring_summary()

    def _save_monitoring_summary(self):
        """Save monitoring summary"""
        summary = {
            'end_time': datetime.now().isoformat(),
            'network': self.network,
            'session_duration': self._calculate_uptime(),
            'total_api_requests': self.metrics['api_requests'],
            'total_errors': self.metrics['errors'],
            'final_error_rate': self._calculate_error_rate(),
            'contracts_monitored': len(self.current_data['deployed_contracts']),
            'address': self.config.get('SYSTEM_ADDRESS', 'unknown')
        }

        summary_path = Path("logs") / "monitoring_session_summary.json"
        summary_path.parent.mkdir(exist_ok=True)

        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"💾 Session summary saved to {summary_path}")

def main():
    """Main dashboard CLI function"""
    parser = argparse.ArgumentParser(description='Enhanced StacksOrbit Monitoring Dashboard')
    parser.add_argument('--config', default='.env', help='Configuration file path')
    parser.add_argument('--network', choices=['devnet', 'testnet', 'mainnet'], default='testnet')
    parser.add_argument('--address', help='Address to monitor')
    parser.add_argument('--update-interval', type=int, default=2, help='Update interval in seconds')
    parser.add_argument('--no-colors', action='store_true', help='Disable colored output')

    args = parser.parse_args()

    try:
        # Load configuration
        config_manager = EnhancedConfigManager(args.config)
        config = config_manager.load_config()

        # Override with command line arguments
        if args.network:
            config['NETWORK'] = args.network
        if args.address:
            config['SYSTEM_ADDRESS'] = args.address

        # Disable colors if requested
        if args.no_colors:
            global USE_COLORS
            USE_COLORS = False

        # Validate configuration
        is_valid, errors = config_manager.validate_config()
        if not is_valid:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"   - {error}")
            return 1

        # Initialize and start dashboard
        dashboard = EnhancedDashboard(config, config.get('NETWORK', 'testnet'))
        dashboard.update_interval = args.update_interval

        dashboard.start_dashboard()
        return 0

    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Dashboard failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
