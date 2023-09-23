import {it} from "@jest/globals";
import {render} from "@testing-library/react-native";
import App from "../App";
import expect from "expect";
import * as React from 'react';

const mockNavigation = jest.fn();
jest.mock('@react-navigation/native', () => ({ ...jest.requireActual('@react-navigation/native'), useNavigation: () => { return mockNavigation; }, }));

it('renders correctly', () => {
  const snapshot = render(<App />);
  expect(snapshot).toMatchSnapshot();
});