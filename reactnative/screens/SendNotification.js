import * as Notifications from "expo-notifications";
export const sendNotification = (notificationSettings) => {
  if (notificationSettings === "true") {
    Notifications.requestPermissionsAsync();
    Notifications.presentNotificationAsync({
      title: "Notifications On",
      body: "You have successfully turned on the notification.",
      //Try this later
      //ios: { _displayInForeground: true },
    });
  } else {
    console.log("Notifications are disabled");
  }
};
export const sendThemeNotification = (notificationSettings) => {
  if (notificationSettings === "true") {
    Notifications.requestPermissionsAsync();
    Notifications.presentNotificationAsync({
      title: "Theme changed",
      body: "You have successfully changed the theme.",
      //Try this later
      //ios: { _displayInForeground: true },
    });
  } else {
    console.log("Notifications are disabled");
  }
};


