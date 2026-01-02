# Frequently Asked Questions (FAQ)

## General Questions

### What is DBP?

DBP (Decentralized BlockDAG Protocol) is an open-source blockchain that combines the speed and scalability of DAG (Directed Acyclic Graph) technology with smart contract capabilities through EVM integration. It's built as a fork of Kaspa with significant enhancements.

### Why was DBP created?

DBP was created to address the failures of closed-source projects like BlockDAG, which promised revolutionary technology but failed to deliver after 2+ years and 45+ presale batches. We're providing what was promised: a transparent, working, auditable blockchain.

### How is DBP different from BlockDAG?

| Feature | DBP | BlockDAG |
|---------|-----|----------|
| **Source Code** | Open source, auditable | Closed, possibly plagiarized |
| **Working Product** | Yes (testnet in 90 days) | No (2+ years, nothing) |
| **Smart Contracts** | Yes (full EVM) | Promised, never delivered |
| **Transparency** | Complete (public GitHub) | Zero (hidden in Docker) |
| **Team** | Public, verifiable | Anonymous |
| **Launch** | Fair launch (mining) | Endless presale |

### What makes DBP unique?

1. **Open Source from Day One**: Every line of code is auditable
2. **Dual Mining Algorithms**: kHeavyHash + SHA-3 for hardware flexibility
3. **EVM + DAG**: First open-source DAG blockchain with full smart contract support
4. **Fair Launch**: No presale, no premine - earn through mining
5. **Product First**: Working testnet before asking for investment

---

## Technical Questions

### What consensus mechanism does DBP use?

DBP uses GHOSTDAG, a generalization of Nakamoto consensus to DAG structures. It allows parallel block creation while maintaining security and ordering.

### What are the mining algorithms?

DBP supports two mining algorithms:

1. **kHeavyHash**: Kaspa-compatible algorithm
   - Works with existing Kaspa mining hardware
   - GPU and ASIC friendly
   
2. **SHA-3**: Standard cryptographic hash
   - Works with BlockDAG mining hardware
   - Broader hardware compatibility

Miners can choose which algorithm to use based on their hardware.

### Does DBP support smart contracts?

Yes! DBP has full EVM (Ethereum Virtual Machine) compatibility. This means:
- Deploy Solidity smart contracts
- Use existing Ethereum tools (Remix, Hardhat, Truffle)
- ERC-20, ERC-721, ERC-1155 token standards
- Full DeFi compatibility

### What's the transaction speed?

- **Block time**: ~1 second (target)
- **Confirmation**: 1-5 seconds for finality
- **Throughput**: 1,000+ transactions per second (TPS)
- **Scalability**: 10-100 blocks per second via DAG

### How does DBP handle state in a DAG?

DBP uses GHOSTDAG ordering to create a deterministic sequence of blocks. Smart contract transactions are executed in this canonical order, ensuring consistent state across all nodes.

### Is DBP compatible with Kaspa?

Partially:
- **Mining**: Yes, Kaspa miners can mine DBP with same hardware
- **Software**: Kaspa mining software works with minor modifications
- **Pools**: Kaspa pools can easily add DBP support
- **Blockchain**: No, different chain (not merge-mined)

### What programming languages are supported?

- **Smart Contracts**: Solidity (same as Ethereum)
- **Core Blockchain**: Go (Golang)
- **Tools/SDKs**: JavaScript, Python, Go
- **Mobile Wallet**: React Native (TypeScript)

---

## Mining Questions

### How do I mine DBP?

1. **Get Mining Hardware**:
   - GPUs (NVIDIA or AMD)
   - Kaspa ASICs (for kHeavyHash)
   - BlockDAG ASICs (for SHA-3)

2. **Choose Mining Software**:
   - lolminer (for kHeavyHash)
   - bzminer (for both algorithms)
   - Custom miners (will be released)

3. **Join a Mining Pool**:
   - Woolypooly
   - Herominers
   - Or solo mine

4. **Start Mining**:
   ```bash
   lolminer --algo KHEAVYHASH --pool stratum+tcp://pool.bdp.network:3333 --user YOUR_ADDRESS
   ```

### What are the mining rewards?

- **Initial Reward**: 50 DBP per block
- **Halving**: Every 210,000 blocks (~1 year)
- **Total Supply**: 21 million DBP (same as Bitcoin)
- **Algorithm**: Same reward regardless of algorithm used

### Can I mine with my Kaspa hardware?

Yes! If you have:
- **Kaspa GPUs**: Can mine DBP using kHeavyHash
- **Kaspa ASICs**: Can mine DBP with firmware update
- **Kaspa Mining Software**: Works with minor config changes

### Can I mine with my BlockDAG hardware?

Yes! BlockDAG ASICs can mine DBP using the SHA-3 algorithm. This gives those machines actual utility instead of being paperweights if BlockDAG never launches.

### What's more profitable, kHeavyHash or SHA-3?

Profitability depends on:
- Your hardware
- Current difficulty for each algorithm
- Electricity costs

The network automatically balances difficulty so both algorithms remain competitive over time.

### How do mining pools work with DBP?

Mining pools:
1. Combine hashrate from many miners
2. Find blocks more frequently
3. Distribute rewards proportionally
4. Charge small fee (1-2%)

Recommended for small miners. Solo mining only viable with large hashrate.

---

## Economic Questions

### What's the tokenomics?

- **Total Supply**: 21 million DBP
- **Initial Reward**: 50 DBP per block
- **Halving Schedule**: Every 210,000 blocks
- **Distribution**: 100% through mining (no presale)
- **Dev Allocation**: 1-5% (vested, from mining)

### Is there a presale?

**NO.** DBP has zero presale, zero ICO, zero private sale. The only way to get DBP is:
1. Mine it
2. Buy it on exchanges (after launch)
3. Earn it (bug bounties, grants)

This ensures fair distribution and decentralization.

### What's the expected market cap?

Conservative estimates:
- **Year 1**: $50-150M (5-10% of Kaspa's market cap)
- **Year 2**: $200-500M (10-20% of Kaspa's market cap)
- **Year 3**: $1-3B (rival established DAG projects)

Depends on: adoption, technology delivery, market conditions, competition.

### When will DBP be listed on exchanges?

Timeline:
- **Month 1-2**: Testnet DEX (for testing)
- **Month 9**: Mainnet launch
- **Month 10**: DEX listings (Uniswap, etc.)
- **Month 10-12**: CEX applications (KuCoin, Gate.io)
- **Year 2**: Major exchanges (Binance, Coinbase)

### How is development funded?

- **Initial Phase**: Volunteer team (equity/token allocation)
- **Security Audits**: $20,000 (one-time, from donations)
- **Ongoing**: Small dev allocation (1-5% of supply)
- **Grants**: Community-funded development

No VCs, no ICO, no presale means true community ownership.

---

## Development Questions

### How can I contribute to DBP?

Multiple ways:
1. **Code Contributions**: Submit PRs to GitHub
2. **Documentation**: Improve docs, write tutorials
3. **Testing**: Run testnet nodes, report bugs
4. **Community**: Answer questions, help newcomers
5. **Development**: Build DApps on DBP
6. **Marketing**: Spread the word on social media

### Is there a developer grant program?

Yes! Launching with mainnet:
- **Grant Pool**: $100,000 (Year 1)
- **Categories**: DeFi, NFTs, Tools, Infrastructure
- **Application**: Via GitHub discussions
- **Review**: Community + core team

### What developer tools are available?

- **Block Explorer**: View blocks, transactions, contracts
- **RPC API**: JSON-RPC for blockchain queries
- **GraphQL API**: Flexible data querying
- **Web3.js/Ethers.js**: JavaScript libraries
- **Remix IDE**: Deploy contracts in browser
- **Hardhat**: Smart contract development framework
- **Truffle**: Alternative development framework

### Can I build DApps on DBP?

Absolutely! DBP supports:
- **DeFi**: DEXs, lending, staking
- **NFTs**: Marketplaces, collections, games
- **DAOs**: Governance, treasuries
- **Gaming**: On-chain games, metaverse
- **Social**: Decentralized social networks
- **Identity**: DIDs, credentials

If it works on Ethereum, it works on DBP (but faster).

### How do I deploy a smart contract?

```solidity
// 1. Write contract (Solidity)
pragma solidity ^0.8.0;

contract HelloWorld {
    string public message;
    
    constructor() {
        message = "Hello DBP!";
    }
}
```

```bash
# 2. Compile with Hardhat
npx hardhat compile

# 3. Deploy to DBP
npx hardhat run scripts/deploy.js --network dbp

# 4. Verify on explorer
npx hardhat verify --network dbp CONTRACT_ADDRESS
```

---

## Security Questions

### Is DBP secure?

Security measures:
- **Audits**: Multiple professional security audits
- **Bug Bounty**: Immunefi program (up to $100k rewards)
- **Open Source**: Community can audit code
- **Testing**: 90%+ code coverage, extensive tests
- **PoW**: Battle-tested consensus mechanism

### Has DBP been audited?

Timeline:
- **Pre-Launch**: OpenZeppelin (smart contracts)
- **Pre-Launch**: Trail of Bits (blockchain core)
- **Ongoing**: Community audits (open source)
- **Post-Launch**: Additional audits as needed

All audit reports will be public.

### What if a critical bug is found?

Responsible disclosure process:
1. **Report**: security@bdp.network (PGP encrypted)
2. **Response**: Within 24 hours
3. **Assessment**: Verify and prioritize
4. **Fix**: Develop and test patch
5. **Disclosure**: Coordinate public announcement
6. **Reward**: Bug bounty payment

### Is DBP vulnerable to 51% attacks?

Mitigations:
- **High Hashrate**: From dual algorithms
- **GHOSTDAG**: More resistant than linear chains
- **Monitoring**: Network health metrics
- **Community**: Diverse miner base

Risk is low with proper decentralization.

### How do you prevent spam transactions?

- **Gas Fees**: Cost to send transactions
- **Mempool**: Priority by fee
- **Rate Limiting**: Node-level protections
- **Block Size**: Limits transaction count

Same mechanisms as Ethereum.

---

## Wallet & Usage Questions

### What wallets support DBP?

**Official Wallet**:
- Mobile (iOS/Android) - React Native
- Web wallet (browser)
- CLI wallet (command line)

**Future Support**:
- MetaMask (via custom network)
- Trust Wallet
- Ledger hardware wallet
- Trezor hardware wallet

### How do I create a wallet?

```bash
# CLI Method
dbp-cli wallet create

# Mobile Method
1. Download DBP wallet app
2. Tap "Create Wallet"
3. Write down seed phrase (24 words)
4. Confirm seed phrase
5. Set PIN/biometric

# MetaMask Method
1. Open MetaMask
2. Add Custom Network:
   - Network Name: DBP
   - RPC URL: https://rpc.bdp.network
   - Chain ID: 1234
   - Currency: DBP
3. Done!
```

### How do I back up my wallet?

**Seed Phrase Method**:
1. Write down 24-word seed phrase
2. Store securely (fireproof safe, bank vault)
3. NEVER share with anyone
4. NEVER store digitally (screenshots, cloud)

**Hardware Wallet Method**:
1. Buy Ledger/Trezor
2. Set up device
3. Connect to DBP wallet
4. Seeds stored on hardware (safer)

### What if I lose my seed phrase?

**Unfortunate reality**: Funds are **permanently lost**.

**Prevention**:
- Multiple backups (separate locations)
- Metal seed storage (fire/water resistant)
- Consider multi-sig (requires multiple keys)
- Test recovery before sending large amounts

### How do I send DBP?

```bash
# CLI
dbp-cli send --to dbp1qw508d6qejxtdg4y5r3zarvary0c5xw7k8z4kv --amount 10

# Mobile
1. Open wallet
2. Tap "Send"
3. Scan QR code or paste address
4. Enter amount
5. Review transaction
6. Confirm with PIN/biometric

# Cost
- Gas fee: ~0.001 DBP (varies)
- Confirmation: 1-5 seconds
```

---

## Community Questions

### Where can I get help?

- **Discord**: https://discord.gg/dbp (most active)
- **Telegram**: https://t.me/dbpnetwork
- **Reddit**: r/DBPNetwork
- **Twitter**: @DBPNetwork
- **Email**: support@bdp.network

### How can I stay updated?

- **Twitter**: Daily updates, announcements
- **Discord**: Community discussions
- **Blog**: Technical posts, roadmap updates
- **GitHub**: Code commits, releases
- **Newsletter**: Weekly digest (optional)

### Is there a bounty program?

Yes! Multiple programs:

**Bug Bounty**:
- Critical: $10,000 - $100,000
- High: $5,000 - $10,000
- Medium: $1,000 - $5,000
- Low: $100 - $1,000

**Content Bounty**:
- Tutorial: $100 - $500
- Video: $200 - $1,000
- Translation: $50 - $200
- Meme: $10 - $50 (yes, really)

**Development Bounty**:
- DApp: $1,000 - $10,000
- Tool: $500 - $5,000
- Integration: $200 - $2,000

### Can I propose features?

Absolutely! Process:
1. **Discuss**: Discord or GitHub Discussions
2. **Draft**: Write proposal
3. **Submit**: GitHub issue or DIP (DBP Improvement Proposal)
4. **Review**: Community + core team feedback
5. **Vote**: On-chain governance (future)
6. **Implement**: If approved

### How is DBP governed?

**Current** (Early Stage):
- Core team makes decisions
- Community input via Discord/GitHub
- Transparency in decision-making

**Future** (Post-Launch):
- On-chain governance (DAO)
- Token holders vote on proposals
- Decentralized decision-making
- Community treasury management

---

## Comparison Questions

### DBP vs Kaspa?

**Similarities**:
- GHOSTDAG consensus
- kHeavyHash mining
- High throughput
- Fair launch

**Differences**:
- DBP has smart contracts (Kaspa doesn't)
- DBP has dual algorithms (Kaspa only kHeavyHash)
- DBP has EVM (Kaspa custom)
- Kaspa is more battle-tested

**Relationship**: DBP builds on Kaspa's foundation, doesn't compete.

### DBP vs Ethereum?

**Similarities**:
- EVM compatibility
- Smart contracts
- DeFi/NFT support
- Developer tools

**Differences**:
- DBP uses DAG (Ethereum linear chain)
- DBP is PoW (Ethereum is PoS)
- DBP is faster (1s blocks vs 12s)
- Ethereum has larger ecosystem

**Positioning**: "Ethereum speed, 100x faster"

### DBP vs Hedera?

**Similarities**:
- DAG structure
- Fast transactions
- Smart contracts

**Differences**:
- DBP is decentralized (Hedera is council-controlled)
- DBP is open source (Hedera is patented)
- DBP is PoW (Hedera is PoS)
- DBP is permissionless (Hedera has node requirements)

**Target**: DBP for community, Hedera for enterprise

### DBP vs Avalanche?

**Similarities**:
- DAG-based consensus
- Fast finality
- Smart contracts
- High throughput

**Differences**:
- DBP is simpler (Avalanche complex)
- DBP is fair launch (Avalanche VC-backed)
- DBP is PoW (Avalanche is PoS)
- Avalanche has subnets (DBP single chain)

**Market**: Different segments (accessible vs enterprise)

---

## Future Questions

### What's the roadmap?

**Q1 2025** (Months 1-3):
- Testnet launch
- Open source repository
- Mining operational
- Community building

**Q2 2025** (Months 4-6):
- Smart contracts functional
- Dual algorithm mining
- Mobile wallet beta
- Security audits

**Q3 2025** (Months 7-9):
- Mainnet launch
- Exchange listings
- Developer grants
- Marketing push

**Q4 2025** (Months 10-12):
- Ecosystem growth
- DApp deployment
- Cross-chain bridges
- Governance

### Will DBP have Layer 2?

Yes, future plans include:
- **Payment Channels**: Instant micropayments
- **Sidechains**: Specialized chains
- **Rollups**: Ethereum-style scalability
- **State Channels**: Off-chain computation

Timeline: Year 2+

### Will DBP support other languages?

Smart contract languages:
- **Now**: Solidity
- **Future**: Vyper (Ethereum alternative)
- **Research**: Rust, Move, others

Node implementation:
- **Now**: Go
- **Future**: Rust (maybe)

### What about privacy features?

Future considerations:
- **Optional Privacy**: zk-SNARKs for private transactions
- **Mixing**: Built-in coin mixing
- **Confidential Contracts**: Private smart contracts

Not a priority for launch, but on roadmap.

### Will there be staking?

Possible hybrid PoW/PoS in future:
- **PoW**: Continue for security
- **PoS**: Add for governance
- **Hybrid**: Best of both worlds

Needs community discussion and research.

---

## Concerns & Criticisms

### "Isn't this just another BlockDAG clone?"

**No.** Key differences:
1. We're actually building (not just promising)
2. Open source (not closed and hidden)
3. Based on Kaspa (proven technology)
4. Fair launch (no presale scam)
5. Public team (not anonymous)

We're the **anti-BlockDAG**: doing what they failed to do.

### "How do I know this isn't a scam?"

Red flags for scams (BlockDAG has them all):
- ❌ Closed source
- ❌ Anonymous team
- ❌ Endless presale
- ❌ No working product
- ❌ Impossible promises
- ❌ No transparency

DBP does the opposite:
- ✅ Open source
- ✅ Public team
- ✅ No presale
- ✅ Working product (90 days)
- ✅ Realistic goals
- ✅ Complete transparency

### "Why should I believe you'll deliver?"

**Evidence**:
1. Working testnet (within 90 days)
2. Public code (audit anytime)
3. Realistic roadmap (not impossible promises)
4. Based on proven tech (Kaspa fork)
5. Transparency (no hiding)

**Accountability**:
- GitHub activity (visible progress)
- Community oversight (open discussions)
- No presale (can't run with money)

### "What if the team abandons the project?"

**Mitigations**:
1. **Open Source**: Anyone can fork and continue
2. **Decentralized**: Network runs without team
3. **Documentation**: Complete technical specs
4. **Community**: Can self-organize
5. **Fair Launch**: No team control over tokens

Even if team leaves, project can continue.

### "Isn't the roadmap too aggressive?"

**Perspective**:
- Kaspa took years to build from scratch
- We're forking Kaspa (head start)
- AI-assisted development (faster)
- Clear specifications (less uncertainty)
- Committed team (full-time)

**Risk Management**:
- If timeline slips, we communicate
- Better to ship late than ship broken
- Community input on priorities
- Flexible on non-critical features

---

## Getting Started

### I want to mine, where do I start?

1. **Join Discord**: https://discord.gg/dbp
2. **Read Mining Guide**: /docs/mining
3. **Get Hardware**: GPU or ASIC
4. **Download Software**: lolminer or bzminer
5. **Choose Pool**: Recommended pools list
6. **Start Mining**: Follow configuration guide
7. **Monitor**: Check pool dashboard

### I want to develop, where do I start?

1. **Read Docs**: Technical spec, architecture
2. **Join Developer Discord**: #developers channel
3. **Clone Repo**: `git clone https://github.com/dbp-project/dbp`
4. **Run Testnet Node**: Follow setup guide
5. **Deploy Contract**: Use Remix or Hardhat
6. **Get Grants**: Apply for development funding

### I want to invest, when can I buy?

**Current**: Cannot buy (no presale)

**After Launch** (Month 9+):
- Mine it (earn through mining)
- DEX (Uniswap, PancakeSwap)
- CEX (KuCoin, Gate.io later)

**Recommendation**: Join community now, mine after launch.

### I'm skeptical, how can I verify?

**Do Your Own Research**:
1. **Read Code**: GitHub repository (coming soon)
2. **Check Team**: LinkedIn profiles, history
3. **Test Testnet**: Run a node yourself
4. **Ask Questions**: Discord, Reddit, Twitter
5. **Compare**: Read competitive analysis
6. **Wait**: See if we deliver (90 days)

**Healthy Skepticism**: We encourage it! Don't trust, verify.

---

## Contact

- **Website**: https://bdp.network (coming soon)
- **GitHub**: https://github.com/dbp-project
- **Discord**: https://discord.gg/dbp
- **Twitter**: @DBPNetwork
- **Telegram**: https://t.me/dbpnetwork
- **Email**: hello@bdp.network

---

*Last Updated: [Date will be added]*

*Have a question not answered here? Ask in Discord or submit a GitHub issue!*
