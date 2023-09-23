import { render, fireEvent } from '@testing-library/react-native';
import ExchangeAsset from '../../screens/cryptoExchanges/ExchangeAsset';
import renderer from 'react-test-renderer';

describe('ExchangeAsset component', () => {
    it('renders correctly', () => {
      const props = {
        item: { id: 1, crypto_exchange_name: 'Test Exchange' },
        balances: [],
        navigation: {
            navigate: jest.fn()
        }
      };  
      const tree = renderer.create(<ExchangeAsset {...props} />).toJSON();
      expect(tree).toMatchSnapshot();
    });
});

describe('<ExchangeAsset />', () => {
  test('renders correctly with minimum props', () => {
    const props = {
      item: { id: 1, crypto_exchange_name: 'Test Exchange' },
      balances: [],
      navigation: {
        navigate: jest.fn()
      }
    };
    const { getByText, getByTestId } = render(<ExchangeAsset {...props} />);
    
    expect(getByTestId('exchangeAsset')).toBeDefined();
    expect(getByText('Test Exchange')).toBeDefined();
    expect(getByText('Total Balance: £Loading...')).toBeDefined();
  });
});

describe('<ExchangeAsset />', () => {
    test('displays total balance when provided with balances', () => {
      const props = {
        item: { id: 1, crypto_exchange_name: 'Test Exchange' },
        balances: [{ id: 1, x: '2023-03-19T09:00:00.000Z', y: 123.45 }],
        navigation: {
          navigate: jest.fn()
        }
      };
      const { getByText } = render(<ExchangeAsset {...props} />);
      
      expect(getByText('Total Balance: £123.45')).toBeDefined();
    });
  });

describe('<ExchangeAsset />', () => {
  test('navigates to "ExchangeTransactions" screen on press', () => {
    const props = {
      item: { id: 1, crypto_exchange_name: 'Test Exchange' },
      balances: [],
      removeExchange: jest.fn(),
      navigation: {
        navigate: jest.fn()
      }
    };
    const { getByTestId } = render(<ExchangeAsset {...props} />);
    const exchangeAsset = getByTestId('exchangeAsset');
    fireEvent.press(exchangeAsset);
    
    expect(props.navigation.navigate).toHaveBeenCalledWith('ExchangeTransactions', {
      item: props.item,
      removeExchange: props.removeExchange
    });
  });
});