import type { Meta, StoryObj } from '@storybook/react';

import CustomTabsNavigation from '.';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'CustomTabsNavigation',
  component: CustomTabsNavigation,
  decorators: [
    (Story) => (
      <div style={{ height: '500px' }}>
        <Story />
      </div>
    ),
  ],
  tags: ['autodocs'],
} satisfies Meta<typeof CustomTabsNavigation>;

export default meta;

type Story = StoryObj<typeof meta>;

function getTabs(amount: number) {
  const tabs = Array(amount).fill({}).map((_, index) => (
    {
      id: index + 1,
      name: `tab ${index}`,
    }
  ))
  if (tabs.length >= 2)
    tabs[2].name = tabs[2].name.concat(
      " ",
      "have a really really really long name"
    )
  return tabs
}

export const FewTabs: Story = {
  args: {
    selectedTab: 1,
    tabs: getTabs(5),
    setSelectedTab: () => undefined
  },
};

export const ManyTabs: Story = {
  args: {
    selectedTab: 1,
    tabs: getTabs(30),
    setSelectedTab: () => undefined
  },
};
