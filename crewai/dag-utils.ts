export function traverseDAG(blockHash: string): Block[] {
  // Traverse the DAG starting from the given block hash
  // Return an array of blocks in the traversal order
}

export function isBlueBlock(block: Block): boolean {
  // Check if the given block is a blue block
  // Blue blocks contribute to the main chain  
}

export function isRedBlock(block: Block): boolean {
  // Check if the given block is a red block
  // Red blocks are off the main chain
}

export function getConfirmations(blockHash: string): number {
  // Get the number of confirmations for a block
  // In Phoenix, this is the number of blue blocks built on top
}