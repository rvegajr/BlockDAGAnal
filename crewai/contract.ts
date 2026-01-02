import { Contract as EthersContract } from '@ethersproject/contracts';
import { PhoenixProvider } from './providers/phoenix-provider';

export class Contract extends EthersContract {
  constructor(address: string, abi: any[], signer?: PhoenixProvider) {
    super(address, abi, signer);
  }

  // Add custom methods for Phoenix contracts here
}