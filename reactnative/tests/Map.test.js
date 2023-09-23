import React from 'react';
import Map from '../screens/stocks/Map';
import renderer from 'react-test-renderer';
import { render } from '@testing-library/react-native';

describe('<Map />', () => {
    it('map test regular values', () => {
        const map = renderer.create(<Map latitude={10} longitude={15}/>);
        expect(map).toMatchSnapshot();
      });

    it('map test marker', () => {
        const { getByTestId } = render(<Map latitude={37} longitude={50} />);
        expect(getByTestId("marker")).toBeDefined();
        expect((getByTestId("marker").props.coordinate.latitude)).toBe(37);
        expect((getByTestId("marker").props.coordinate.longitude)).toBe(50);
      });

    it('map test mapView', () => {
        const { getByTestId } = render(<Map latitude={37} longitude={50} />);
        expect((getByTestId("mapView").props.region.latitude)).toBe(37);
        expect((getByTestId("mapView").props.region.longitude)).toBe(50);
        expect((getByTestId("mapView").props.style.position)).toBe('absolute');
        expect(getByTestId("mapView")).toBeDefined();
      });

    it('map test negative values', () => {
        const map = renderer.create(<Map latitude={-10} longitude={-15}/>);
        expect(map).toMatchSnapshot();
      });
      
    it('map test zero values', () => {
        const map = renderer.create(<Map latitude={0} longitude={0}/>);
        expect(map).toMatchSnapshot();
      }); 
      
    it('map test null values returns null', () => {
        const map = renderer.create(<Map latitude={null} longitude={null}/>).toJSON();
        expect(map).toBeNull();
        expect(map).toMatchSnapshot();
      });
      
    it('map test no values returns null', () => {
        const map = renderer.create(<Map />).toJSON();
        expect(map).toBeNull();
        expect(map).toMatchSnapshot();
      });      
  });



