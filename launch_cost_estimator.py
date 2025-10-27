#!/usr/bin/env python3
"""
Conxian Self-Launch Cost Estimation and Planning Tool
Analyzes the complete system and provides detailed launch cost breakdowns
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ContractInfo:
    name: str
    path: str
    category: str
    dependencies: List[str]
    estimated_gas: int
    complexity: str
    launch_phase: str

@dataclass
class LaunchPhase:
    name: str
    min_funding: int
    max_funding: int
    contracts: List[str]
    total_gas: int
    description: str

class LaunchCostEstimator:
    """Comprehensive cost estimation for Conxian self-launch"""

    def __init__(self):
        self.contracts = self._load_contract_database()
        self.launch_phases = self._define_launch_phases()
        self.gas_price = 1000000  # 1 STX per deployment (conservative)

    def _load_contract_database(self) -> Dict[str, ContractInfo]:
        """Load comprehensive contract database"""
        return {
            # Core System Contracts
            'all-traits': ContractInfo(
                name='all-traits',
                path='contracts/traits/all-traits.clar',
                category='core',
                dependencies=[],
                estimated_gas=2000000,
                complexity='high',
                launch_phase='bootstrap'
            ),
            'utils-encoding': ContractInfo(
                name='utils-encoding',
                path='contracts/utils/encoding.clar',
                category='core',
                dependencies=['all-traits'],
                estimated_gas=1500000,
                complexity='medium',
                launch_phase='bootstrap'
            ),
            'utils-utils': ContractInfo(
                name='utils-utils',
                path='contracts/utils/utils.clar',
                category='core',
                dependencies=['all-traits'],
                estimated_gas=1500000,
                complexity='medium',
                launch_phase='bootstrap'
            ),

            # Token System
            'cxd-token': ContractInfo(
                name='cxd-token',
                path='contracts/tokens/cxd-token.clar',
                category='tokens',
                dependencies=['all-traits', 'utils-encoding'],
                estimated_gas=3000000,
                complexity='high',
                launch_phase='core'
            ),
            'token-emission-controller': ContractInfo(
                name='token-emission-controller',
                path='contracts/dex/token-emission-controller.clar',
                category='tokens',
                dependencies=['all-traits', 'cxd-token'],
                estimated_gas=2500000,
                complexity='high',
                launch_phase='core'
            ),

            # DEX System
            'dex-factory': ContractInfo(
                name='dex-factory',
                path='contracts/dex/dex-factory.clar',
                category='dex',
                dependencies=['all-traits', 'utils-encoding'],
                estimated_gas=4000000,
                complexity='high',
                launch_phase='core'
            ),
            'dex-router': ContractInfo(
                name='dex-router',
                path='contracts/dex/dex-router.clar',
                category='dex',
                dependencies=['dex-factory', 'cxd-token'],
                estimated_gas=5000000,
                complexity='high',
                launch_phase='liquidity'
            ),

            # Oracle System
            'oracle': ContractInfo(
                name='oracle',
                path='contracts/oracle.clar',
                category='oracle',
                dependencies=['all-traits'],
                estimated_gas=2500000,
                complexity='high',
                launch_phase='core'
            ),
            'oracle-aggregator': ContractInfo(
                name='oracle-aggregator',
                path='contracts/oracle/oracle-aggregator.clar',
                category='oracle',
                dependencies=['oracle'],
                estimated_gas=3000000,
                complexity='high',
                launch_phase='liquidity'
            ),

            # Governance System
            'governance-token': ContractInfo(
                name='governance-token',
                path='contracts/governance-token.clar',
                category='governance',
                dependencies=['all-traits'],
                estimated_gas=2000000,
                complexity='medium',
                launch_phase='governance'
            ),
            'proposal-engine': ContractInfo(
                name='proposal-engine',
                path='contracts/proposal-engine.clar',
                category='governance',
                dependencies=['governance-token'],
                estimated_gas=3000000,
                complexity='high',
                launch_phase='governance'
            ),

            # Autonomous Systems
            'self-launch-coordinator': ContractInfo(
                name='self-launch-coordinator',
                path='contracts/self-launch-coordinator.clar',
                category='autonomous',
                dependencies=['all-traits', 'token-emission-controller'],
                estimated_gas=2000000,
                complexity='high',
                launch_phase='autonomous'
            ),
            'predictive-scaling-system': ContractInfo(
                name='predictive-scaling-system',
                path='contracts/dex/predictive-scaling-system.clar',
                category='autonomous',
                dependencies=['all-traits'],
                estimated_gas=2500000,
                complexity='high',
                launch_phase='autonomous'
            ),
            'automation-keeper-coordinator': ContractInfo(
                name='automation-keeper-coordinator',
                path='contracts/automation/keeper-coordinator.clar',
                category='autonomous',
                dependencies=['all-traits'],
                estimated_gas=2000000,
                complexity='medium',
                launch_phase='autonomous'
            )
        }

    def _define_launch_phases(self) -> Dict[str, LaunchPhase]:
        """Define community-accessible launch phases with micro-contribution support"""
        return {
            'bootstrap': LaunchPhase(
                name='Community Bootstrap',
                min_funding=100000000,  # 100 STX
                max_funding=500000000,  # 500 STX
                contracts=['all-traits', 'utils-encoding', 'utils-utils'],
                total_gas=2000000,
                description='Essential infrastructure - deployable by community'
            ),
            'micro_core': LaunchPhase(
                name='Micro Core',
                min_funding=500000000,  # 500 STX
                max_funding=1000000000,  # 1K STX
                contracts=['cxd-price-initializer', 'token-system-coordinator'],
                total_gas=3000000,
                description='Core utilities and price management'
            ),
            'token_system': LaunchPhase(
                name='Token System',
                min_funding=1000000000,  # 1K STX
                max_funding=2500000000,  # 2.5K STX
                contracts=['cxd-token', 'token-emission-controller'],
                total_gas=5000000,
                description='Basic token functionality and emission control'
            ),
            'dex_core': LaunchPhase(
                name='DEX Core',
                min_funding=2500000000,  # 2.5K STX
                max_funding=5000000000,  # 5K STX
                contracts=['oracle', 'dex-factory', 'budget-manager'],
                total_gas=10000000,
                description='DEX infrastructure and basic trading'
            ),
            'liquidity': LaunchPhase(
                name='Liquidity & Trading',
                min_funding=5000000000,  # 5K STX
                max_funding=10000000000,  # 10K STX
                contracts=['dex-router', 'dex-pool', 'oracle-aggregator'],
                total_gas=15000000,
                description='Advanced trading and liquidity provision'
            ),
            'governance': LaunchPhase(
                name='Governance',
                min_funding=10000000000,  # 10K STX
                max_funding=25000000000,  # 25K STX
                contracts=['governance-token', 'proposal-engine', 'timelock-controller'],
                total_gas=8000000,
                description='Community governance and decision making'
            ),
            'autonomous': LaunchPhase(
                name='Fully Autonomous',
                min_funding=25000000000,  # 25K STX
                max_funding=50000000000,  # 50K STX
                contracts=['self-launch-coordinator', 'predictive-scaling-system', 'automation-keeper-coordinator'],
                total_gas=5000000,
                description='Self-sustaining autonomous operation'
            )
        }

    def estimate_total_launch_cost(self) -> Dict:
        """Estimate total cost for complete system launch"""
        total_cost = 0
        total_gas = 0

        for phase in self.launch_phases.values():
            total_cost += phase.max_funding
            total_gas += phase.total_gas

        return {
            'total_funding_required': total_cost,
            'total_gas_cost': total_gas,
            'estimated_stx_cost': total_cost / 1000000,
            'total_contracts': len(self.contracts),
            'phases': len(self.launch_phases),
            'bootstrap_cost': self.launch_phases['bootstrap'].min_funding / 1000000,
            'full_system_cost': total_cost / 1000000
        }

    def estimate_phase_cost(self, phase: str) -> Dict:
        """Estimate cost for specific launch phase"""
        if phase not in self.launch_phases:
            return {'error': 'Phase not found'}

        phase_info = self.launch_phases[phase]
        contract_costs = []

        for contract_name in phase_info.contracts:
            if contract_name in self.contracts:
                contract = self.contracts[contract_name]
                contract_costs.append({
                    'name': contract.name,
                    'gas_cost': contract.estimated_gas,
                    'stx_cost': contract.estimated_gas / 1000000,
                    'complexity': contract.complexity
                })

        return {
            'phase': phase_info.name,
            'min_funding': phase_info.min_funding / 1000000,
            'max_funding': phase_info.max_funding / 1000000,
            'total_gas': phase_info.total_gas,
            'contract_count': len(contract_costs),
            'contracts': contract_costs,
            'description': phase_info.description
        }

    def generate_launch_roadmap(self) -> Dict:
        """Generate comprehensive launch roadmap"""
        roadmap = {
            'total_system_cost': self.estimate_total_launch_cost(),
            'phases': {},
            'cost_breakdown': {},
            'milestones': [],
            'risk_assessment': {}
        }

        # Phase details
        for phase_name, phase in self.launch_phases.items():
            roadmap['phases'][phase_name] = self.estimate_phase_cost(phase_name)

        # Cost breakdown by category
        categories = {}
        for contract in self.contracts.values():
            if contract.category not in categories:
                categories[contract.category] = []
            categories[contract.category].append({
                'name': contract.name,
                'gas': contract.estimated_gas,
                'stx': contract.estimated_gas / 1000000
            })

        roadmap['cost_breakdown'] = categories

        # Milestones
        roadmap['milestones'] = [
            {'phase': 'bootstrap', 'funding': '100 STX', 'contracts': 3, 'description': 'Core infrastructure'},
            {'phase': 'micro_core', 'funding': '500 STX', 'contracts': 2, 'description': 'Price management'},
            {'phase': 'token_system', 'funding': '1K STX', 'contracts': 2, 'description': 'Token functionality'},
            {'phase': 'dex_core', 'funding': '2.5K STX', 'contracts': 3, 'description': 'DEX infrastructure'},
            {'phase': 'liquidity', 'funding': '5K STX', 'contracts': 3, 'description': 'Trading enabled'},
            {'phase': 'governance', 'funding': '10K STX', 'contracts': 3, 'description': 'Community governance'},
            {'phase': 'autonomous', 'funding': '25K+ STX', 'contracts': 3, 'description': 'Self-sustaining'}
        ]

        # Risk assessment
        roadmap['risk_assessment'] = {
            'technical_risk': 'medium',
            'funding_risk': 'high',
            'adoption_risk': 'medium',
            'regulatory_risk': 'low',
            'total_contracts': len(self.contracts),
            'complexity_score': self._calculate_complexity_score()
        }

        return roadmap

    def _calculate_complexity_score(self) -> int:
        """Calculate overall system complexity score"""
        total_complexity = 0
        complexity_weights = {'high': 3, 'medium': 2, 'low': 1}

        for contract in self.contracts.values():
            total_complexity += complexity_weights.get(contract.complexity, 1)

        return total_complexity

def main():
    """Main CLI function for launch cost estimation"""
    parser = argparse.ArgumentParser(description='Conxian Self-Launch Cost Estimation Tool')
    parser.add_argument('--phase', choices=['bootstrap', 'micro_core', 'token_system', 'dex_core', 'liquidity', 'governance', 'autonomous', 'all'])
    parser.add_argument('--output-format', choices=['json', 'text'], default='text')
    parser.add_argument('--detailed', action='store_true', help='Show detailed contract breakdown')
    parser.add_argument('--roadmap', action='store_true', help='Generate full launch roadmap')

    args = parser.parse_args()

    try:
        estimator = LaunchCostEstimator()

        if args.roadmap:
            roadmap = estimator.generate_launch_roadmap()
            if args.output_format == 'json':
                print(json.dumps(roadmap, indent=2))
            else:
                print_launch_roadmap(roadmap)
        elif args.phase:
            if args.phase == 'all':
                total_cost = estimator.estimate_total_launch_cost()
                if args.output_format == 'json':
                    print(json.dumps(total_cost, indent=2))
                else:
                    print_total_cost_summary(total_cost)
            else:
                phase_cost = estimator.estimate_phase_cost(args.phase)
                if args.output_format == 'json':
                    print(json.dumps(phase_cost, indent=2))
                else:
                    print_phase_cost_summary(phase_cost, args.detailed)
        else:
            # Default: show total cost summary
            total_cost = estimator.estimate_total_launch_cost()
            print_total_cost_summary(total_cost)

    except Exception as e:
        print(f"[ERROR] Cost estimation failed: {e}")
        return 1

    return 0

def print_total_cost_summary(cost_data: Dict):
    """Print total launch cost summary"""
    print(f"\n{'='*60}")
    print(f"CONXIAN SELF-LAUNCH TOTAL COST ESTIMATION")
    print(f"{'='*60}")
    print(f"Total Funding Required: {cost_data['estimated_stx_cost']:.0f} STX")
    print(f"Total Gas Cost: {cost_data['total_gas_cost']:,} STX")
    print(f"Launch Phases: {cost_data['phases']}")
    print(f"Bootstrap Cost: {cost_data['bootstrap_cost']:.0f} STX")
    print(f"Full System Cost: {cost_data['full_system_cost']:.0f} STX")
    print(f"{'='*60}")

def print_phase_cost_summary(phase_data: Dict, detailed: bool):
    """Print phase cost summary"""
    if 'error' in phase_data:
        print(f"[ERROR] {phase_data['error']}")
        return

    print(f"\n{'='*60}")
    print(f"LAUNCH PHASE: {phase_data['phase'].upper()}")
    print(f"{'='*60}")
    print(f"Funding Range: {phase_data['min_funding']:.0f} - {phase_data['max_funding']:.0f} STX")
    print(f"Total Gas Cost: {phase_data['total_gas']:,} STX")
    print(f"Contracts: {phase_data['contract_count']}")
    print(f"Description: {phase_data['description']}")
    print(f"{'='*60}")

    if detailed and 'contracts' in phase_data:
        print(f"\nDETAILED CONTRACT BREAKDOWN:")
        print(f"{'Contract':<30} {'Gas Cost':<12} {'STX Cost':<10} {'Complexity':<10}")
        print(f"{'-'*70}")
        for contract in phase_data['contracts']:
            stx_formatted = f"{contract['stx']:.2f}"
            print(f"{contract['name']:<30} {contract['gas_cost']:<12} {stx_formatted:<10} {contract['complexity']:<10}")

def print_launch_roadmap(roadmap: Dict):
    """Print comprehensive launch roadmap"""
    print(f"\n{'='*80}")
    print(f"CONXIAN SELF-LAUNCH COMPREHENSIVE ROADMAP")
    print(f"{'='*80}")

    # Total costs
    total = roadmap['total_system_cost']
    print(f"TOTAL SYSTEM COST: {total['estimated_stx_cost']:.0f} STX")
    print(f"BOOTSTRAP COST: {total['bootstrap_cost']:.0f} STX")
    print(f"TOTAL GAS COST: {total['total_gas_cost']:,} STX")
    print(f"CONTRACT COUNT: {total['total_contracts']}")
    print(f"{'='*80}")

    # Milestones
    print(f"\nLAUNCH MILESTONES:")
    print(f"{'Phase':<15} {'Funding':<12} {'Contracts':<10} {'Description':<30}")
    print(f"{'-'*70}")
    for milestone in roadmap['milestones']:
        print(f"{milestone['phase']:<15} {milestone['funding']:<12} {milestone['contracts']:<10} {milestone['description']:<30}")

    # Risk assessment
    risk = roadmap['risk_assessment']
    print(f"\nRISK ASSESSMENT:")
    print(f"Technical Risk: {risk['technical_risk'].upper()}")
    print(f"Funding Risk: {risk['funding_risk'].upper()}")
    print(f"Adoption Risk: {risk['adoption_risk'].upper()}")
    print(f"Regulatory Risk: {risk['regulatory_risk'].upper()}")
    print(f"Complexity Score: {risk['complexity_score']}/10")

    print(f"\n{'='*80}")

if __name__ == "__main__":
    exit(main())
