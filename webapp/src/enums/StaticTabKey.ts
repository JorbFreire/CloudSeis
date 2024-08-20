export enum StaticTabKey {
  Input = "tab-input",
  Output = "tab-output",
  Vizualizer = "tab-vizualizer",
}

export const isFixedTab = (tabId: StaticTabKey | number) =>
  tabId == StaticTabKey.Input || tabId == StaticTabKey.Output

export const isStaticTabKey = (tabId: StaticTabKey | number) => {
  if (typeof tabId === 'number') return false
  return Object.values(StaticTabKey).includes(tabId);
}
