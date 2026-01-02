defmodule APITest do
  use ExUnit.Case
  use Phoenix.ConnTest

  @endpoint BlockScoutWeb.Endpoint

  describe "GET /api/v1/blocks" do
    test "returns latest blocks" do
      latest_block_number = Explorer.Chain.block_height()
      
      conn = get(build_conn(), "/api/v1/blocks")
      response = json_response(conn, 200)
      
      assert length(response["items"]) > 0
      assert Enum.at(response["items"], 0)["number"] == latest_block_number
    end
  end

  describe "GET /api/v1/blocks/:number" do
    test "returns block details" do
      block = insert(:block)

      conn = get(build_conn(), "/api/v1/blocks/#{block.number}")
      response = json_response(conn, 200)

      assert response["number"] == block.number
    end

    test "returns error when block not found" do
      conn = get(build_conn(), "/api/v1/blocks/9999999999")
      response = json_response(conn, 404)

      assert response["message"] == "Block not found"
    end
  end
end