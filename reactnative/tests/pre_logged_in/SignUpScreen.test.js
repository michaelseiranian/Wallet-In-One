import React from 'react';
import { render, screen, fireEvent, act, within} from '@testing-library/react-native';
import SignUpScreen from '../../screens/pre_logged_in/SignUpScreen';


jest.mock('react', () => {
  const ActualReact = jest.requireActual('react')
  return {
    ...ActualReact,
    useContext: () => (ActualReact.useState({'signedIn': false})),
  }
})

const fields = ['first_name', 'last_name', 'username', 'email', 'new_password']

global.fetch =  jest.fn( async (api, data ) => {

  // Adds errors if field are black
  var validation_errors = fields.reduce((acc, key) => {
    if (!data.body.hasOwnProperty(key)){ acc[key] = ['This field may not be blank.']};
    return acc;
  }, {});

  if (true){ 
    return Promise.resolve({  status: 400, json: () => Promise.resolve(validation_errors),})
  }
  else{
    return Promise.resolve({  status: 201, json: () => Promise.resolve({}),})
  }
})

const input = {
  'first_name': 'John',
  'last_name': 'Doe',
  'username': 'johndoe',
  'email': 'johndoe@example.com',
  'new_password': 'Test@123',
  'password_confirmation': 'Test@123'
}

describe('<SignUpScreen />', () => {
  it('nothing entered', async () => {

    var renderer = render(<SignUpScreen />)

    await act( async () => {
      fireEvent.press(await screen.getByText('Sign Up'));
    });

    const errors = await screen.findAllByText("This field may not be blank.");
    expect(errors.length).toBe(5);
  });

  it('successful log in', async () => {

    var renderer = render(<SignUpScreen />)
    for (i in input){
      fireEvent.changeText(await screen.getByTestId(i), input[i]);
    }

    await act( async () => {
      fireEvent.press(await screen.getByText('Sign Up'));
      const errors = await screen.queryAllByText("This field may not be blank.");
      expect(errors).toEqual([])
    });
  });

  it('sign up snapshot test', () => {
    const renderer = render(<SignUpScreen />)
    expect(renderer).toMatchSnapshot();
  });
});
