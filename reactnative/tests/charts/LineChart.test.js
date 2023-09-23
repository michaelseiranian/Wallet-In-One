import React from 'react';
import LineChartScreen from '../../screens/charts/LineChart';
import renderer from 'react-test-renderer';

describe('<LineChartScreen />', () => {
    it('test line chart 4', () => {
        const lineChart = renderer.create(<LineChartScreen graph_version={4} height={10} width={100} current_balance={10} data={[{"timestamp": 1675814400000, "value": 2900.6002}, {"timestamp": 1675814400000, "value": 2939.0458}, {"timestamp": 1678320000000, "value": 1223.7844}, {"timestamp": 1678406400000, "value": 227.7844}, {"timestamp": 1678406400000, "value": 266.23}]} />);
        expect(lineChart).toMatchSnapshot();         
      });

      it('test line chart 1', () => {
        const lineChart = renderer.create(<LineChartScreen graph_version={1} height={10} width={100} current_balance={10} data={[{"timestamp": 1675814400000, "value": 2900.6002}, {"timestamp": 1675814400000, "value": 2939.0458}, {"timestamp": 1678320000000, "value": 1223.7844}, {"timestamp": 1678406400000, "value": 227.7844}, {"timestamp": 1678406400000, "value": 266.23}]} />);
        expect(lineChart).toMatchSnapshot();         
      });

      it('test line chart 2', () => {
        const lineChart = renderer.create(<LineChartScreen graph_version={2} height={10} width={100} current_balance={10} data={[{"timestamp": 1675814400000, "value": 2900.6002}, {"timestamp": 1675814400000, "value": 2939.0458}, {"timestamp": 1678320000000, "value": 1223.7844}, {"timestamp": 1678406400000, "value": 227.7844}, {"timestamp": 1678406400000, "value": 266.23}]} />);
        expect(lineChart).toMatchSnapshot();         
      });
})