import { Story, Meta } from '@storybook/web-components';
import { Domain, DomainProps } from './Domain';

export default {
  title: 'Playground/Domain',
  argTypes: {
    backgroundColor: { control: 'color' },
    onClick: { action: 'onClick' },
  },
} as Meta;

const Template: Story<Partial<DomainProps>> = (args) => Domain(args);

export const Primary = Template.bind({});
Primary.args = {
  primary: true,
  uri: '25e7bf6c2298726f4279',
};

export const Secondary = Template.bind({});
Secondary.args = {
  uri: '25e7bf6c2298726f4279',
};

export const Large = Template.bind({});
Large.args = {
  size: 'large',
  uri: '25e7bf6c2298726f4279',
};

export const Small = Template.bind({});
Small.args = {
  size: 'small',
  uri: '25e7bf6c2298726f4279',
};
