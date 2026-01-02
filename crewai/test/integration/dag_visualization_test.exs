defmodule DAGVisualizationTest do
  use ExUnit.Case
  use Wallaby.Feature

  feature "DAG visualization", %{
    session: session
  } do
    session
    |> visit("/dag")
    |> assert_has(Query.css(".dag-container"))

    session
    |> click(Query.css(".block-#{latest_block_number}"))
    |> assert_has(Query.css(".block-details-modal"))

    session
    |> execute_script("window.resizeTo(400, 800)")
    |> assert_has(Query.css(".mobile-dag-view"))
  end  
end