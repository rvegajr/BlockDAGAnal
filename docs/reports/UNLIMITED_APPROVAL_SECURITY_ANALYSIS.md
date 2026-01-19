# BlockDAG Unlimited Approval Security Analysis

**Date**: January 19, 2026  
**Status**: ✅ RESOLVED - Claim Unsubstantiated  
**Analyst**: Technical Security Review  

---

## Executive Summary

A security concern was raised in the BlockDAG investor community claiming that BlockDAG's purchase contract has an "Unlimited Allowance" vulnerability that could allow the team to drain investor wallets. After thorough on-chain analysis of actual transaction hashes, **this claim is FALSE**.

The unlimited approvals found on the investigated wallet belong to **legitimate DeFi protocols (0x Protocol and THORChain)**, not BlockDAG. Furthermore, BlockDAG ETH/BNB purchases are sent to a **regular wallet address (EOA)**, not a smart contract, making token approval exploits technically impossible.

---

## Table of Contents

1. [The Original Claim](#the-original-claim)
2. [Technical Background](#technical-background)
3. [Evidence Analyzed](#evidence-analyzed)
4. [On-Chain Investigation](#on-chain-investigation)
5. [Findings](#findings)
6. [Technical Verdict](#technical-verdict)
7. [Recommendations](#recommendations)
8. [Appendix: How to Verify Yourself](#appendix-how-to-verify-yourself)

---

## The Original Claim

### Source
A message circulated in Telegram groups (forwarded from user "Alpha Sow") stated:

> ⚠️ CRITICAL SECURITY ALERT - TO ALL INVESTORS ⚠️
>
> I performed a technical audit on blockchain explorers (BscScan / Etherscan) to check the permissions (allowances) of the contract we used to purchase.
>
> The finding is serious: The contract has an "Unlimited Allowance."
>
> What this means in reality: As long as your funds remain in the wallet that interacted with this contract, GK and his team technically have the ability to drain your account at any time without your signature.

### Specific Claims Made

| Claim | Implication |
|-------|-------------|
| BlockDAG contract has unlimited allowance | Team can drain USDT/tokens at will |
| This is a "drainer" vulnerability | Malicious intent suggested |
| All investors at risk | Widespread vulnerability |
| Funds should be moved immediately | Urgent action required |

---

## Technical Background

### What Are Token Approvals?

ERC-20 tokens (like USDT, USDC) require a two-step process for third-party spending:

```
Step 1: APPROVE - Grant permission to a spender contract
        approve(spender, amount)
        
Step 2: TRANSFER FROM - Spender moves your tokens
        transferFrom(owner, recipient, amount)
```

### Unlimited Approvals Explained

When you approve a contract, you specify an amount. Many DeFi protocols request "unlimited" approval (`type(uint256).max` = 2²⁵⁶ - 1) for convenience:

```solidity
// Unlimited approval value
115792089237316195423570985008687907853269984665640564039457584007913129639935
```

**Why this exists**: Saves gas by avoiding repeated approval transactions.

**The risk**: If the approved contract is malicious or compromised, it can drain your approved tokens.

### Critical Distinctions

| Concept | Can Be Drained? | Why |
|---------|-----------------|-----|
| Native ETH/BNB | ❌ NO | Not ERC-20, no approval mechanism exists |
| ERC-20 with approval | ⚠️ Potentially | Only if approved to malicious contract |
| ERC-20 without approval | ❌ NO | No permission granted |
| Transfers to EOA (wallet) | ❌ NO | One-time transaction, no ongoing permission |
| Transfers to Contract | ⚠️ Depends | Contract must have drain function + approval |

---

## Evidence Analyzed

### Source Materials

1. **Screenshots from affected investor ("Jaime")**:
   - BlockDAG purchase portal transaction history
   - Etherscan transaction list
   - Etherscan Token Approval Checker results

2. **Transaction Hashes Provided**:
   - `0xe0e3e81fbfafae88b41fc7425cd307365ca45dd8e7a9b22b8986845d95b1d994`
   - `0xc8f8bf6bac86e50b69b9a6886942c331748db3e0936bde86fefcd91ff9d52584`

3. **Wallet Address Investigated**:
   - `0x3109Af458933FD1aA1E84C1Aea21e3075D99aD3c`

---

## On-Chain Investigation

### Transaction 1: The Approval Transaction

**Hash**: `0xe0e3e81fbfafae88b41fc7425cd307365ca45dd8e7a9b22b8986845d95b1d994`

| Field | Value |
|-------|-------|
| **Action** | Approve Unlimited USDT |
| **From** | 0x3109Af458933FD1aA1E84C1Aea21e3075D99aD3c |
| **To (Token Contract)** | 0xdAC17F958D2ee523a2206206994597C13D831ec7 (Tether USDT) |
| **Approved Spender** | **0x: Allowance Holder** |
| **Date** | February 5, 2025 |
| **Status** | Success |

#### Analysis

The approved spender is **0x Protocol's Allowance Holder** - a core component of the 0x DEX aggregator infrastructure. This is:
- ✅ A legitimate, audited DeFi protocol
- ✅ Used by major DEX aggregators (Matcha, Rango, etc.)
- ❌ **NOT a BlockDAG contract**

**Etherscan Link**: [View Transaction](https://etherscan.io/tx/0xe0e3e81fbfafae88b41fc7425cd307365ca45dd8e7a9b22b8986845d95b1d994)

---

### Transaction 2: The BlockDAG Purchase

**Hash**: `0xc8f8bf6bac86e50b69b9a6886942c331748db3e0936bde86fefcd91ff9d52584`

| Field | Value |
|-------|-------|
| **Action** | Transfer 0.625 ETH ($1,997.05) |
| **From** | 0x3109Af458933FD1aA1E84C1Aea21e3075D99aD3c |
| **To** | 0xe19d644E7B535C45E009382F40EE35628899DBE6 |
| **Value** | 0.625 ETH |
| **Date** | April 19, 2025 |
| **Status** | Success |

#### Analysis

This transaction shows a **direct ETH transfer** to address `0xe19d644E7B535C45E009382F40EE35628899DBE6`.

**Etherscan Link**: [View Transaction](https://etherscan.io/tx/0xc8f8bf6bac86e50b69b9a6886942c331748db3e0936bde86fefcd91ff9d52584)

---

### Destination Address Analysis

**Address**: `0xe19d644E7B535C45E009382F40EE35628899DBE6`

| Property | Value | Significance |
|----------|-------|--------------|
| **Address Type** | EOA (Externally Owned Account) | NOT a smart contract |
| **Total Transactions** | 102,753 | High-volume payment receiver |
| **First Transaction** | ~1 year 90 days ago | Consistent with presale timeline |
| **Current Balance** | ~0.006 ETH | Funds moved out regularly |
| **Contract Code** | None | Cannot execute arbitrary code |

#### Critical Finding

The BlockDAG payment destination is a **regular wallet address**, NOT a smart contract.

**This means**:
1. You cannot grant token approvals to an EOA - only contracts can receive approvals
2. Direct ETH transfers create no ongoing permissions
3. Once ETH is sent, the transaction is complete with no residual access

**Etherscan Link**: [View Address](https://etherscan.io/address/0xe19d644E7B535C45E009382F40EE35628899DBE6)

---

### Token Approval Checker Results

The wallet's Etherscan Token Approval Checker showed:

| Approved Spender | Token | Allowance | Is This BlockDAG? |
|------------------|-------|-----------|-------------------|
| 0x: Allowance Holder | USDT | Unlimited | ❌ NO - 0x Protocol |
| THORChain: THORChain Router | USDT | Unlimited | ❌ NO - THORChain DEX |

**No BlockDAG contract appears in the approval list.**

---

## Findings

### Finding 1: Unlimited Approvals Exist, But Not to BlockDAG

The investigated wallet does have unlimited USDT approvals, but they are to:
- **0x Protocol** (legitimate DEX aggregator)
- **THORChain** (legitimate cross-chain DEX)

These approvals were likely created when the user swapped tokens through a DEX aggregator, completely unrelated to BlockDAG purchases.

### Finding 2: BlockDAG Uses Direct Transfers, Not Contract Interactions

BlockDAG presale purchases via ETH/BNB are processed as:
- **Simple value transfers** to a receiving wallet
- **NOT interactions with a smart contract**
- **No approval required or requested**

### Finding 3: ETH/BNB Has No Approval Mechanism

Native blockchain currencies (ETH, BNB) are fundamentally different from ERC-20 tokens:
- No `approve()` function exists
- No `transferFrom()` capability
- Each transfer is explicit and one-time
- Impossible to create "drainer" vulnerability with native currency transfers

### Finding 4: No Evidence of BlockDAG Contract in Approvals

Despite the claim, no BlockDAG-related contract address was found in the wallet's token approval list. The original claimant either:
1. Misidentified which protocol created the approval
2. Confused DEX aggregator approvals with BlockDAG
3. Did not understand the technical distinction

---

## Technical Verdict

### Claim Assessment Matrix

| Original Claim | Verdict | Evidence |
|----------------|---------|----------|
| "BlockDAG contract has unlimited allowance" | ❌ **FALSE** | No BlockDAG contract in approval list |
| "Team can drain your account" | ❌ **FALSE** | ETH purchases go to EOA, not contract |
| "This is a drainer vulnerability" | ❌ **FALSE** | No approval granted to BlockDAG |
| "Major security flaw" | ❌ **FALSE** | Standard ETH transfer mechanism |
| "Move funds immediately" | ⚠️ **Unnecessary for BlockDAG reason** | Good practice generally |

### Risk Assessment by Purchase Method

| Payment Method | Approval Risk from BlockDAG | Reason |
|----------------|----------------------------|--------|
| ETH | ❌ **NONE** | Native currency, no approval mechanism |
| BNB | ❌ **NONE** | Native currency, no approval mechanism |
| USDT/USDC | ⚠️ **Unconfirmed** | Would require approval, but no evidence of unlimited request |
| TON | ❌ **NONE** | Different blockchain, separate trust model |

### Conclusion

**The security alert is based on a technical misunderstanding.**

The unlimited approvals found on the wallet are:
1. To legitimate DeFi protocols (0x, THORChain)
2. Unrelated to BlockDAG purchases
3. Common artifacts of DEX usage

BlockDAG's ETH/BNB purchase flow uses direct transfers to a regular wallet, which creates **zero ongoing permissions** and **cannot be used to drain funds**.

---

## Recommendations

### For Investors Concerned About This Issue

1. **Check your own approvals**: Use [revoke.cash](https://revoke.cash) or Etherscan's Token Approval Checker
2. **Look for the spender**: If you see unlimited approvals, check WHO the spender is
3. **Revoke unnecessary approvals**: Good hygiene regardless of BlockDAG
4. **Understand the distinction**: ETH/BNB transfers ≠ ERC-20 approvals

### For Community Moderators

1. **Correct misinformation**: Share this analysis when the claim resurfaces
2. **Educate on token mechanics**: Many users don't understand approval vs. transfer
3. **Encourage verification**: Teach users to check their own transactions

### General Security Best Practices

| Practice | Why |
|----------|-----|
| Use separate wallets | Isolate DeFi activity from long-term holdings |
| Revoke unused approvals | Reduce attack surface |
| Verify before approving | Check spender contract legitimacy |
| Don't store value in hot wallets | Minimize exposure |

---

## Appendix: How to Verify Yourself

### Step 1: Check Your Token Approvals

1. Go to [Etherscan Token Approval Checker](https://etherscan.io/tokenapprovalchecker)
2. Enter your wallet address
3. Review the "Approved Spender" column
4. Look for any BlockDAG-related contracts (there shouldn't be any for ETH purchases)

### Step 2: Trace a Purchase Transaction

1. Find your BlockDAG purchase transaction hash
2. Look it up on Etherscan: `https://etherscan.io/tx/[YOUR_TX_HASH]`
3. Check the "To" field:
   - If it shows an address without "Contract" label → EOA (safe)
   - If it shows "Contract" → Check what contract it is

### Step 3: Verify the Destination Address

1. Click on the "To" address
2. Look for "Contract" tab - if missing, it's an EOA
3. Check transaction history for patterns

### Step 4: Revoke Suspicious Approvals

1. Use [revoke.cash](https://revoke.cash)
2. Connect your wallet
3. Find unlimited approvals you don't recognize
4. Click "Revoke" (requires gas)

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-19 | 1.0 | Initial analysis and publication |

---

## References

- [Etherscan Transaction 1](https://etherscan.io/tx/0xe0e3e81fbfafae88b41fc7425cd307365ca45dd8e7a9b22b8986845d95b1d994)
- [Etherscan Transaction 2](https://etherscan.io/tx/0xc8f8bf6bac86e50b69b9a6886942c331748db3e0936bde86fefcd91ff9d52584)
- [BlockDAG Payment Address](https://etherscan.io/address/0xe19d644E7B535C45E009382F40EE35628899DBE6)
- [ERC-20 Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [0x Protocol Documentation](https://0x.org/docs)
- [Revoke.cash](https://revoke.cash)
