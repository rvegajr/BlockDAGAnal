import { TypeChain } from 'typechain';

export async function generateContractTypes(abis: any[], outDir: string) {
  const cwd = process.cwd();
  await TypeChain.generate({
    cwd,
    outDir,
    target: 'ethers-v5',
    abis,
  });
}