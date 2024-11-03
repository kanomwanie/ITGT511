# Fluorine 🐢
"I got it yesterday, and it's already changed my life." &mdash; [teccles](https://halite.io/user/?user_id=2807)

![Fluorine Screenshot](https://user-images.githubusercontent.com/16438795/48973423-e1ae5900-f036-11e8-9546-58f19a3c493d.png)

This is a replay viewer for [Halite 3](https://halite.io/).

# Installation

If you have npm and [Electron](https://electron.atom.io/) installed globally (`npm install electron -g`) you can enter the *Fluorine* directory and do:

```
npm install
electron .
```

If you only have npm, and don't want to install Electron globally, I'm told the following works instead:

```
npm install
npm install electron --save-dev --save-exact
./node_modules/.bin/electron .
```

Finally, for those who use Docker, lpenz supplies a [Dockerfile](https://gist.github.com/lpenz/09776db42cf5bdb5d6a2553d53f8899e).

# Building

Once the dependencies are installed (`npm install`), it should be possible to build a standalone application with `npm run pack` but for Windows there's also a pre-built application in the *Releases* section of this repo.

# Other dependencies

* [node-zstandard](https://www.npmjs.com/package/node-zstandard) (gets installed by `npm install`)

# Usage

Open a file from the menu, or via command line with `electron . filename.hlt`. Drag-and-dropping a file onto the window may also work. Once a file is opened, navigate with left and right arrow keys.

# Thanks

Thanks to Snaar, Shummie, Ewirkerman, and Lidavidm for helpful discussions. *Fluorine* was developed during the beta phase of Halite 3 despite me not actually being in the beta, so I relied on them for information. Thanks to DomNomNom for the "monitor folder" feature. Thanks to DanielVF for an OS X bugfix. Thanks for Billiam for coloured logs and other enhancements.
