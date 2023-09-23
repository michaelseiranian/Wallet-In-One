import React from 'react';
import renderer from 'react-test-renderer';
import AuthWebView from '../../screens/banking/AuthView'

describe('<AuthWebView />', () => {
    it('snapshot test', () => {
        const snapshot = renderer.create(<AuthWebView />);
        expect(snapshot).toMatchSnapshot();         
      });
  });