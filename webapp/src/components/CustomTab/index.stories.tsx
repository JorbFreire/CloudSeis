import type { Meta, StoryObj } from '@storybook/react';

import CustomTab from '.';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'CustomTab',
  component: CustomTab,
  decorators: [
    (Story) => (
      <div style={{ height: '500px' }}>
        <Story />
      </div>
    ),
  ],
  tags: ['autodocs'],
} satisfies Meta<typeof CustomTab>;

export default meta;

type Story = StoryObj<typeof meta>;

export const FewTabs: Story = {
  args: {
    value: 1,
    label: "Tab title",
    $color: 'primary',
    $orientation: 'horizontal'
  },
};
