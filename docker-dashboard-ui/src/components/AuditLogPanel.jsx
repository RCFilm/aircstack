import React, { useEffect, useState } from 'react';
import { api } from '../api';
import Table from './ui/Table';
export default function AuditLogPanel() {
  const [data, setData] = useState([]);
  useEffect(() => {
    api.get('/auditlog').then(res => setData(res.data));
  }, []);
  return (
    <div>
      <h2>Audit Log</h2>
      <Table columns={['timestamp', 'user', 'action']} data={data} />
    </div>
  );
}
