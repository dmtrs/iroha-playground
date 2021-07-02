import { html, directive } from 'lit-html';
import { styleMap } from 'lit-html/directives/style-map';

import 'carbon-web-components/es/components/link/link.js';

export interface DomainProps {
  /**
   * Is this the principal call to action on the page?  */
  primary?: boolean;
  /**
   * What background color to use
   */
  backgroundColor?: string;
  /**
   * How large should the button be?
   */
  size?: 'small' | 'medium' | 'large';
  /**
   * Button contents
   */
  uri: string;
  /**
   * Optional click handler
   */
  onClick?: () => void;
}
/**
 * Primary UI component for user interaction
 */
export const Domain = ({ primary, backgroundColor = null, size, uri, onClick }: ButtonProps) => {
  return html`
    <bx-link
      href=${uri}
    >
      ${uri}
    </bx-link>
  `;
};
