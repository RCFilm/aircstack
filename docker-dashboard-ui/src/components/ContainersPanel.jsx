import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
export default function ContainersPanel() {
  const [data, setData] = useState([]);
  useEffect(() => {
    api.get('/containers').then(res => setData(res.data));
  }, []);

  function handleDragEnd(result) {
    if (!result.destination) return;
    const items = Array.from(data);
    const [moved] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, moved);
    setData(items);
  }
  return (
    <div>
      <h2>Containers</h2>
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="containers">
          {(provided) => (
            <table ref={provided.innerRef} {...provided.droppableProps}>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Image</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {data.map((row, index) => (
                  <Draggable draggableId={row.name} index={index} key={row.name}>
                    {(drag) => (
                      <tr ref={drag.innerRef} {...drag.draggableProps} {...drag.dragHandleProps}>
                        <td>{row.name}</td>
                        <td>{row.image}</td>
                        <td>{row.status}</td>
                      </tr>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </tbody>
            </table>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
}
