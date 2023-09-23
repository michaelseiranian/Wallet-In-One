import React from 'react';
import { StyleSheet, Text, View} from 'react-native';

import { LineChart, CandlestickChart } from 'react-native-wagmi-charts';
import { useTheme } from "reactnative/src/theme/ThemeProvider";
import { styles } from "reactnative/screens/All_Styles.style.js";

// Display a LineChartScreen component which takes in several props to configure the chart to the needs of the user.
export default function LineChartScreen({graph_version, height, width, current_balance, data})
{
    const {dark, colors, setScheme } = useTheme();

    let percentageChange = null;
    let priceChange = null;
    
    // Define a function to calculate the percentage and price change between the current_balance and the previous balance stored in the data array.
    function calculateChange(new_value, old_value) {
        if (old_value != 0){
            percentageChange = (((new_value - old_value) / Math.abs(old_value)) * 100).toFixed(2);
        }
        else{
            // If the old balance is equal to zero, set the percentageChange to '0 ERR' as division by 0 is not possible.
            percentageChange = '0 ERR';
        }
        
        if (percentageChange > 0) {
            percentageChange = '+' + percentageChange;
        }
        
        priceChange = (((new_value) - old_value)).toFixed(3);
        if(priceChange > 0){
            priceChange = '+' + priceChange;
        }
    }
    calculateChange(current_balance, data[0]?.value);

    // Set colour of the line graph based on the balace fluctuation.
    let color1 = '';
    
    if (data && data.length > 0) {
        if (data[0]?.value > data[data.length -1]?.value){
            color1 = 'red';
        } 
        else {
            color1 = 'green';
        }
    }

    let candlestickData = null;

    // Check if the graph version is equal to 3. If so, map the list of line graph data ({timestamp,value})
    // into data that is compatible with the candlestick chart ({timestamp,open,close,high,low})
    if(graph_version == 3){
        // Use the reduce function to transform the data array into an object with data grouped by month.
        const transformedData = data.reduce((acc, transaction) => {
            const date = new Date(transaction.timestamp);
            const month = `${date.getFullYear()}-${date.getMonth() + 1}`;

            // If the month doesn't exist in the accumulator object, create a new object with the transaction's value for all fields.
            if (!acc[month]) {
                acc[month] = {
                    high: transaction.value,
                    low: transaction.value,
                    open: transaction.value,
                    close: transaction.value,
                };
            } 
            else {
                // If the month already exists in the accumulator object, update the high, low, and close values.
                if (transaction.value > acc[month].high) {
                    acc[month].high = transaction.value;
                }

                if (transaction.value < acc[month].low) {
                    acc[month].low = transaction.value;
                }

                acc[month].close = transaction.value;
            }

            return acc;
        }, {});
        
        // Use Object.keys to get an array of the keys (month-year strings) and map them to candlestick compatible data.
        candlestickData = Object.keys(transformedData).map((key) => {
            const [year, month] = key.split('-');
            return {
                timestamp: (new Date(year, month - 1)).getTime(),
                open: parseFloat(transformedData[key].open),
                close: parseFloat(transformedData[key].close),
                high: parseFloat(transformedData[key].high),
                low: parseFloat(transformedData[key].low),
            };
        });
    }

    return (
        <View >
            {data && data.length > 1 ? (
                <>
                    {/* Interactive graph */}
                    { graph_version == 1 && 
                        <>
                        <View style={{flexDirection: 'row', paddingBottom: 14, paddingHorizontal: 10}} >
                            <Text style={{ color: color1, fontSize: 14, fontWeight: 'bold' }}>{priceChange}</Text>
                            <Text style={{ color: color1, fontSize: 14, fontWeight: 'bold' }}> ({percentageChange}%)</Text>
                        </View>

                        <LineChart.Provider data={data}>
                            <LineChart height={height} width={width}>
                                <LineChart.Path color={color1}>
                                    <LineChart.Gradient />
                                </LineChart.Path>
                                <LineChart.HorizontalLine />
                                <LineChart.CursorLine />
                                <LineChart.CursorCrosshair />
                            </LineChart>

                            <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
                                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                                    <Text style={{ marginHorizontal: 5, fontSize: 12, color: colors.text}}>Date: </Text>
                                    <LineChart.DatetimeText precision={10} style={{ color: colors.text, fontSize: 13, fontWeight: 'bold' }} />
                                </View>

                                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                                    <Text style={{ marginHorizontal: 5, fontSize: 12,color: colors.text}}>Balance: </Text>
                                    <LineChart.PriceText precision={10} style={{ color: colors.text, fontSize: 13, fontWeight: 'bold' }}/>
                                </View>
                            </View>
                        </LineChart.Provider></>
                    }


                    {/* Static graph */}   
                    { graph_version == 2 &&
                    <><Text style={{ textAlign: 'right', marginLeft: 'auto', color: color1, fontSize: 11 }}>{percentageChange}%</Text>
                    <LineChart.Provider data={data}>
                            <LineChart width={width} height={height}>
                                <LineChart.Path color={color1}>
                                    <LineChart.Gradient />
                                </LineChart.Path>
                            </LineChart>
                        </LineChart.Provider></>
                    }
                    {/* Candelstick graph */}   
                    { graph_version == 3 && candlestickData &&
                        <>
                        <View style={{flexDirection: 'row', paddingBottom: 14, paddingHorizontal: 10}}>
                            <Text style={{ color: color1, fontSize: 14, fontWeight: 'bold' }}>{priceChange}</Text>
                            <Text style={{ color: color1, fontSize: 14, fontWeight: 'bold' }}> ({percentageChange}%)</Text>
                        </View>

                        <CandlestickChart.Provider data={candlestickData}>
                            <CandlestickChart height={height} width={width}>
                                <CandlestickChart.Candles />
                                <CandlestickChart.Crosshair />
                            </CandlestickChart>
                            
                            <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
                                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                                    <Text style={{ marginHorizontal: 8, fontSize: 12,color: colors.text }}>Opening Price:</Text>
                                    <CandlestickChart.PriceText precision={10} type="open" style={{ color: colors.text, fontSize: 12, fontWeight: 'bold' }} />
                                </View>

                                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                                    <Text style={{ marginHorizontal: 8, fontSize: 12,color: colors.text  }}>Highest Price: </Text>
                                    <CandlestickChart.PriceText precision={10} type="high" style={{ color: colors.text, fontSize: 12, fontWeight: 'bold' }} />
                                </View>
                            </View>

                            <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
                                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                                    <Text style={{ marginHorizontal: 8, fontSize: 12,color: colors.text  }}>Closing Price:</Text>
                                    <CandlestickChart.PriceText precision={10} type="close" style={{ color: colors.text, fontSize: 12, fontWeight: 'bold' }} />
                                </View>

                                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                                    <Text style={{ marginHorizontal: 8, fontSize: 12,color: colors.text }}>Lowest Price:</Text>
                                    <CandlestickChart.PriceText precision={10} type="low" style={{ color: colors.text, fontSize: 12, fontWeight: 'bold' }} />
                                </View>
                            </View>

                            <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
                                <Text style={{ marginHorizontal: 1, fontSize: 12,color: colors.text}}>Date: </Text>
                                <CandlestickChart.DatetimeText style={{ fontSize: 12,color: colors.text, fontWeight: 'bold' }} />
                            </View>

                        </CandlestickChart.Provider></>
                        
                    }

                    {/* Interactive graph WalletAssetVersion */}
                    { graph_version == 4 && 
                        <>
                        <View style={{flexDirection: 'row', paddingBottom: 14, paddingHorizontal: 10}}>
                            <Text style={{ color: color1, fontSize: 14, fontWeight: 'bold' }}>{priceChange}</Text>
                            <Text style={{ color: color1, fontSize: 14, fontWeight: 'bold' }}> ({percentageChange}%)</Text>
                        </View>

                        <LineChart.Provider data={data}>
                            <LineChart height={height} width={width}>
                            <LineChart.Path color={colors.text}/>
                            <LineChart.CursorCrosshair color={colors.text}>

                                <LineChart.Tooltip textStyle={{color: colors.text}}>
                                <LineChart.PriceText precision={10} style={{color: colors.text}} />
                                </LineChart.Tooltip>

                                <LineChart.Tooltip position="bottom" >
                                <LineChart.DatetimeText style={{color: colors.text}} />
                                </LineChart.Tooltip>

                            </LineChart.CursorCrosshair>
                            </LineChart>
                        </LineChart.Provider></>
                    }
                </>
            ) : (<Text style={[chartStyles.emptyText, {textAlign: 'center', alignSelf: 'center', color: colors.text}]}>No data available</Text>)}

        </View>
    );
}


const chartStyles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    alignSelf: 'center',
    padding: 8,
  },
  chartContainer: {
    marginVertical: 8,
    borderRadius: 16,
    // paddingHorizontal: 10,
  },
  head: {
    height: 44,
     backgroundColor: '#42b983'
  },
  text: { 
    // margin: 8
  },
  row: { 
    flexDirection: 'row',
  },
  ins_name:{
    // color: colors.text,
    fontSize: 15,
    fontFamily: 'sans-serif',
  },
});