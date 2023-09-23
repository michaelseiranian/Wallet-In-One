import React from 'react';
import { render, screen, fireEvent, act, within} from '@testing-library/react-native';
import LoginScreen from '../../screens/LoginScreen';


jest.mock('react', () => {
  const ActualReact = jest.requireActual('react')
  return {
    ...ActualReact,
    useContext: () => (ActualReact.useState({'signedIn': false})),
  }
})

var empty = {
  "username": [
      "This field is required."
  ],
  "password": [
      "This field is required."
  ],
}

var invalid = {
  "non_field_errors": [
      "Unable to log in with provided credentials."
  ]
}

var success = {
  "token": "123"
}

jest.mock('../../authentication', () => {
  return {
    login: jest.fn((username, password) => {
      if (!username && !password){
        return Promise.resolve({status:400,body: empty})
      }
      if (username == "john doe" && password == "password123"){
        return Promise.resolve({status:200,body: success})
      }
      else{
        return Promise.resolve({status:400,body: invalid})
      }
    })
}})

describe('<LoginScreen />', () => {
  it('nothing entered', async () => {

    var renderer = render(<LoginScreen />)

    await act( async () => {
      fireEvent.press(await screen.getByText('Log In'));
    });

    const errors = await screen.findAllByText("This field is required.");
    expect(errors.length).toBe(2);
  });

  it('wrong credentials ', async () => {

    var renderer = render(<LoginScreen />)

    await act( async () => {
      fireEvent.changeText(await screen.getByTestId('username'), 'wrongusername');
      fireEvent.changeText(await screen.getByTestId('password'), 'wrongpassword');

      fireEvent.press(await screen.getByText('Log In'));
    });
    

    const errors = await screen.findAllByText("Unable to log in with provided credentials.");
    expect(errors.length).toBe(1);
  });

  it('successful login ', async () => {

    var renderer = render(<LoginScreen />)

    await act( async () => {
      fireEvent.changeText(await screen.getByTestId('username'), 'john doe');
      fireEvent.changeText(await screen.getByTestId('password'), 'password123');

      fireEvent.press(await screen.getByText('Log In'));
    });
    
    const errors1 = await screen.queryAllByText("Unable to log in with provided credentials.");
    const errors2 = await screen.queryAllByText("This field is required.");

    expect(errors1).toEqual([])
    expect(errors2).toEqual([])
  });

  it('log in snapshot test', () => {
    const renderer = render(<LoginScreen />)
    expect(renderer).toMatchSnapshot();
  });
});
