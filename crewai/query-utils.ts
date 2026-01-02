export function getUTXOs(address: string): UTXO[] {
  // Get the list of unspent transaction outputs for an address
}

export function getMempoolTransactions(): Transaction[] {
  // Get the list of transactions currently in the mempool
}  

export function getNetworkStats(): NetworkStats {
  // Get key network statistics 
  // E.g. number of nodes, transactions per second, gas price
}