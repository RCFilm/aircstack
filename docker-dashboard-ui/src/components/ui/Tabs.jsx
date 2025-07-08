import React from 'react';
export function Tabs({ defaultValue, children }) {
  const [value, setValue] = React.useState(defaultValue);
  const triggers = [];
  const contents = [];
  React.Children.forEach(children, (child) => {
    if (child.type.name === 'TabsList') triggers.push(child);
    else contents.push(React.cloneElement(child, { value, setValue }));
  });
  return <div>{triggers}{contents}</div>;
}
export function TabsList({ children }) { return <nav>{children}</nav>; }
export function TabsTrigger({ value, children, setValue }) {
  return <button onClick={() => setValue(value)}>{children}</button>;
}
export function TabsContent({ value, setValue, children }) {
  return value === value ? <section>{children}</section> : null;
}
