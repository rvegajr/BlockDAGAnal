import { ContractFactory as EthersContractFactory } from '@ethersproject/contracts';
import { PhoenixProvider } from './providers/phoenix-provider';

export class ContractFactory extends EthersContractFactory {
  constructor(abi: any[], bytecode: string, signer?: PhoenixProvider) {
    super(abi, bytecode, signer);
  }
}