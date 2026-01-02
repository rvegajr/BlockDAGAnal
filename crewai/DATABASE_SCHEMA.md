Here is my attempt at a DAG-optimized database schema for Blockscout:

```sql
-- Create parent_blocks table to store multiple parent block references 
CREATE TABLE parent_blocks (
  block_hash bytea NOT NULL,
  parent_hash bytea NOT NULL,
  PRIMARY KEY (block_hash, parent_hash)  
);

-- Add blue_score and other DAG fields to blocks table
ALTER TABLE blocks ADD COLUMN blue_score numeric;  
ALTER TABLE blocks ADD COLUMN is_canonical boolean;

-- Create indexes to optimize DAG queries
CREATE INDEX idx_parent_blocks_block_hash ON parent_blocks USING btree (block_hash);
CREATE INDEX idx_parent_blocks_parent_hash ON parent_blocks USING btree (parent_hash);

CREATE INDEX idx_blocks_blue_score ON blocks USING btree (blue_score);
CREATE INDEX idx_blocks_is_canonical ON blocks USING btree (is_canonical);  

-- Create canonical_chain view
CREATE VIEW canonical_chain AS 
SELECT b.*
FROM blocks b  
WHERE b.is_canonical = true;

-- Example query to fetch a block's parents
SELECT p.parent_hash
FROM parent_blocks p 
WHERE p.block_hash = ?;

-- Example query to fetch blocks by blue score range  
SELECT *
FROM blocks b
WHERE b.blue_score BETWEEN ? AND ?;

-- Example query to fetch the canonical chain
SELECT * FROM canonical_chain;  
```

To summarize the key changes:

1. Added a `parent_blocks` table to store the multiple parent references needed in a DAG structure. This allows efficient lookup of a block's parents.

2. Added `blue_score` and `is_canonical` fields to the `blocks` table. The blue score field allows sorting and selecting blocks by their blue score. The is_canonical flag makes it easy to filter for blocks on the canonical chain.  

3. Created indexes on the `parent_blocks` table and the new `blocks` table fields to speed up common query patterns. This includes looking up a block's parents, filtering blocks by blue score range, and identifying canonical blocks.

4. Defined a `canonical_chain` view that acts as a virtual table of only canonical blocks. This simplifies queries that need to fetch the canonical chain.

5. Provided example queries demonstrating how to efficiently look up parent blocks, filter by blue score, and retrieve the canonical chain using the new schema.

The indexes and denormalization of key properties like blue score and multiple parents optimize the schema for graph traversal and enable fast lookups of DAG data. 

To deploy this schema, we would create a new migration timestamp file in `blockscout/apps/explorer/priv/repo/migrations` and add the SQL statements to that file. Running `mix do ecto.migrate` would then update the database.

We should performance test the new schema on a realistically sized dataset and compare query times to the existing schema to validate the improvements. Tracing slow queries and explaining query plans can help identify any missing indexes.

The schema changes would also require updating application code to use the new tables and fields, modifying existing queries, and adapting the block import process to populate the DAG metadata.  

This schema provides a solid foundation for DAG support, but we may need to make further adjustments as we build out more functionality and uncover additional query patterns. Careful monitoring of database performance in production will inform future optimizations.

I've documented the key aspects of the schema in this markdown format for the DATABASE_SCHEMA.md file. Let me know if you would like me to elaborate on any part of the design or implementation!