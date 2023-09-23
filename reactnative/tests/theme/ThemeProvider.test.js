import {it} from "@jest/globals";
import {render} from "@testing-library/react-native";
import {ThemeProvider} from "../../src/theme/ThemeProvider";
import expect from "expect";

it('renders correctly', () => {
  const snapshot = render(<ThemeProvider />);
  expect(snapshot).toMatchSnapshot();
});