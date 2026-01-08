# Security and Safety Guidelines

## Overview

This document outlines security best practices for the AI Transaction System. All transactions route proceeds to the dev vault: **5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr**

## Critical Security Rules

### 1. Private Key Management

**NEVER**:
- Log private keys to console, files, or databases
- Store private keys in code or configuration files
- Transmit private keys over unencrypted connections
- Share private keys in chat or communication platforms
- Commit private keys to version control

**ALWAYS**:
- Use environment variables for private keys
- Encrypt private keys at rest
- Use secure key management services (AWS KMS, HashiCorp Vault)
- Prompt users to enter keys securely
- Clear private keys from memory after use

```python
# BAD - Don't do this
private_key = "123abc456def789..."  # Hardcoded!

# GOOD - Use environment variables
import os
private_key = os.environ.get('SOLANA_PRIVATE_KEY')

# BETTER - Use secure key management
from key_vault import get_secure_key
private_key = get_secure_key('solana_key')
```

### 2. Network Configuration

**Development/Testing**:
```json
{
  "network": {
    "default": "devnet"
  }
}
```

**Production**:
```json
{
  "network": {
    "default": "mainnet"
  },
  "security": {
    "requireConfirmation": true,
    "maxTransactionAmount": 1000
  }
}
```

### 3. Transaction Limits

Configure appropriate limits in `config/system-config.json`:

```json
{
  "security": {
    "maxTransactionAmount": 1000,
    "dailyLimit": 5000,
    "transactionDelay": 5,
    "requireConfirmation": true
  }
}
```

### 4. Input Validation

Always validate user inputs:

```python
def validate_wallet_address(address):
    """Validate Solana wallet address"""
    import base58
    try:
        decoded = base58.b58decode(address)
        return len(decoded) == 32
    except:
        return False

def validate_amount(amount):
    """Validate transaction amount"""
    try:
        amount = float(amount)
        return 0 < amount <= MAX_TRANSACTION_AMOUNT
    except:
        return False
```

### 5. Rate Limiting

Implement rate limiting to prevent abuse:

```python
from functools import wraps
from time import time

def rate_limit(calls=10, period=60):
    """Rate limiter decorator"""
    calls_made = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            calls_made[:] = [c for c in calls_made if c > now - period]
            
            if len(calls_made) >= calls:
                raise Exception("Rate limit exceeded")
            
            calls_made.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls=10, period=60)
def process_transaction(data):
    # Process transaction
    pass
```

## Transaction Safety

### 1. Confirmation Flow

Always confirm transactions before execution:

```python
def execute_transfer(from_wallet, to_wallet, amount):
    # Display transaction details
    print(f"""
    Transaction Details:
    - From: {from_wallet}
    - To: {to_wallet}
    - Amount: {amount} SOL
    - Dev Vault: 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr
    - All proceeds go to dev vault (100%)
    """)
    
    # Require confirmation
    confirmation = input("Confirm transaction? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Transaction cancelled")
        return None
    
    # Execute transaction
    return perform_transfer(from_wallet, to_wallet, amount)
```

### 2. Dry Run Mode

Test transactions without execution:

```python
def transfer_sol(from_wallet, to_wallet, amount, dry_run=True):
    if dry_run:
        return {
            "status": "dry_run",
            "operation": "transfer",
            "from": from_wallet,
            "to": to_wallet,
            "amount": amount,
            "note": "This is a simulation. No real transaction executed."
        }
    
    # Real transaction logic
    return execute_real_transfer(from_wallet, to_wallet, amount)
```

### 3. Transaction Verification

Verify transactions after submission:

```python
def verify_transaction(signature, network='devnet'):
    """Verify transaction on blockchain"""
    from solana.rpc.api import Client
    
    client = Client(NETWORK_URLS[network])
    result = client.get_transaction(signature)
    
    if result['result']:
        return {
            "status": "confirmed",
            "signature": signature,
            "block_time": result['result']['blockTime']
        }
    else:
        return {
            "status": "pending",
            "signature": signature
        }
```

## API Security

### 1. Authentication

Implement API authentication:

```python
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key != VALID_API_KEY:
            return jsonify({"error": "Invalid API key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/v1/transaction', methods=['POST'])
@require_api_key
def create_transaction():
    # Process transaction
    pass
```

### 2. CORS Configuration

Restrict CORS to trusted domains:

```python
from flask_cors import CORS

app = Flask(__name__)

# Restrict to specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://trusted-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "X-API-Key"]
    }
})
```

### 3. HTTPS Only

Always use HTTPS in production:

```python
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=True)
```

## Logging and Monitoring

### 1. Secure Logging

Log transactions without sensitive data:

```python
import logging

logging.basicConfig(
    filename='transactions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_transaction(tx_data):
    # Remove sensitive fields
    safe_data = {
        'operation': tx_data['operation'],
        'amount': tx_data['amount'],
        'signature': tx_data.get('signature'),
        'status': tx_data['status'],
        # NEVER log private_key!
    }
    logging.info(f"Transaction: {safe_data}")
```

### 2. Audit Trail

Maintain complete audit trail:

```python
def create_audit_entry(operation, user, details):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "user": user,
        "details": details,
        "ip_address": request.remote_addr
    }
    
    # Save to secure audit log
    save_audit_entry(entry)
```

### 3. Alert System

Set up alerts for suspicious activity:

```python
def check_suspicious_activity(transaction):
    alerts = []
    
    # Large amount
    if transaction['amount'] > ALERT_THRESHOLD:
        alerts.append("Large transaction amount")
    
    # Rapid transactions
    if get_recent_transaction_count() > RATE_THRESHOLD:
        alerts.append("High transaction frequency")
    
    # Send alerts
    if alerts:
        send_security_alert(alerts)
```

## Incident Response

### 1. Suspected Compromise

If private keys are compromised:

1. **Immediately**:
   - Stop all transactions
   - Rotate all API keys
   - Change all passwords

2. **Assess**:
   - Review transaction logs
   - Identify unauthorized transactions
   - Calculate potential losses

3. **Contain**:
   - Block compromised accounts
   - Update security rules
   - Notify affected users

4. **Recover**:
   - Transfer funds to new secure wallets
   - Update all credentials
   - Implement additional security measures

### 2. Transaction Errors

If transactions fail:

1. Check transaction signature on explorer
2. Verify network status
3. Check account balances
4. Review error logs
5. Retry with adjusted parameters if safe

### 3. Reporting Issues

Contact information for security issues:
- **Email**: security@example.com
- **Issue Tracker**: GitHub Issues (for non-sensitive issues)
- **Dev Vault**: 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr

## Best Practices Summary

✅ **DO**:
- Test on devnet first
- Use environment variables for secrets
- Validate all inputs
- Implement rate limiting
- Log transactions (without sensitive data)
- Require confirmations for large amounts
- Use HTTPS in production
- Keep dependencies updated
- Monitor for suspicious activity
- Have an incident response plan

❌ **DON'T**:
- Hardcode private keys
- Skip input validation
- Log sensitive data
- Allow unlimited transaction amounts
- Deploy directly to mainnet without testing
- Share API keys
- Ignore security warnings
- Store unencrypted credentials
- Skip transaction verification
- Ignore failed transactions

## Compliance Considerations

### 1. Know Your Customer (KYC)

For production systems, consider:
- User identity verification
- Transaction limits based on verification level
- Suspicious activity reporting

### 2. Anti-Money Laundering (AML)

Implement checks for:
- Large or unusual transactions
- Rapid movement of funds
- Transactions to/from high-risk addresses

### 3. Data Protection

Comply with regulations:
- GDPR (EU)
- CCPA (California)
- Other applicable data protection laws

## Security Checklist

Before production deployment:

- [ ] All private keys stored securely
- [ ] Environment variables configured
- [ ] Input validation implemented
- [ ] Rate limiting enabled
- [ ] HTTPS configured
- [ ] API authentication active
- [ ] Logging configured (without sensitive data)
- [ ] Monitoring and alerts set up
- [ ] Tested thoroughly on devnet
- [ ] Transaction limits configured
- [ ] Confirmation flow implemented
- [ ] Incident response plan documented
- [ ] Team trained on security procedures
- [ ] Regular security audits scheduled
- [ ] Backup and recovery plan in place

## Dev Vault Security

The dev vault address is **public** and **hardcoded** by design:
- Address: `5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr`
- Purpose: Receives all passive income (100%)
- Transparency: All transactions visible on blockchain
- Security: Private key must be secured separately

**Never** expose the dev vault private key in:
- Code repositories
- Configuration files
- Logs or console output
- API responses
- User interfaces

---

**Remember**: Security is not a one-time task but an ongoing process. Regularly review and update security measures.

**Dev Vault**: 5hSWosj58ki4A6hSfQrvteQU5QvyCWmhHn4AuqgaQzqr
