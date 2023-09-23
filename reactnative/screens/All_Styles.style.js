import { StyleSheet } from 'react-native';

export const styles = (dark, colors) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors?.background,
  },
  title: {
    fontWeight: '900',
    fontSize: 50,
    alignSelf: 'center',
    paddingVertical: 10,
    color: colors?.text,
  },
  buttonWide: {
    padding: 20,
    borderRadius: 10,
    marginVertical: 10,
    backgroundColor: colors?.primary,
  },
  text: {
    color: colors?.text,
  },
  textBold: {
    fontWeight: "700",
    color: colors?.text,
  },
  largeTextBold: {
    fontWeight: "800",
    fontSize: 40,
    color: colors?.text,
  },
  backArrow: {
    fontWeight: "900",
    fontSize: 30,
    paddingVertical: 10,
    color: colors?.primary,
  },
  button: {
    width: "75%",
    borderRadius: 25,
    textAlign: 'center',
    fontWeight: 'bold',
    marginTop: '4%',
    paddingHorizontal: "12%",
    paddingVertical: "2%",
    fontSize:  20,
    backgroundColor: colors?.primary,
    color: colors?.text,
  },
  smallButton: {
    marginTop: 10,
    padding: 10,
    paddingHorizontal: 30,
    borderRadius: 5,
    backgroundColor: colors?.primary,
  },
  input: {
    height: 40,
    width: '100%',
    borderWidth: 0.5,
    padding: 10,
    borderColor: 'gray',
    borderRadius: 5,
    marginTop: 5,
    marginBottom: 5,
  },
   btn: {
    padding: 10,
    margin: 10,
    borderRadius: 10,
    width: "40%",
    alignItems: "center",
  },
  list: {
    backgroundColor: colors?.background,
    width: "80%",
    borderWidth: 1,
    borderRadius: 4,
    borderColor: 'lightgrey',
  }
});