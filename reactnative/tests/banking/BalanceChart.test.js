import React from 'react';
import renderer from 'react-test-renderer';
import { BalanceChart } from '../../screens/banking/BalanceChart'

describe('<BalanceChart />', () => {
    it('BalanceChart test', () => {
        var balance_history = {
            "2023-02-15": 100.0,
            "2023-02-01": 150.0,
            "2023-01-15": 50.0,
            "2023-01-01": 100.0,
            "2022-12-15": -200.0,
            "2022-12-01": -150.0
        }

        const snapshot = renderer.create(<BalanceChart rawData={balance_history} highest={150.0}/>);
        expect(snapshot).toMatchSnapshot();         
      });
  });
