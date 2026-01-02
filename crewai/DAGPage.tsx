import React, { useEffect, useState } from 'react';
import { gql, useQuery } from '@apollo/client';
import DAGVisualization from './DAGVisualization';

const GET_BLOCKS = gql`
  query GetBlocks($limit: Int!, $offset: Int!) {
    blocks(limit: $limit, offset: $offset) {
      items {
        hash
        parentHashes
        blueScore
        isCanonical
      }
    }
  }
`;

const DAGPage: React.FC = () => {
  const [blocks, setBlocks] = useState([]);
  const { loading, error, data } = useQuery(GET_BLOCKS, {
    variables: { limit: 100, offset: 0 },
  });

  useEffect(() => {
    if (!loading && !error && data) {
      setBlocks(data.blocks.items);
    }
  }, [loading, error, data]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <div>
      <h2>DAG Visualization</h2>
      <DAGVisualization blocks={blocks} />
    </div>
  );
};

export default DAGPage;
