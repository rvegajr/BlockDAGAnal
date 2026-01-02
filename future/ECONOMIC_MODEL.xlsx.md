# BlockDAG Economic Model - Interactive Spreadsheet Specification

**Status**: Implementation-Ready  
**Version**: 1.0  
**Format**: Excel/Google Sheets with adjustable parameters

---

## Overview

This document specifies the structure for an interactive economic model spreadsheet that allows variable inputs for miner populations and price targets, generating comprehensive vesting and emission scenarios.

---

## Sheet Structure

### Sheet 1: Input Parameters

| Parameter | Cell | Default Value | Description |
|-----------|------|---------------|-------------|
| Launch Liquidity | B2 | $32,000,000 | Total DEX liquidity at launch |
| Target Price | B3 | $0.05 | Target launch price |
| Total Presale Supply | B4 | 50,000,000,000 | Total presale tokens |
| Base Coins | B5 | 17,000,000,000 | Base coin allocation |
| Bonus Coins | B6 | 33,000,000,000 | Bonus coin allocation |
| TGE Base Unlock % | B7 | 2% | Base coins unlocked at TGE |
| TGE Bonus Unlock % | B8 | 0% | Bonus coins unlocked at TGE |

#### Miner Population Scenarios

| Miner Type | Units Sold | Migration Rate | Active Miners | Base Daily Output |
|------------|-----------|----------------|---------------|-------------------|
| X1 | B10 | B11 | =B10*B11 | 20 BDAG |
| X10 | B12 | B13 | =B12*B13 | 200 BDAG |
| X30 | B14 | B15 | =B14*B15 | 600 BDAG |
| X100 | B16 | B17 | =B16*B17 | 2,000 BDAG |

**Scenarios**:
- **Conservative**: X1=50K(30%), X10=10K(80%), X30=2K(90%), X100=500(95%)
- **Moderate**: X1=100K(40%), X10=25K(85%), X30=5K(90%), X100=1.5K(95%)
- **Aggressive**: X1=200K(50%), X10=50K(90%), X30=10K(95%), X100=3K(98%)

---

### Sheet 2: Emission Schedule

| Month | Emission Rate | Daily Cap | Monthly Cap | Cumulative Emission | Circulating from Mining |
|-------|--------------|-----------|-------------|---------------------|------------------------|
| 0 | 0% | 0 | 0 | 0 | 0 |
| 1 | 10% | =B10*B11*20*0.1 + ... | =Daily*30 | =SUM(C2:C2) | =E2 |
| 2 | 10% | ... | ... | =SUM(C2:C3) | =E3 |
| ... | ... | ... | ... | ... | ... |
| 12 | 100% | =B10*B11*20*1.0 + ... | =Daily*30 | =SUM(C2:C13) | =E13 |

**Formulas**:
- Daily Cap = SUM(Active_Miners * Base_Output * Emission_Rate)
- Monthly Cap = Daily_Cap * 30
- Cumulative = SUM(Monthly_Caps)
- Circulating = Cumulative (assuming no staking)

---

### Sheet 3: Vesting Schedule

#### Base Coins Vesting

| Month | Phase | % Released | Tokens Released | Cumulative Released | Circulating Base |
|-------|------|------------|-----------------|---------------------|------------------|
| 0 | TGE | 2% | =B5*B7 | =D2 | =D2 |
| 1-12 | Cliff | 0% | 0 | =D2 | =D2 |
| 13 | Phase 1 Start | 0.67% | =B5*0.0067 | =D13+D2 | =E13 |
| 14 | Phase 1 | 0.67% | =B5*0.0067 | =D14+E13 | =E14 |
| ... | ... | ... | ... | ... | ... |
| 24 | Phase 1 End | 0.67% | =B5*0.0067 | =D24+E23 | =E24 |
| 25 | Phase 2 Start | 1.25% | =B5*0.0125 | =D25+E24 | =E25 |
| ... | ... | ... | ... | ... | ... |

**Formulas**:
- Phase 1 (Months 13-24): 8% total = 0.67% per month
- Phase 2 (Months 25-36): 15% total = 1.25% per month
- Phase 3 (Months 37-48): 25% total = 2.08% per month
- Phase 4 (Months 49-60): 50% total = 4.17% per month

#### Bonus Coins Vesting

| Month | Phase | % Released | Tokens Released | DAO Approved | Cumulative Released |
|-------|------|------------|-----------------|--------------|---------------------|
| 0 | TGE | 0% | 0 | N/A | 0 |
| 1-24 | Cliff | 0% | 0 | N/A | 0 |
| 25 | Phase 1 | 5% | =B6*0.05 | =IF(DAO_VOTE=TRUE, D25, 0) | =IF(F25=TRUE, D25, 0) |
| ... | ... | ... | ... | ... | ... |

---

### Sheet 4: Total Circulating Supply

| Month | Base Circulating | Bonus Circulating | Mining Circulating | Staked (30%) | Net Circulating | Price Impact |
|-------|------------------|-------------------|-------------------|--------------|-----------------|-------------|
| 0 | =Vesting!E2 | =Vesting!F2 | =Emission!E2 | =SUM(B2:D2)*0.3 | =SUM(B2:D2)*0.7 | =B2/E2 |
| 1 | =Vesting!E3 | =Vesting!F3 | =Emission!E3 | =SUM(B3:D3)*0.3 | =SUM(B3:D3)*0.7 | =B3/E3 |
| ... | ... | ... | ... | ... | ... | ... |

**Price Impact Formula**:
- Price = Launch_Liquidity / Net_Circulating
- If Net_Circulating > 640M, price < $0.05

---

### Sheet 5: Scenario Analysis

#### Scenario Matrix

| Scenario | Miner Pop | Target Price | Month 1 Circulating | Month 6 Circulating | Month 12 Circulating | Viable? |
|----------|-----------|--------------|---------------------|---------------------|----------------------|---------|
| 1 | Conservative | $0.05 | =Calc!E2 | =Calc!E7 | =Calc!E13 | =IF(E2<=640M, "YES", "NO") |
| 2 | Moderate | $0.05 | =Calc!E2 | =Calc!E7 | =Calc!E13 | =IF(E2<=640M, "YES", "NO") |
| 3 | Aggressive | $0.05 | =Calc!E2 | =Calc!E7 | =Calc!E13 | =IF(E2<=640M, "NO", "NO") |
| 4 | Conservative | $0.01 | =Calc!E2 | =Calc!E7 | =Calc!E13 | =IF(E2<=3200M, "YES", "NO") |
| 5 | Moderate | $0.01 | =Calc!E2 | =Calc!E7 | =Calc!E13 | =IF(E2<=3200M, "YES", "NO") |
| ... | ... | ... | ... | ... | ... | ... |

---

### Sheet 6: Price Sensitivity Analysis

| Circulating Supply | Price at $32M Liquidity | Market Cap | % of Total Supply |
|--------------------|------------------------|------------|-------------------|
| 320M | $0.10 | $32M | 0.64% |
| 640M | $0.05 | $32M | 1.28% |
| 1.28B | $0.025 | $32M | 2.56% |
| 2.56B | $0.0125 | $32M | 5.12% |
| 3.2B | $0.01 | $32M | 6.4% |
| 6.4B | $0.005 | $32M | 12.8% |
| 12.8B | $0.0025 | $32M | 25.6% |
| 25.6B | $0.00125 | $32M | 51.2% |
| 50B | $0.00064 | $32M | 100% |

---

### Sheet 7: Staking Impact Model

| Staking Participation | Month 1 Net Circulating | Month 6 Net Circulating | Month 12 Net Circulating | Price Support |
|------------------------|-------------------------|-------------------------|--------------------------|---------------|
| 0% | =Calc!E2 | =Calc!E7 | =Calc!E13 | =B2/640M*0.05 |
| 10% | =Calc!E2*0.9 | =Calc!E7*0.9 | =Calc!E13*0.9 | =B3/640M*0.05 |
| 20% | =Calc!E2*0.8 | =Calc!E7*0.8 | =Calc!E13*0.8 | =B4/640M*0.05 |
| 30% | =Calc!E2*0.7 | =Calc!E7*0.7 | =Calc!E13*0.7 | =B5/640M*0.05 |
| 40% | =Calc!E2*0.6 | =Calc!E7*0.6 | =Calc!E13*0.6 | =B6/640M*0.05 |
| 50% | =Calc!E2*0.5 | =Calc!E7*0.5 | =Calc!E13*0.5 | =B7/640M*0.05 |

---

## Key Formulas Reference

### Maximum Circulating Supply
```
Max_Circulating = Launch_Liquidity / Target_Price
```

### Daily Mining Emission
```
Daily_Emission = SUM(Active_Miners[Type] * Base_Output[Type] * Emission_Rate)
```

### Monthly Mining Emission
```
Monthly_Emission = Daily_Emission * 30
```

### Net Circulating Supply
```
Net_Circulating = (Base_Vested + Bonus_Vested + Mining_Emission) * (1 - Staking_Rate)
```

### Price Calculation
```
Price = Launch_Liquidity / Net_Circulating
```

### Vesting Release (Base Coins)
```
Month_N_Release = IF(Month < 13, TGE_Amount, 
                 IF(Month < 25, Base_Total * 0.0067,
                 IF(Month < 37, Base_Total * 0.0125,
                 IF(Month < 49, Base_Total * 0.0208,
                 Base_Total * 0.0417))))
```

---

## Visualization Charts

### Chart 1: Circulating Supply Over Time
- X-axis: Months (0-60)
- Y-axis: Tokens (Millions)
- Series:
  - Base Coins Circulating
  - Bonus Coins Circulating
  - Mining Emission Circulating
  - Net Circulating (after staking)
  - 640M Target Line

### Chart 2: Price Impact Over Time
- X-axis: Months (0-60)
- Y-axis: Price ($)
- Series:
  - Actual Price (based on circulating)
  - Target Price ($0.05)
  - Emergency Threshold ($0.02)

### Chart 3: Emission Rate Schedule
- X-axis: Months (0-12)
- Y-axis: Emission Rate (%)
- Series:
  - Actual Emission Rate
  - Target Schedule

---

## Usage Instructions

1. **Select Miner Scenario**: Change values in Sheet 1 (Input Parameters)
2. **Select Price Target**: Change Target Price in B3
3. **Adjust Staking Rate**: Modify staking participation in Sheet 7
4. **Review Results**: Check Sheet 4 (Total Circulating) and Sheet 5 (Scenario Analysis)
5. **Compare Scenarios**: Use Sheet 5 to compare different combinations

---

## Export Formats

- **Excel**: `.xlsx` with formulas and charts
- **Google Sheets**: Shareable link with same functionality
- **PDF Report**: Static snapshot of current scenario

---

## References

- [Vesting Contract Spec](../specs/contracts/VESTING_CONTRACT_SPEC.md)
- [Emission Cap Schedule](../specs/mining/EMISSION_CAP_SCHEDULE.md)
- [Staking Contract Spec](../specs/contracts/STAKING_CONTRACT_SPEC.md)

