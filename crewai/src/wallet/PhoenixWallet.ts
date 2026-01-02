import { Wallet, HDNode } from '@ethersproject/wallet';
import { ExternallyOwnedAccount } from '@ethersproject/abstract-signer';
import { Mnemonic } from '@ethersproject/hdnode';
import { randomBytes } from '@ethersproject/random';
import { serialize, deserialize } from '@ethersproject/json-wallets';
import { encrypt, decrypt } from '@ethersproject/json-wallets';
import { computeAddress } from '@ethersproject/transactions';
import { getAddress } from '@ethersproject/address';
import { PhoenixProvider } from '../providers/phoenix-provider';

export class PhoenixWallet extends Wallet {
  private hdNode: HDNode;
  private mnemonic: Mnemonic;
  private accounts: ExternallyOwnedAccount[] = [];

  constructor(privateKey?: string, provider?: PhoenixProvider) {
    super(privateKey, provider);
  }

  static createRandom(provider?: PhoenixProvider): PhoenixWallet {
    const entropy = randomBytes(16);
    const mnemonic = Mnemonic.entropyToMnemonic(entropy);
    return PhoenixWallet.fromMnemonic(mnemonic, provider);
  }

  static fromMnemonic(mnemonic: string, provider?: PhoenixProvider): PhoenixWallet {
    const hdNode = HDNode.fromMnemonic(mnemonic);
    const wallet = new PhoenixWallet(hdNode.privateKey, provider);
    wallet.mnemonic = Mnemonic.fromEntropy(hdNode.privateKey);
    wallet.hdNode = hdNode;
    return wallet;
  }

  addAccount(index: number = 0): ExternallyOwnedAccount {
    const derivationPath = `m/44'/60'/${index}'/0/0`;
    const hdNode = this.hdNode.derivePath(derivationPath);
    const account = new ExternallyOwnedAccount(hdNode.privateKey, this.provider);
    this.accounts.push(account);
    return account;
  }

  getAccounts(): ExternallyOwnedAccount[] {
    return this.accounts;
  }

  async signTransaction(transaction: any): Promise<string> {
    const account = this.accounts[0];
    const signedTx = await account.signTransaction(transaction);
    return signedTx;
  }

  async getAddress(): Promise<string> {
    const account = this.accounts[0];
    return account.getAddress();
  }

  encrypt(password: string): Promise<string> {
    return encrypt(this.privateKey, password);
  }

  static decrypt(json: string, password: string, provider?: PhoenixProvider): Promise<PhoenixWallet> {
    return decrypt(json, password).then((wallet) => {
      return new PhoenixWallet(wallet.privateKey, provider);
    });
  }

  getPrivateKey(): string {
    return this.privateKey;
  }

  getMnemonic(): string {
    return this.mnemonic.phrase;
  }
}