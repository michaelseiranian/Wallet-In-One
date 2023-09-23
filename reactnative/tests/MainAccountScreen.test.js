import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react-native';
import MainAccountPage from '../screens/Main Account/MainAccountPage';

describe('<MainAccountPage />', () => {
    it('mainAccountPage snapshot test', () => {
        const mainAccountPage = render(<MainAccountPage/>);
        expect(mainAccountPage).toMatchSnapshot();
    }
    )

    it('mainAccountPage banking button test', () => {
        const navigate = jest.fn();
        const mainAccountPage = render(<MainAccountPage navigation={ {navigate} }/>);
        fireEvent.press(screen.getByText('Bank Accounts'));
        expect(navigate).toHaveBeenCalledWith('Bank Accounts');
        expect(mainAccountPage).toMatchSnapshot();
    }
    )

    it('mainAccountPage cryptocurrency button test', () => {
        const navigate = jest.fn();
        const mainAccountPage = render(<MainAccountPage navigation={ {navigate} }/>);
        fireEvent.press(screen.getByText('Cryptocurrency'));
        expect(navigate).toHaveBeenCalledWith('Crypto Wallets & Exchanges');
        expect(mainAccountPage).toMatchSnapshot();
    }
    )

    it('mainAccountPage stocks button test', () => {
        const navigate = jest.fn();
        const mainAccountPage = render(<MainAccountPage navigation={ {navigate} }/>);
        fireEvent.press(screen.getByText('Stock Accounts'));
        expect(navigate).toHaveBeenCalledWith('Stock Account List');
        expect(mainAccountPage).toMatchSnapshot();
    }
    )
})