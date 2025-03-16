import { App } from "astal/gtk3"
import { Variable, GLib, bind, exec } from "astal"
import { Astal, Gtk, Gdk } from "astal/gtk3"
import Hyprland from "gi://AstalHyprland"
import Mpris from "gi://AstalMpris"
import Battery from "gi://AstalBattery"
import Wp from "gi://AstalWp"
import Network from "gi://AstalNetwork"
import Tray from "gi://AstalTray"

function SysTray() {
	const tray = Tray.get_default()

	return <box className="SysTray">
		{bind(tray, "items").as(items => items.map(item => (
			<menubutton
				tooltipMarkup={bind(item, "tooltipMarkup")}
				usePopover={false}
				actionGroup={bind(item, "actionGroup").as(ag => ["dbusmenu", ag])}
				menuModel={bind(item, "menuModel")}>
				<icon gicon={bind(item, "gicon")} />
			</menubutton>
		)))}
	</box>
}

function Wifi() {
	const network = Network.get_default()
	const wifi = bind(network, "wifi")

	return <box visible={wifi.as(Boolean)}>
		{wifi.as(wifi => wifi && (
			<icon
				tooltipText={bind(wifi, "ssid").as(String)}
				className="Wifi"
				icon={bind(wifi, "iconName")}
			/>
		))}
	</box>
}

function BatteryLevel() {
	const bat = Battery.get_default()

	return <box className="Battery"
		visible={bind(bat, "isPresent")}>
		<icon icon={bind(bat, "batteryIconName")} />
		<label label={bind(bat, "percentage").as(p =>
			`${Math.floor(p * 100)} %`
		)} />
	</box>
}

function Media() {
	const mpris = Mpris.get_default()

	return <box className="Media">
		{bind(mpris, "players").as(ps => ps[0] ? (
			<box>
				<box
					className="Cover"
					valign={Gtk.Align.CENTER}
					css={bind(ps[0], "coverArt").as(cover =>
						`background-image: url('${cover}');`
					)}
				/>
				<label
					label={bind(ps[0], "metadata").as(() =>
						`${ps[0].title} - ${ps[0].artist}`
					)}
				/>
			</box>
		) : (
			<label label="Nothing Playing" />
		))}
	</box>
}

function Workspaces() {
	const hypr = Hyprland.get_default()

	return <box className="Workspaces">
		<label label={bind(hypr, "focusedWorkspace").as(fw => fw.id.toString())} />
	</box>

	//return <box className="Workspaces">
	//	{bind(hypr, "workspaces").as(wss => wss
	//		.filter(ws => !(ws.id >= -99 && ws.id <= -2)) // filter out special workspaces
	//		.sort((a, b) => a.id - b.id)
	//		.map(ws => (
	//			<button
	//				className={bind(hypr, "focusedWorkspace").as(fw =>
	//					ws === fw ? "focused" : "")}
	//				onClicked={() => ws.focus()}>
	//				{ws.id}
	//			</button>
	//		))
	//	)}
	//</box>
}

// LUA:
// local patterns = {
//  ["^Spotify Premium$"] = "Spotify",
//  ["^.* - Obsidian v.*$"] = "Obsidian",
//}
//
//function matchPat(str)
//  for key, value in pairs(patterns) do
//    if string.match(str, key) then
//      return value
//    end
//  end
//  return str
//end

// hyprctl clients
const clients_ititle_rules: { [key: string]: string } = {
	"^Spotify Premium$": "Spotify",
	"^.* - Obsidian v.*$": "Obsidian",
};
const clients_title_rules: { [key: string]: string } = {
	"^nvim.*$": "Neovim",
	"^~$": "Ghostty",
};

const correct_title = (title: string, ititle = false) => {
	const client_rules = ititle ? clients_ititle_rules : clients_title_rules;

	title = title.trim();

	for (const key in client_rules) {
		if (new RegExp(key).test(title)) {
			if (title.includes(key))
				return

			return client_rules[key];
		}
	}

	return ititle ? title : title.split(" ")[0];
}

function FocusedClient() {
	const hypr = Hyprland.get_default()
	const focused = bind(hypr, "focusedClient")

	return <box
		className="Focused"
		visible={focused.as(Boolean)}>
		{focused.as(client => (
			client && <label label={bind(client, "title").as(
				title => correct_title(hypr.get_focused_client().initialTitle, true) || correct_title(hypr.get_focused_client().title))} />
		))}
	</box>

}

function Time({ format = "%H:%M" }) {
	const time = Variable<string>("").poll(1000, () =>
		GLib.DateTime.new_now_local().format(format)!)

	return <label
		className="Time"
		onDestroy={() => time.drop()}
		label={time()}
	/>
}

function Upgrades() {
	const cmd = "bash -c 'checkupdates | wc -l'"
	return <label
		className="Upgrades"
		label={exec(cmd)}
	/>
}

export default function Bar(monitor: Gdk.Monitor) {
	const { TOP, LEFT, RIGHT } = Astal.WindowAnchor

	return <window
		className="Bar"
		gdkmonitor={monitor}
		exclusivity={Astal.Exclusivity.EXCLUSIVE}
		anchor={TOP | LEFT | RIGHT}>
		<centerbox>
			<box hexpand halign={Gtk.Align.START}>
				<Workspaces />
				<FocusedClient />
			</box>
			<box>
				<Media />
			</box>
			<box hexpand halign={Gtk.Align.END} >
				<Time />
			</box>
		</centerbox>
	</window>
}
