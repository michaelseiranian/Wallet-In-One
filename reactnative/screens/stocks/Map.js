import MapView from 'react-native-maps';
import { Marker } from 'react-native-maps';
import { StyleSheet } from 'react-native';

/**
 * Component that takes in a latitude and longitude and displays a map with a marker at the specified location
 */
export default function Map({latitude, longitude}){
  if(latitude && longitude){
    return(
        <MapView
        style={{...StyleSheet.absoluteFillObject}}
        region={{
          latitude: latitude,
          longitude: longitude,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421,
        }}
        testID={"mapView"}
      >
    <Marker coordinate={{ latitude: latitude, longitude: longitude }} testID={"marker"} />
      </MapView>
    )
  }
  else{
    return null;
  }
}