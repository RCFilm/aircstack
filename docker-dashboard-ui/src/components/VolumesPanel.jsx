import React, { useEffect, useState } from 'react';
import { api } from '../api';
import Table from './ui/Table';
export default function VolumesPanel() {
  const [data, setData] = useState([]);
  useEffect(() => {
    api.get('/volumes').then(res => setData(res.data.map(name => ({ name }))));
  }, []);
  return (
    <div>
      <h2>Volumes</h2>
      <Table columns={['name']} data={data} />
    </div>
  );
}
