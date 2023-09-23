import React from 'react';
import renderer from 'react-test-renderer';
import { BankBarChart } from '../../screens/banking/BankBarChart'

describe('<BankBarChart />', () => {
    it('snapshot test', () => {
        var fixture = {
            "labels": [
                "December",
                "January",
                "February"
            ],
            "values": [
                50.0,
                250.0,
                50.0
            ],
            "data": {
                "2023-02-01": 50.0,
                "2023-01-01": 250.0,
                "2022-12-01": 50.0
            }
        }

        const snapshot = renderer.create(<BankBarChart rawData = {fixture} tab={1} />);
        expect(snapshot).toMatchSnapshot();         
      });
  });
  describe('<BankBarChart /> 2' , () => {
    it('snapshot test', () => {
        var fixture = {
            "labels": [
                "December",
                "January",
                "February"
            ],
            "values": [
                50.0,
                250.0,
                50.0
            ],
            "data": {
                "2023-02-01": 50.0,
                "2023-01-01": 250.0,
                "2022-12-01": 50.0
            }
        }

        const snapshot = renderer.create(<BankBarChart rawData = {fixture} tab={2} />);
        expect(snapshot).toMatchSnapshot();         
      });
  });

  describe('<BankBarChart /> 3' , () => {
    it('snapshot test', () => {
        var fixture = {
            "labels": [
                "December",
                "January",
                "February"
            ],
            "values": [
                50.0,
                250.0,
                50.0
            ],
            "data": {
                "2023-02-01": 50.0,
                "2023-01-01": 250.0,
                "2022-12-01": 50.0
            }
        }

        const snapshot = renderer.create(<BankBarChart rawData = {fixture} tab={3} />);
        expect(snapshot).toMatchSnapshot();         
      });
  });