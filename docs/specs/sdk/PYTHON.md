# BDP Python SDK Specification

Status: Draft
Owner: DevRel SDK Team

## Base
- web3.py wrapper with Phoenix extensions
- Package: blockdag-phoenix or bdp-sdk

## Installation
```bash
pip install blockdag-phoenix
```

## API
```python
from bdp import Web3

# Connect to Phoenix
w3 = Web3(Web3.HTTPProvider('https://rpc.bdp.network'))

# Standard web3.py API
balance = w3.eth.get_balance('0x...')
block = w3.eth.get_block('latest')

# Phoenix extensions
dag_info = w3.bdp.get_dag_info()  # returns {blueScore, parents, ...}
blue_score = w3.bdp.get_blue_score('latest')
```

## Features
- Full web3.py compatibility (v6+)
- Account/transaction signing
- Contract interaction (ABIs)
- Event filtering
- ENS support (if deployed)

## Phoenix Extensions Module
```python
class BDPModule:
    def get_dag_info(self, block_identifier='latest'):
        return self.web3.manager.request_blocking('bdp_getDAGInfo', [block_identifier])
    
    def get_blue_score(self, block_identifier='latest'):
        return self.web3.manager.request_blocking('bdp_getBlueScore', [block_identifier])
```

## Type Hints
- Full typing support with py.typed marker
- Compatible with mypy strict mode

## Testing
- pytest fixtures for Phoenix testnet
- Mock provider for unit tests

## Documentation
- Sphinx docs hosted on ReadTheDocs
- Jupyter notebook examples






