import React from 'react';
import ExchangeTransactions from '../../screens/cryptoExchanges/ExchangeTransactions';
import {render, fireEvent, waitFor, act, screen} from '@testing-library/react-native';
import {describe, it, test} from "@jest/globals";
import expect from "expect";

jest.mock('expo-secure-store');
jest.mock('../../screens/cryptocurrency/icons/icon');

describe('ExchangeTransactions', () => {
  const props = {
    route: {
      params: {
        item: {
          id: 1,
          crypto_exchange_name: 'Test Exchange',
        },
        removeExchange: jest.fn(),
      },
    },
    navigation: {
      goBack: jest.fn(),
    },
  };

  beforeEach(() => {
    global.fetch = jest.fn();
  })

  afterEach(() => {
    global.fetch.mockClear();
    delete global.fetch;
  })

  it('renders correctly', () => {
    const { toJSON } = render(<ExchangeTransactions {...props} />);
    expect(toJSON()).toMatchSnapshot();
  });


  const createTestProps = (props) => ({
    navigation: {
      goBack: jest.fn(),
    },
    route: {
      params: {
        item: {
          id: '1',
          crypto_exchange_name: 'Example Exchange',
        },
        removeExchange: jest.fn(),
      },
    },
    ...props,
  });

  test('renders ExchangeTransactions screen correctly', () => {
    const props = createTestProps();
    const { getByTestId, getByText } = render(<ExchangeTransactions {...props} />);

    expect(getByTestId('exchange-image')).toBeDefined();
    expect(getByText('Example Exchange Exchange')).toBeDefined();
    expect(getByText('Balance: Loading...')).toBeDefined();
  });

  test('remove button opens confirmation modal', async () => {
    const props = createTestProps();
    const { getByText, getByTestId } = render(<ExchangeTransactions {...props} />);

    fireEvent.press(getByText('Remove'));
    await waitFor(() => getByTestId('conditional-modal'));

    expect(getByTestId('conditional-modal')).toBeDefined();

    act(async () => {
      fireEvent.press(getByText('No'));
    })

  });

  test('switch selector opens transactions', async () => {
    const props = createTestProps();
    const { getByText, getByTestId } = render(<ExchangeTransactions {...props} />);

    fireEvent.press(getByText('Transactions'));
    await waitFor(() => {
      expect(screen.getByText('Pair')).toBeDefined()
    });

  });

  test('switch selector works correctly', async () => {
    const props = createTestProps();
    const { getByText, getByTestId } = render(<ExchangeTransactions {...props} />);

    fireEvent.press(getByText('Transactions'));
    await waitFor(() => getByTestId('switchSelector'));

    expect(getByText('Coin Breakdown')).toBeDefined();
    expect(getByTestId('transactionTitle')).toBeDefined();
  });

  const mockTransactionData = [
    {
      "crypto_exchange_object": 8,
      "asset": "BTCUSDT",
      "transaction_type": "sell",
      "amount": 0.01633,
      "timestamp": "2021-02-07T15:36:10.777000Z"
    },
    {
      "crypto_exchange_object": 8,
      "asset": "ADAUSDT",
      "transaction_type": "buy",
      "amount": 243.7,
      "timestamp": "2021-04-26T14:39:17.825000Z"
    }]

  const mockTokenData = {
    "balance": 44.54,
    "token_data": [
      {
        "x": "BNB: £0.0",
        "y": 0.0
      },
      {
        "x": "ADA: £0.0",
        "y": 0.0
      }]}

  const mockEmptyTransactionData = ["empty"]

  const mockEmptyTokenData = {
    "balance": 0,
    "token_data": ["empty"]
  }

  test('API calls are made and data is rendered correctly', async () => {
    global.fetch = jest.fn((url, options) => {
      console.log(url)
      if (url.includes('/crypto-exchanges/get_transactions/1/')) {
        return Promise.resolve({
          json: () => Promise.resolve(mockTransactionData),
        });
      } else if (url.includes('/crypto-exchanges/get_token_breakdown/1/')) {
        return Promise.resolve({
          json: () => Promise.resolve(mockTokenData),
        });
      } else {
        return Promise.reject(new Error('Invalid API call'));
      }
    });

    const {getByText, getByTestId} = render(<ExchangeTransactions {...props} />);

    act(async () => {
      fireEvent.press(await screen.getByText('Transactions'));
    });
  });

  test('API calls are made and empty data is rendered correctly', async () => {
    global.fetch = jest.fn((url, options) => {
      console.log(url)
      if (url.includes('/crypto-exchanges/get_transactions/1/')) {
        return Promise.resolve({
          json: () => Promise.resolve(mockEmptyTransactionData),
        });
      } else if (url.includes('/crypto-exchanges/get_token_breakdown/1/')) {
        return Promise.resolve({
          json: () => Promise.resolve(mockEmptyTokenData),
        });
      } else {
        return Promise.reject(new Error('Invalid API call'));
      }
    });

    render(<ExchangeTransactions {...props} />);

    await act(async () => {
      fireEvent.press(await screen.getByText('Transactions'));
    });
  });

  test('API calls are made and errors are thrown', async () => {
    act(() => {
      global.fetch = jest.fn((url, options) => {
        if (url.includes('/crypto-exchanges/get_transactions/1/')) {
          return Promise.reject({
            json: () => Promise.reject(mockTransactionData),
          });
        } else if (url.includes('/crypto-exchanges/get_token_breakdown/1/')) {
          return Promise.reject({json: () => Promise.reject(mockTokenData)});
        }
      });
     global.fetch.mockClear();
    });
  });

  test('remove exchange breaks expectedly', async () => {

    const props = createTestProps();
    const {getByText, getByTestId} = render(<ExchangeTransactions {...props} />);

    fireEvent.press(getByText('Remove'));
    await waitFor(() => getByTestId('conditional-modal'));

    try {
      fireEvent.press(getByText('Yes'));
    } catch (error) {
      expect(error.message).toBe("Cannot read properties of undefined (reading 'then')");
    }
  });
});