import { Contract } from './contract';

export class ERC1155 extends Contract {
  constructor(address: string, signer?: PhoenixProvider) {
    super(address, ERC1155_ABI, signer);
  }

  async balanceOf(account: string, id: BigNumberish): Promise<BigNumber> {
    return this.functions.balanceOf(account, id);
  }

  async balanceOfBatch(accounts: string[], ids: BigNumberish[]): Promise<BigNumber[]> {
    return this.functions.balanceOfBatch(accounts, ids);
  }

  async setApprovalForAll(operator: string, approved: boolean): Promise<TransactionResponse> {
    return this.functions.setApprovalForAll(operator, approved);
  }

  async isApprovedForAll(account: string, operator: string): Promise<boolean> {
    return this.functions.isApprovedForAll(account, operator);
  }

  async safeTransferFrom(
    from: string,
    to: string,
    id: BigNumberish,
    amount: BigNumberish,
    data: BytesLike
  ): Promise<TransactionResponse> {
    return this.functions.safeTransferFrom(from, to, id, amount, data);
  }

  async safeBatchTransferFrom(
    from: string,
    to: string,
    ids: BigNumberish[],
    amounts: BigNumberish[],
    data: BytesLike
  ): Promise<TransactionResponse> {
    return this.functions.safeBatchTransferFrom(from, to, ids, amounts, data);
  }
}

const ERC1155_ABI = [
  {
    "constant": true,
    "inputs": [
      {
        "name": "_owner",
        "type": "address"
      },
      {
        "name": "_id",
        "type": "uint256"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_owners",
        "type": "address[]"
      },
      {
        "name": "_ids",
        "type": "uint256[]"
      }
    ],
    "name": "balanceOfBatch",
    "outputs": [
      {
        "name": "",
        "type": "uint256[]"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_operator",
        "type": "address"
      },
      {
        "name": "_approved",
        "type": "bool"
      }
    ],
    "name": "setApprovalForAll",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_owner",
        "type": "address"
      },
      {
        "name": "_operator",
        "type": "address"
      }
    ],
    "name": "isApprovedForAll",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_from",
        "type": "address"
      },
      {
        "name": "_to",
        "type": "address"
      },
      {
        "name": "_id",
        "type": "uint256"
      },
      {
        "name": "_value",
        "type": "uint256"
      },
      {
        "name": "_data",
        "type": "bytes"
      }
    ],
    "name": "safeTransferFrom",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_from",
        "type": "address"
      },
      {
        "name": "_to",
        "type": "address"
      },
      {
        "name": "_ids",
        "type": "uint256[]"
      },
      {
        "name": "_values",
        "type": "uint256[]"
      },
      {
        "name": "_data",
        "type": "bytes"
      }
    ],
    "name": "safeBatchTransferFrom",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
];