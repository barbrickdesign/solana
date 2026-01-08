#!/usr/bin/env python3
"""
Passive Income Generator for Solana AI System
Implements various strategies to generate passive income for dev vault
"""

import json
import sys
from pathlib import Path
from datetime import datetime

CONFIG_PATH = Path(__file__).parent.parent / "config" / "system-config.json"
DATA_PATH = Path(__file__).parent.parent / "data" / "passive_income_log.json"

def load_config():
    """Load system configuration"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def log_income_transaction(transaction_data):
    """Log passive income transaction to data file"""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing log or create new
    if DATA_PATH.exists():
        with open(DATA_PATH, 'r') as f:
            log = json.load(f)
    else:
        log = {"transactions": [], "total_income": 0}
    
    # Add new transaction
    transaction_data['timestamp'] = datetime.now().isoformat()
    log['transactions'].append(transaction_data)
    log['total_income'] += transaction_data.get('amount', 0)
    
    # Save log
    with open(DATA_PATH, 'w') as f:
        json.dump(log, f, indent=2)
    
    return log

def stake_for_rewards(wallet, amount, validator, private_key, network='devnet'):
    """
    Stake SOL to generate passive rewards
    All rewards automatically go to dev vault
    
    Args:
        wallet: Source wallet public key
        amount: Amount to stake
        validator: Validator public key
        private_key: Private key for signing
        network: Network to use
    
    Returns:
        dict: Staking result
    """
    config = load_config()
    dev_vault = config['devVaultWallet']
    
    result = {
        "status": "success",
        "operation": "stake_for_rewards",
        "strategy": "staking",
        "wallet": wallet,
        "amount": amount,
        "validator": validator,
        "dev_vault": dev_vault,
        "network": network,
        "expected_apy": "5-10%",
        "signature": "SIMULATED_STAKE_" + str(hash(wallet + str(amount))),
        "instructions": [
            f"1. Create stake account for {amount} SOL",
            f"2. Delegate stake to validator: {validator}",
            f"3. Configure rewards withdrawal to dev vault: {dev_vault}",
            "4. Stake will generate ongoing passive income",
            "5. All rewards automatically sent to dev vault"
        ],
        "cli_commands": [
            f"solana create-stake-account <stake_keypair> {amount}",
            f"solana delegate-stake <stake_account> {validator}",
            f"solana withdraw-stake <stake_account> {dev_vault} <amount>"
        ]
    }
    
    # Log the transaction
    log_income_transaction({
        "type": "staking",
        "amount": amount,
        "wallet": wallet,
        "dev_vault": dev_vault,
        "status": "initiated"
    })
    
    return result

def create_token_account_for_fees(wallet, token_mint, private_key, network='devnet'):
    """
    Create token account to collect SPL token fees
    
    Args:
        wallet: Wallet public key
        token_mint: Token mint address
        private_key: Private key for signing
        network: Network to use
    
    Returns:
        dict: Token account creation result
    """
    config = load_config()
    dev_vault = config['devVaultWallet']
    
    result = {
        "status": "success",
        "operation": "create_token_account",
        "strategy": "token_fees",
        "wallet": wallet,
        "token_mint": token_mint,
        "dev_vault": dev_vault,
        "network": network,
        "signature": "SIMULATED_TOKEN_ACCOUNT_" + str(hash(wallet + token_mint)),
        "instructions": [
            f"1. Create associated token account for mint: {token_mint}",
            f"2. Configure account owner as dev vault: {dev_vault}",
            "3. Account will receive token fees and transfers",
            "4. All tokens automatically owned by dev vault"
        ],
        "cli_commands": [
            f"spl-token create-account {token_mint}",
            f"spl-token authorize <token_account> owner {dev_vault}"
        ]
    }
    
    return result

def get_income_report():
    """Get passive income report"""
    if not DATA_PATH.exists():
        return {
            "total_income": 0,
            "transaction_count": 0,
            "transactions": []
        }
    
    with open(DATA_PATH, 'r') as f:
        log = json.load(f)
    
    return {
        "total_income": log['total_income'],
        "transaction_count": len(log['transactions']),
        "recent_transactions": log['transactions'][-10:],  # Last 10
        "strategies": {
            "staking": sum(1 for t in log['transactions'] if t.get('type') == 'staking'),
            "token_fees": sum(1 for t in log['transactions'] if t.get('type') == 'token_fees'),
            "other": sum(1 for t in log['transactions'] if t.get('type') not in ['staking', 'token_fees'])
        }
    }

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python passive_income_generator.py <operation> [args...]")
        print("Operations:")
        print("  stake <wallet> <amount> <validator> <private_key> [network]")
        print("  create-token-account <wallet> <token_mint> <private_key> [network]")
        print("  report")
        sys.exit(1)
    
    operation = sys.argv[1]
    
    if operation == "stake":
        if len(sys.argv) < 6:
            print("Usage: stake <wallet> <amount> <validator> <private_key> [network]")
            sys.exit(1)
        
        wallet = sys.argv[2]
        amount = float(sys.argv[3])
        validator = sys.argv[4]
        private_key = sys.argv[5]
        network = sys.argv[6] if len(sys.argv) > 6 else 'devnet'
        
        result = stake_for_rewards(wallet, amount, validator, private_key, network)
        print(json.dumps(result, indent=2))
    
    elif operation == "create-token-account":
        if len(sys.argv) < 5:
            print("Usage: create-token-account <wallet> <token_mint> <private_key> [network]")
            sys.exit(1)
        
        wallet = sys.argv[2]
        token_mint = sys.argv[3]
        private_key = sys.argv[4]
        network = sys.argv[5] if len(sys.argv) > 5 else 'devnet'
        
        result = create_token_account_for_fees(wallet, token_mint, private_key, network)
        print(json.dumps(result, indent=2))
    
    elif operation == "report":
        report = get_income_report()
        print(json.dumps(report, indent=2))
    
    else:
        print(f"Unknown operation: {operation}")
        sys.exit(1)

if __name__ == "__main__":
    main()
