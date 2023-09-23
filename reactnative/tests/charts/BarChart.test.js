import React from 'react';
import BarChart from '../../screens/charts/chartComponents/barChart';
import renderer from 'react-test-renderer';
import { StyleSheet } from 'react-native';

var data = {
    "all": [
        {
          "x": "Credit Card",
          "y": 200
        },
        {
          "x": "Cryptocurrency",
          "y": 50
        },
        {
          "x": "Stocks",
          "y": 75
        },
        {
          "x": "Debit Card",
          "y": 20
        }
    ]
  }

  var floatData = {
    "all": [
        {
          "x": "Credit Card",
          "y": 200.50
        },
        {
          "x": "Cryptocurrency",
          "y": 50.39
        },
        {
          "x": "Stocks",
          "y": 75.27
        },
        {
          "x": "Debit Card",
          "y": 20.21
        }
    ]
  }

var emptyData = {"all": []}
const emptyArray = Object.values(emptyData)[0]
const array = Object.values(data)[0]
const floatArray = Object.values(floatData)[0]
var colours = ["pink", "turquoise", "lime", "#FA991C"];
const handlePressIn = (event, datapoint)=>{console.log(datapoint)};
const list = array.map((val) => val.x);
const floatList = floatArray.map((val) => val.x);
const colors = { text: 'black' };

describe('<BarChart />', () => {
    it('test bar chart', () => {
        const barChart = renderer.create(BarChart(colours, list, data.all, list.length*60, handlePressIn, colors));
        expect(barChart).toMatchSnapshot();         
      });

    it('test bar chart with float values', () => {
        const barChart = renderer.create(BarChart(colours, floatList, floatData.all, floatList.length*60, handlePressIn, colors));
        expect(barChart).toMatchSnapshot();         
      });

    it('test bar chart with empty data', () => {
      const barChart = renderer.create(BarChart(colours, emptyArray, emptyData.all, emptyArray.length*60, handlePressIn, colors));
      expect(barChart).toMatchSnapshot();     
      });

    it('test bar chart no props', () => {
        const barChart = renderer.create(BarChart()).toJSON();
        expect(barChart).toBeNull();
        expect(barChart).toMatchSnapshot();
      });
  });