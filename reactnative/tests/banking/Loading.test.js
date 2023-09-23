import React from 'react';
import renderer from 'react-test-renderer';
import Loading from '../../screens/banking/Loading'

describe('<HomePage />', () => {
    it('snapshot test', () => {
        const snapshot = renderer.create(<Loading />);
        expect(snapshot).toMatchSnapshot();         
      });
  });