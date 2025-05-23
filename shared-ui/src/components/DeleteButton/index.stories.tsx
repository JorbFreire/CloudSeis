// DeleteButton.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import DeleteButton from './';

const meta: Meta<typeof DeleteButton> = {
  title: 'Components/DeleteButton',
  component: DeleteButton,
};

export default meta;

type Story = StoryObj<typeof DeleteButton>;

export const Default: Story = {
  args: {
    onClick: () => action('Clicked delete!'),
    size: 'large',
  },
  decorators: [
    (Story) => (
      <div style={{ padding: "0 64px" }}>
        <Story />
      </div>
    ),
  ],
};
