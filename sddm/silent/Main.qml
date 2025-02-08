import QtQuick 2.2
import QtGraphicalEffects 1.0
import SddmComponents 2.0

Rectangle {
	id: root
	width: 1920
	height: 1080
	state: config.lockScreen || true || config.lockScreen === "true" ? "lockState" : "loginState"

	readonly property bool showLockScreen: config.lockScreen || true || config.lockScreen === "true"
	readonly property color fontColor: "light" ? config.lightModeFontColor : config.darkModeFontColor;
	readonly property color bgColor: "light" ? config.lightModeBgColor : config.darkModeBgColor;
	readonly property string loginPosition: config.loginPosition || "center"
	readonly property string lockPosition: config.lockPosition || "center"

	states: [
		State {
			name: "lockState"
			PropertyChanges { target: lockScreen; opacity: 1 }
			PropertyChanges { target: loginScreen; opacity: 0 }
			PropertyChanges { target: loginScreen; scale: 0.5 }
			PropertyChanges { target: blur; radius: 0 }
		},
		State {
			name: "loginState"
			PropertyChanges { target: lockScreen; opacity: 0 }
			PropertyChanges { target: loginScreen; opacity: 1 }
			PropertyChanges { target: loginScreen; scale: 1 }
			PropertyChanges { target: blur; radius: config.blur || 50 }
		}
	]

	transitions: Transition {
		enabled: config.animations || true || config.animations === "true"
        PropertyAnimation { duration: 150; properties: "opacity"; }
        PropertyAnimation { duration: 400; properties: "radius"; }
		PropertyAnimation { duration: 200; properties: "scale"; }
    }
}
