import {it} from "@jest/globals";
import {fireEvent, render, screen} from "@testing-library/react-native";
import expect from "expect";
import * as React from 'react';
import MainStackNavigator from "../screens/Main Account/MainStackNavigator";
import {NavigationContainer} from "@react-navigation/native";

const mockNavigation = jest.fn();
jest.mock('@react-navigation/native', () => ({ ...jest.requireActual('@react-navigation/native'), useNavigation: () => { return mockNavigation; }, }));

it('renders correctly', async () => {
  const snapshot = render(<NavigationContainer><MainStackNavigator /></NavigationContainer>);
  expect(snapshot).toMatchSnapshot();
});