# BlockDAG Vesting Contracts Deployment Plan

**Date**: January 2025  
**Status**: READY FOR DEPLOYMENT  
**Target**: Protocol v2.6 Model (Best Investor Returns)

---

## 🎯 Deployment Overview

Deploying the vesting smart contracts based on **Protocol v2.6** parameters (validated as best for investor returns):

- ✅ 3% TGE unlock
- ✅ 3-month cliff
- ✅ 21-month vesting
- ✅ Oracle price gate at $0.05
- ✅ 40% staking APY
- ✅ Emergency brake protection

---

## 📋 Pre-Deployment Checklist

### 1. Contract Implementation
- [ ] Write VestingContract.sol based on specs
- [ ] Write StakingContract.sol based on specs
- [ ] Write EmergencyBrake.sol based on specs
- [ ] Write OraclePriceGate.sol (Chainlink integration)
- [ ] Write DAOGovernance.sol for milestone triggers

### 2. Testing
- [ ] Unit tests for all contracts
- [ ] Integration tests for vesting flows
- [ ] Fuzz testing for edge cases
- [ ] Gas optimization tests
- [ ] Reorg resistance tests

### 3. Security
- [ ] Slither static analysis
- [ ] Mythril security audit
- [ ] External security audit (recommended)
- [ ] Multisig wallet setup
- [ ] Timelock controller setup

### 4. Configuration
- [ ] Deployer wallet funded
- [ ] Oracle addresses configured
- [ ] Initial parameters set:
  - [ ] TGE unlock: 3%
  - [ ] Cliff: 3 months
  - [ ] Vesting: 21 months
  - [ ] Price gate: $0.05
  - [ ] Emergency brake: $0.02 / $10M
- [ ] Token addresses verified
- [ ] Admin addresses verified

### 5. Network Setup
- [ ] Hardhat/Foundry configured
- [ ] Testnet RPC configured
- [ ] Mainnet RPC configured
- [ ] Explorer verification ready

---

## 🚀 Deployment Steps

### Phase 1: Testnet Deployment

1. **Deploy Core Contracts**
   ```bash
   npx hardhat run scripts/deploy/01-deploy-vesting.js --network phoenixTestnet
   npx hardhat run scripts/deploy/02-deploy-staking.js --network phoenixTestnet
   npx hardhat run scripts/deploy/03-deploy-emergency-brake.js --network phoenixTestnet
   npx hardhat run scripts/deploy/04-deploy-oracle-gate.js --network phoenixTestnet
   ```

2. **Initialize Contracts**
   ```bash
   npx hardhat run scripts/deploy/05-initialize-vesting.js --network phoenixTestnet
   npx hardhat run scripts/deploy/06-initialize-staking.js --network phoenixTestnet
   ```

3. **Wire Contracts Together**
   ```bash
   npx hardhat run scripts/deploy/07-wire-contracts.js --network phoenixTestnet
   ```

4. **Transfer Admin to Multisig**
   ```bash
   npx hardhat run scripts/deploy/08-transfer-admin.js --network phoenixTestnet
   ```

5. **Verify on Explorer**
   ```bash
   npx hardhat verify --network phoenixTestnet <CONTRACT_ADDRESS>
   ```

### Phase 2: Testnet Validation

1. **Health Checks**
   - [ ] Vesting contract paused state: false
   - [ ] Staking tiers configured correctly
   - [ ] Oracle price feed connected
   - [ ] Emergency brake thresholds set
   - [ ] Admin roles assigned

2. **End-to-End Tests**
   - [ ] TGE unlock works (3% release)
   - [ ] Cliff period enforced (no releases months 1-3)
   - [ ] Linear vesting works (month 4+)
   - [ ] Price gate blocks releases below $0.05
   - [ ] Emergency brake triggers correctly
   - [ ] Staking deposits/withdrawals work

3. **Load Testing**
   - [ ] 1000+ concurrent claims
   - [ ] Gas optimization verified
   - [ ] No reentrancy issues

### Phase 3: Mainnet Deployment

1. **Pre-Mainnet Checklist**
   - [ ] All testnet tests pass
   - [ ] Security audit complete
   - [ ] Multisig signers ready
   - [ ] Timelock delay set (recommended: 48 hours)
   - [ ] Emergency contacts ready

2. **Deploy to Mainnet**
   ```bash
   npx hardhat run scripts/deploy/01-deploy-vesting.js --network phoenix
   # ... repeat for all contracts
   ```

3. **Initialize Mainnet**
   ```bash
   npx hardhat run scripts/deploy/05-initialize-vesting.js --network phoenix
   # ... repeat for all initialization scripts
   ```

4. **Transfer Admin to Multisig**
   ```bash
   npx hardhat run scripts/deploy/08-transfer-admin.js --network phoenix
   ```

5. **Verify on Explorer**
   ```bash
   npx hardhat verify --network phoenix <CONTRACT_ADDRESS>
   ```

---

## 📊 Deployment Parameters

### Vesting Contract

| Parameter | Value | Notes |
|-----------|-------|-------|
| TGE Unlock | 3% | 510M tokens |
| Cliff Period | 3 months | 90 days |
| Vesting Duration | 21 months | 630 days |
| Base Coins | 17B | Total allocation |
| Bonus Coins | 33B | Total allocation |

### Staking Contract

| Parameter | Value | Notes |
|-----------|-------|-------|
| Tier 1 APY | 15% | 30-day lock |
| Tier 2 APY | 25% | 90-day lock |
| Tier 3 APY | 35% | 180-day lock |
| Tier 4 APY | 40% | 365-day lock |

### Emergency Brake

| Parameter | Value | Notes |
|-----------|-------|-------|
| Price Threshold | $0.02 | Triggers pause |
| Liquidity Threshold | $10M | Triggers pause |
| Recovery Period | 7 days | Price must stay above threshold |

### Oracle Price Gate

| Parameter | Value | Notes |
|-----------|-------|-------|
| Price Threshold | $0.05 | Blocks releases below |
| Oracle | Chainlink | Price feed |
| Update Frequency | Daily | Checks price |

---

## 🔐 Security Considerations

### Multisig Configuration
- **Recommended**: 3-of-5 multisig
- **Signers**: Team lead, CTO, CFO, Community rep, External advisor
- **Timelock**: 48-hour delay for critical operations

### Admin Functions
- Pause vesting (emergency only)
- Update price thresholds (timelocked)
- Update oracle address (timelocked)
- Emergency brake override (multisig required)

### Access Control
- **Owner**: Multisig wallet
- **Admin**: Timelock controller
- **Pauser**: Emergency multisig (2-of-3)
- **Oracle**: Chainlink price feed

---

## 📝 Post-Deployment Tasks

### Immediate (Day 1)
- [ ] Publish contract addresses
- [ ] Update documentation with addresses
- [ ] Announce deployment to community
- [ ] Set up monitoring/alerts

### Week 1
- [ ] Monitor first vesting releases
- [ ] Verify staking deposits
- [ ] Check oracle price updates
- [ ] Review gas usage

### Month 1
- [ ] First cliff period ends
- [ ] Verify linear vesting starts
- [ ] Monitor price stability
- [ ] Collect user feedback

---

## 🚨 Emergency Procedures

### If Price Drops Below $0.02
1. Emergency brake auto-triggers
2. All vesting pauses
3. Staking rewards increase by 50%
4. Notify community
5. Assess market conditions
6. Plan recovery strategy

### If Oracle Fails
1. Pause vesting (manual override)
2. Switch to backup oracle
3. Update contract configuration
4. Resume vesting

### If Critical Bug Found
1. Pause all contracts immediately
2. Notify security team
3. Assess impact
4. Deploy fix via upgrade (if proxy)
5. Or deploy new contracts and migrate

---

## 📁 Deployment Artifacts

After deployment, save:
- `deployment.json` - All contract addresses
- `deployment-transactions.json` - Transaction hashes
- `verification-ids.json` - Explorer verification IDs
- `initial-config.json` - Initial parameters
- `multisig-config.json` - Multisig addresses

---

## 📞 Support Contacts

- **Technical Lead**: [TBD]
- **Security Team**: [TBD]
- **Operations**: [TBD]
- **Emergency Hotline**: [TBD]

---

*Deployment Plan v1.0*  
*Last Updated: January 2025*  
*Status: READY FOR IMPLEMENTATION*

