"use strict";

const alert = require("./modules/alert");
const app = require('electron').app;
const electron = require("electron");
const fs = require("fs");
const ipcMain = require("electron").ipcMain;
const path = require("path");
const read_prefs = require("./modules/preferences").read_prefs;
const save_prefs = require("./modules/preferences").save_prefs;
const windows = require("./modules/windows");

const save_dialog = electron.dialog.showSaveDialogSync || electron.dialog.showSaveDialog;
const open_dialog = electron.dialog.showOpenDialogSync || electron.dialog.showOpenDialog;

let about_message = `Fluorine ${app.getVersion()} is a replay viewer for Halite 3\n--\n` +
	`Electron ${process.versions.electron} + Node ${process.versions.node} + Chrome ${process.versions.chrome} + V8 ${process.versions.v8}`;

// -------------------------------------------------------
// Preferences.

const prefs = read_prefs();

function set_pref(attrname, value) {
	if (!prefs.hasOwnProperty(attrname)) {
		throw new Error("Tried to set a prefence attr that wasn't defined: ", attrname);
	}
	prefs[attrname] = value;
	windows.send("renderer", "prefs_changed", prefs);
	save_prefs(prefs);
}

// -------------------------------------------------------

let menu;

electron.app.on("ready", () => {

	let main = windows.new("renderer", {
		title: "Fluorine", show: false, width: 1150, height: 800, resizable: true, page: path.join(__dirname, "fluorine_renderer.html")
	});

	main.once("ready-to-show", () => {
		main.show();
	});

	windows.new("extra_stats", {
		title: "Extra Stats", show: false, width: 400, height: 800, resizable: true, page: path.join(__dirname, "fluorine_info.html")
	});

	windows.new("selector", {
		title: "Select Ship", show: false, width: 320, height: 100, resizable: true, page: path.join(__dirname, "fluorine_select.html")
	});

	windows.new("turn", {
		title: "Go To Turn", show: false, width: 320, height: 100, resizable: true, page: path.join(__dirname, "fluorine_turn.html")
	});

	menu = make_main_menu();
	electron.Menu.setApplicationMenu(menu);
});

electron.app.on("window-all-closed", () => {
	electron.app.quit();
});

// -------------------------------------------------------

ipcMain.on("alert", (event, msg) => {
	alert(msg);
});

ipcMain.on("renderer_ready", () => {

	// Open a file via command line. Some awkwardness around the different ways Fluorine can be started.

	let filename = "";

	if (path.basename(process.argv[0]) === "electron" || path.basename(process.argv[0]) === "electron.exe") {
		if (process.argv.length > 2) {
			filename = process.argv[process.argv.length - 1];
		}
	} else {
		if (process.argv.length > 1) {
			filename = process.argv[process.argv.length - 1];
		}
	}

	if (filename !== "") {
		windows.send("renderer", "open", filename);
		monitor_dirs(null);
	} else {
		monitor_dirs(prefs.last_monitored_replay_dirs);
	}
});

ipcMain.on("relay", (event, msg) => {
	windows.send(msg.receiver, msg.channel, msg.content);		// Messages from one browser window to another...
});

ipcMain.on("show_window", (event, window_token) => {
	windows.show(window_token);
});

ipcMain.on("hide_window", (event, window_token) => {
	windows.hide(window_token);
});

ipcMain.on("stop_monitoring", () => {
	monitor_dirs(null);
});

// -------------------------------------------------------
// Replay dir monitoring.

let replay_dir_watchers = [];

function get_replays(dirs) {
	let replays = [];
	for (let dir of dirs) {
		let filenames = fs.readdirSync(dir);
		for (let f of filenames) {
			if (f.endsWith(".hlt")) {
				replays.push(path.join(dir, f));
			}
		}
	}
	return replays;
}

function most_recent(filepaths) {

	// There's a race here if things change during the call, but meh.

	let recent_file = null;
	let recent_time = 0;

	for (let filepath of filepaths) {
		let t = fs.statSync(filepath).mtime.getTime();
		if (t > recent_time) {
			recent_file = filepath;
			recent_time = t;
		}
	}

	return recent_file;
}

function start_watcher(dir) {

	let darwin_last_filename = null;	// Variable specific to this watcher / folder.

	try {
		let watcher = fs.watch(dir, {persistent: false}, (eventType, filename) => {
			if (filename.endsWith(".hlt")) {
				windows.send("renderer", "log", `${eventType} - ${filename}`);
				if (process.platform === "darwin") {
					// fs.watch on OS X sends all events as "rename". It's the second
					// rename event that actually means the file is written.
					if (eventType === "rename" && darwin_last_filename === filename) {
						windows.send("renderer", "open_silent_fail", path.join(dir, filename));
					}
					darwin_last_filename = filename;
				} else {
					if (eventType === "change") {
						windows.send("renderer", "open_silent_fail", path.join(dir, filename));
					}
				}
			}
		});
		return watcher;
	} catch (err) {
		windows.send("renderer", "log", `monitor_dirs(): ${err.message}`);
		return null;
	}
}

function monitor_dirs(dirs) {

	dirs = dirs || [];

	for (let watcher of replay_dir_watchers) {
		watcher.close();
	}

	// Open the most recent replay file.
	// This might be rather slow for large directories?

	try {
		if (dirs.length) {
			let replay_paths = get_replays(dirs);
			if (replay_paths.length) {
				windows.send("renderer", "open", most_recent(replay_paths));
			}
		}
	} catch (err) {
		windows.send("renderer", "log", `monitor_dirs() while opening recent: ${err.message}`);
	}

	// Start the new watchers.

	replay_dir_watchers = [];

	for (let dir of dirs) {
		let watcher = start_watcher(dir);
		if (watcher) {
			replay_dir_watchers.push(watcher);
		}
	}

	// Checkmark on/off for the "open" menu item, enabled on/off for the "stop" item...
	menu.items[0].submenu.items[2].checked = replay_dir_watchers.length > 0 ? true : false;
	menu.items[0].submenu.items[3].enabled = replay_dir_watchers.length > 0 ? true : false;

	set_pref("last_monitored_replay_dirs", dirs);
}

// -------------------------------------------------------

function make_main_menu() {
	const template = [
		{
			label: "File",
			submenu: [
				{
					label: "Open...",
					accelerator: "CommandOrControl+O",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						let files = open_dialog({
							defaultPath: prefs.last_replay_directory || "",
							properties: ["openFile"]
						});
						if (files && files.length > 0) {
							set_pref("last_replay_directory", path.dirname(files[0]));
							windows.send("renderer", "open", files[0]);
							monitor_dirs(null);					// Stop monitoring if we were
						}
					}
				},
				{
					type: "separator"
				},
				{
					label: "Monitor replay folder...",
					type: "checkbox",
					checked: false,								// Updated by monitor_dirs()
					accelerator: "CommandOrControl+Shift+O",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						monitor_dirs(open_dialog({
							defaultPath: prefs.last_replay_directory || "",
							properties: ["openDirectory", "multiSelections"],
						}));
					}
				},
				{
					label: "Stop monitoring",
					enabled: false,								// Updated by monitor_dirs()
					click: () => {
						monitor_dirs(null);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Open f-log...",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						let files = open_dialog({
							defaultPath: prefs.last_flog_directory || "",
							properties: ["openFile"]
						});
						if (files && files.length > 0) {
							set_pref("last_flog_directory", path.dirname(files[0]));
							windows.send("renderer", "open_flog", files[0]);
						}
					}
				},
				{
					label: "What is an f-log?",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						about_flogging();
					}
				},
				{
					type: "separator"
				},
				{
					label: "Save decompressed JSON",
					accelerator: "CommandOrControl+S",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						let outfilename = save_dialog();
						if (outfilename) {
							windows.send("renderer", "save", outfilename);
						}
					}
				},
				{
					label: "Save current frame",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						let outfilename = save_dialog();
						if (outfilename) {
							windows.send("renderer", "save_frame", outfilename);
						}
					}
				},
				{
					label: "Save current entities",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						let outfilename = save_dialog();
						if (outfilename) {
							windows.send("renderer", "save_entities", outfilename);
						}
					}
				},
				{
					label: "Save upcoming moves",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						let outfilename = save_dialog();
						if (outfilename) {
							windows.send("renderer", "save_moves", outfilename);
						}
					}
				},
				{
					label: "Save upcoming events",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						let outfilename = save_dialog();
						if (outfilename) {
							windows.send("renderer", "save_events", outfilename);
						}
					}
				},
				{
					type: "separator"
				},
				{
					accelerator: "CommandOrControl+Q",
					role: "quit"
				},
			]
		},
		{
			label: "Navigation",
			submenu: [
				{
					label: "Forward",
					accelerator: "Right",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.send("renderer", "forward", 1);
					}
				},
				{
					label: "Back",
					accelerator: "Left",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.send("renderer", "forward", -1);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Move to start",
					accelerator: "Home",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.send("renderer", "forward", -99999);
					}
				},
				{
					label: "Move to end",
					accelerator: "End",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.send("renderer", "forward", 99999);
					}
				},
				{
					label: "Autoplay",
					accelerator: "Space",
					click: () => {
						windows.send("renderer", "toggle_autoplay", null);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Go to turn...",
					accelerator: "CommandOrControl+T",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.show("turn");
						windows.send("turn", "focus_input", null);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Previous collision",
					accelerator: "C",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.send("renderer", "previous_collision", null);
					}
				},
				{
					label: "Next collision",
					accelerator: "V",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.send("renderer", "next_collision", null);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Selected ship's fate",
					accelerator: "X",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.send("renderer", "ship_fate", null);
					}
				},
			]
		},
		{
			label: "View",
			submenu: [
				{
					label: "Integer box sizes",
					type: "checkbox",
					checked: prefs.integer_box_sizes,
					click: (menuItem) => {
						set_pref("integer_box_sizes", menuItem.checked);
					}
				},
				{
					label: "Turns start at 1",
					type: "checkbox",
					checked: prefs.turns_start_at_one,
					click: (menuItem) => {
						set_pref("turns_start_at_one", menuItem.checked);
					}
				},
				{
					label: "Grid",
					submenu: [
						{
							label: "0",
							type: "radio",
							accelerator: "F1",
							checked: prefs.grid_aesthetic === 0,
							click: () => {
								set_pref("grid_aesthetic", 0);
							}
						},
						{
							label: "halite / 4",
							type: "radio",
							accelerator: "F2",
							checked: prefs.grid_aesthetic === 1,
							click: () => {
								set_pref("grid_aesthetic", 1);
							}
						},
						{
							label: "255 * sqrt(halite / 2048)",
							type: "radio",
							accelerator: "F3",
							checked: prefs.grid_aesthetic === 2,
							click: () => {
								set_pref("grid_aesthetic", 2);
							}
						},
						{
							label: "255 * sqrt(halite / 1024)",
							type: "radio",
							accelerator: "F4",
							checked: prefs.grid_aesthetic === 3,
							click: () => {
								set_pref("grid_aesthetic", 3);
							}
						},
					]
				},
				{
					label: "Triangles",
					submenu: [
						{
							label: "Show next move",
							type: "radio",
							checked: prefs.triangles_show_next,
							click: () => {
								set_pref("triangles_show_next", true);
							}
						},
						{
							label: "Show previous move",
							type: "radio",
							checked: prefs.triangles_show_next === false,
							click: () => {
								set_pref("triangles_show_next", false);
							}
						}
					]
				},
				{
					type: "separator"
				},
				{
					label: "Up",
					accelerator: "W",
					click: () => {
						windows.send("renderer", "down", 1);
					}
				},
				{
					label: "Left",
					accelerator: "A",
					click: () => {
						windows.send("renderer", "right", 1);
					}
				},
				{
					label: "Down",
					accelerator: "S",
					click: () => {
						windows.send("renderer", "down", -1);
					}
				},
				{
					label: "Right",
					accelerator: "D",
					click: () => {
						windows.send("renderer", "right", -1);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Reset camera",
					accelerator: "R",
					click: () => {
						windows.send("renderer", "set", ["offset_x", 0]);
						windows.send("renderer", "set", ["offset_y", 0]);
					}
				},
				{
					label: "Farside camera",
					accelerator: "F",
					click: () => {
						windows.send("renderer", "farside", null);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Select ship by ID...",
					accelerator: "CommandOrControl+F",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.show("selector");
						windows.send("selector", "focus_input", null);
					}
				},
				{
					label: "Clear selection",
					accelerator: "Escape",
					click: () => {
						windows.send("renderer", "set", ["selection", null]);
					}
				},
				{
					type: "separator"
				},
				{
					label: "Font smaller",
					accelerator: "CommandOrControl+-",
					role: "zoomout"
				},
				{
					label: "Font larger",
					accelerator: "CommandOrControl+=",
					role: "zoomin"
				},
				{
					label: "Reset font",
					role: "resetzoom"
				},
			]
		},
		{
			label: "Extra",
			submenu: [
				{
					label: "Extra stats",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						windows.show("extra_stats");
					}
				},
				{
					type: "separator"
				},
				{
					label: "About Fluorine",
					click: () => {
						windows.send("renderer", "stop_autoplay", null);
						alert(about_message);
					}
				},
				{
					label: "Dev tools",
					role: "toggledevtools"
				},
			]
		},
	];

	return electron.Menu.buildFromTemplate(template);
}

function about_flogging() {

	let s = `

An f-log is a JSON file with the following format:

    [
        {"t": 1, "x": 22, "y": 22, "msg": "Hello"},
        {"t": 15, "x": 8, "y": 15, "msg": "Danger!", "color": "red"},
        {"t": 15, "x": 9, "y": 16, "color": "#0000FF"}
    ]

For convenience, Fluorine can parse an incomplete JSON array, meaning \
one lacking its closing "]". Such an incomplete array can have a final \
"," or not. You may find this format easier to write.

When an f-log is loaded, if the Fluorine crosshairs are on a point \
with a message (i.e. at time t, coordinates x and y) then the given \
message will be displayed in the infobox. If the f-log has more than \
one message for a given [t,x,y] then all of them will be shown.

Colours in the f-log are always shown when available.

For t, you may consider turns as starting at 0 or 1. There is a menu \
item in the View menu for this. Make sure Fluorine is using the same \
system as your bot.

Also note that loading an f-log is not safe against malicious input.`;

	alert(s);
}
