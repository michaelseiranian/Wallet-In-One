import { VictoryChart, VictoryLine, VictoryAxis, VictoryScatter } from "victory-native";	
import { useTheme } from 'reactnative/src/theme/ThemeProvider'
export function BalanceChart({rawData,highest}) {	

  const {dark, colors, setScheme} = useTheme();

  const data = Object.keys(rawData).map(date => ({	
    x: new Date(date),	
    y: parseFloat(rawData[date])	
  }));	

  const beforeMonths = Object.keys(rawData).map(date => {date = new Date(date); return new Date(date.getFullYear(), date.getMonth(), 1)});	
  const afterMonths = Object.keys(rawData).map(date => {date = new Date(date); return new Date(date.getFullYear(), date.getMonth()+1, 1)});	
  const months = beforeMonths.concat(afterMonths)	
  	
  return (	
    <VictoryChart minDomain={{ y: 0 }} maxDomain={{ y: highest*1.1 }} height={220} width={350}>	
    <VictoryLine data={data} interpolation="stepAfter" style={{ data: { stroke: "#0055b3", strokeWidth: 2 } }} />	
    <VictoryAxis	
      tickFormat={(date) => {	
        var d = new Date(date)	
        return `${d.getMonth()+1}/${d.getFullYear().toString().substr(-2)}`	
      }}	
      tickValues = {months}	
      style={{	
        grid: {	
          stroke: "grey",	
          strokeDsharray: "2, 5"	
        },	
        axis: {stroke: 'grey'},
        tickLabels: {fill: colors.text , fontSize: 12},
      }}	
    />	
    <VictoryAxis	
      tickFormat={(value) => `£${value}`}	
      dependentAxis={true}

      style={{	
        grid: {	
          stroke: "grey",	
          strokeDasharray: "2, 5"	
        },
        axis: {stroke: 'grey'},
        tickLabels: {fill: colors.text},	
      }}	
    />	
    	
  </VictoryChart>	
  );	
}