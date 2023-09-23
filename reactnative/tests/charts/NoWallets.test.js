// HomePage.test.js
import React from 'react';
import NoWallets from '../../screens/charts/chartComponents/noWallets';
import renderer from 'react-test-renderer';

describe('<NoWallets />', () => {
    it('snapshot test', () => {
        const snapshot = renderer.create(<NoWallets />);
        expect(snapshot).toMatchSnapshot();         
      });
  });