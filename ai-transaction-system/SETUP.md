# Installation and Setup Guide

## Quick Setup

### 1. Clone or Access Repository
```bash
git clone https://github.com/barbrickdesign/solana.git
cd solana/ai-transaction-system
```

### 2. Make Scripts Executable (Unix/Linux/Mac)
```bash
chmod +x scripts/*.py
```

### 3. Test the System
```bash
# Test balance query
python3 scripts/ai_prompt_handler.py "What is the balance of 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr?"

# Test income report
python3 scripts/passive_income_generator.py report
```

## Python Requirements

**Current Version (Simulation Mode)**:
- Python 3.7 or higher
- No external dependencies (uses standard library only)

**Production Version (Full Blockchain Integration)**:
```bash
pip install -r requirements.txt
```

## Configuration

### 1. System Configuration
Edit `config/system-config.json`:

```json
{
  "devVaultWallet": "5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr",
  "network": {
    "default": "devnet"  // Change to "mainnet" for production
  }
}
```

### 2. Security Settings
Adjust limits in `config/system-config.json`:
```json
{
  "security": {
    "maxTransactionAmount": 1000,  // Adjust as needed
    "allowedOperations": [
      "transfer",
      "token_transfer",
      "stake",
      "query_balance"
    ]
  }
}
```

## Testing

### 1. Test AI Prompt Handler
```bash
# Balance query
python3 scripts/ai_prompt_handler.py "Check balance of 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr"

# Transfer (simulation)
python3 scripts/ai_prompt_handler.py "Transfer 0.5 SOL from ABC to XYZ"

# Staking
python3 scripts/ai_prompt_handler.py "Stake 10 SOL to generate passive income"

# Income report
python3 scripts/ai_prompt_handler.py "Show passive income report"
```

### 2. Test Transaction Handler
```bash
# Balance query
python3 scripts/transaction_handler.py balance 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr devnet

# Transfer
python3 scripts/transaction_handler.py transfer FROM_WALLET TO_WALLET 1.0 PRIVATE_KEY devnet
```

### 3. Test Passive Income Generator
```bash
# Income report
python3 scripts/passive_income_generator.py report

# Stake operation
python3 scripts/passive_income_generator.py stake WALLET 10.0 VALIDATOR PRIVATE_KEY devnet
```

## AI Integration

### Option 1: Direct Script Execution
AI can execute scripts directly via command line:
```python
import subprocess
import json

result = subprocess.run([
    'python3', 
    'scripts/ai_prompt_handler.py',
    'Transfer 0.5 SOL from A to B'
], capture_output=True, text=True)

response = json.loads(result.stdout)
```

### Option 2: REST API
Create a web service wrapper:
```python
from flask import Flask, request, jsonify
import sys
sys.path.append('scripts')
from ai_prompt_handler import process_ai_request

app = Flask(__name__)

@app.route('/api/transaction', methods=['POST'])
def handle_transaction():
    prompt = request.json.get('prompt')
    credentials = request.json.get('credentials', {})
    result = process_ai_request(prompt, credentials)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Option 3: GitHub Actions
Set up workflow for AI-triggered transactions:
```yaml
name: AI Transaction
on:
  workflow_dispatch:
    inputs:
      prompt:
        description: 'AI Transaction Prompt'
        required: true

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Execute Transaction
        run: |
          cd ai-transaction-system
          python3 scripts/ai_prompt_handler.py "${{ github.event.inputs.prompt }}"
```

## Production Deployment

### 1. Install Solana Dependencies
```bash
pip install solana base58
```

### 2. Update Scripts for Real Blockchain
In `scripts/transaction_handler.py`, replace simulation code with:
```python
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

def transfer_sol_real(from_wallet, to_wallet, amount, private_key, network):
    # Connect to Solana network
    client = Client(NETWORK_URLS[network])
    
    # Create keypair from private key
    sender = Keypair.from_secret_key(base58.b58decode(private_key))
    
    # Create transfer transaction
    transfer_tx = Transaction().add(
        transfer(
            TransferParams(
                from_pubkey=sender.public_key,
                to_pubkey=to_wallet,
                lamports=int(amount * 1e9)  # Convert SOL to lamports
            )
        )
    )
    
    # Send transaction
    result = client.send_transaction(transfer_tx, sender)
    return result
```

### 3. Set Up Monitoring
Monitor passive income:
```bash
# Set up cron job for regular reporting
0 */6 * * * cd /path/to/ai-transaction-system && python3 scripts/passive_income_generator.py report >> logs/income.log
```

### 4. Security Hardening
- Store private keys in secure vault (not in code)
- Use environment variables for sensitive data
- Enable rate limiting
- Add transaction confirmation checks
- Implement multi-sig for large amounts

## Troubleshooting

### Issue: Import Error
**Error**: `ModuleNotFoundError: No module named 'transaction_handler'`

**Solution**: Run scripts from the correct directory or update Python path:
```bash
cd ai-transaction-system/scripts
python3 ai_prompt_handler.py "your prompt"
```

### Issue: Permission Denied
**Error**: `Permission denied: './ai_prompt_handler.py'`

**Solution**: Make script executable:
```bash
chmod +x scripts/*.py
```

### Issue: Invalid JSON
**Error**: `json.decoder.JSONDecodeError`

**Solution**: Ensure config files are valid JSON. Validate at jsonlint.com

### Issue: Network Timeout
**Error**: Connection timeout to Solana network

**Solution**: Check network connectivity and RPC endpoint:
```bash
# Test connection
curl https://api.devnet.solana.com -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}'
```

## Updating Configuration

### Change Network
To switch from devnet to mainnet:
1. Edit `config/system-config.json`
2. Change `"default": "devnet"` to `"default": "mainnet"`
3. Test thoroughly on devnet first!

### Adjust Transaction Limits
Edit security settings:
```json
{
  "security": {
    "maxTransactionAmount": 1000,  // Maximum SOL per transaction
    "requireConfirmation": true     // Require explicit confirmation
  }
}
```

### Add New Operations
To add new transaction types:
1. Add to `allowedOperations` in config
2. Implement handler in `transaction_handler.py`
3. Add prompt patterns in `ai_prompt_handler.py`
4. Update `ai-prompts.json` with examples

## Data Management

### Backup Transaction Logs
```bash
# Backup passive income log
cp data/passive_income_log.json backups/passive_income_log_$(date +%Y%m%d).json
```

### Clear Old Logs
```bash
# Archive old transactions (keep last 1000)
python3 -c "
import json
with open('data/passive_income_log.json', 'r') as f:
    data = json.load(f)
data['transactions'] = data['transactions'][-1000:]
with open('data/passive_income_log.json', 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Support

For issues or questions:
1. Check [docs/README.md](docs/README.md) for detailed documentation
2. Review [examples/sample_prompts.json](examples/sample_prompts.json) for usage examples
3. Examine logs in `data/passive_income_log.json`

---

**Dev Vault**: 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr
