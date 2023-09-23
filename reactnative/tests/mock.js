const { jest } = require('@jest/globals');

jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
jest.mock('@react-navigation/native', () => ({
    useIsFocused: jest.fn(),
  }));

  jest.mock('react-native-wagmi-charts/lib/commonjs/charts/line/utils', () => {
    return {
      ...jest.requireActual(
        'react-native-wagmi-charts/lib/commonjs/charts/line/utils',
      ),
      getDomain: jest.fn((rows) => {
        const values = rows.map(({value})=> value);
        return [Math.min(...values), Math.max(...values)];
      }),
      lineChartDataPropToArray: jest.fn((dataProp) => {
        if (!dataProp) {
          return [];
        }
  
        if (Array.isArray(dataProp)) {
          return dataProp;
        }
  
        const data = [];
  
        Object.values(dataProp).forEach((dataSet) => {
          if (dataSet) {
            data.push(...dataSet);
          }
        });
  
        return data;
      }),
    };
  });

  jest.mock('react-native-reanimated', () => require('react-native-reanimated/mock'));