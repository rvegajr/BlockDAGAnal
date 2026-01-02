defmodule PhoenixNodeTest do
  use ExUnit.Case

  test "connects to Phoenix node via RPC" do
    assert {:ok, _} = PhoenixNode.rpc("eth_blockNumber")
  end

  test "indexes blocks from Phoenix node" do
    latest_block_number = PhoenixNode.latest_block_number()
    Indexer.fetch_and_import_range(latest_block_number, latest_block_number)
    assert latest_block_number == Explorer.Chain.block_height()
  end

  test "handles real-time block updates" do
    PhoenixNode.subscribe_to_new_blocks()
    latest_block_number = PhoenixNode.latest_block_number()
    :timer.sleep(1000) # wait for a new block
    assert Explorer.Chain.block_height() > latest_block_number
  end
end