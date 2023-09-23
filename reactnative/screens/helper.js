'use strict';
import React, { Component } from 'react';
import {
  AppRegistry,
  Text,
  TextInput,
  View
} from 'react-native';

export function ConvertTransactionsToGraphCompatibleData(transactions, balance) {
    let graph_data = transactions.map((item) => [item.amount, item.date]);
    graph_data = graph_data.sort((a, b) => new Date(b[1]) - new Date(a[1]));

    let points = [];

    for (let i = 0; i < graph_data.length; i++) {
        let point = {timestamp: new Date(graph_data[i][1]).getTime(), value: balance};
        balance -= graph_data[i][0];
        points = [point, ...points];
    }
    if (points.length > 0) {
        points[points.length - 1].value = parseFloat(points[points.length - 1].value);
    }
    return (points);
}