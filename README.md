# Custom E-Ink Reader

A custom, lightweight e-reader built with Python and designed to run on a Raspberry Pi with a Waveshare 3.7-inch e-ink display. The project focuses on building an e-reader from the ground up, including a custom user interface, EPUB library management, reading settings, and e-ink display integration.

> **Status:** In Progress

## Overview

This project is an exploration of embedded software development, Python application architecture, and e-ink interfaces. The goal is to create a dedicated reading device with a simple, distraction-free interface and physical button controls.

The application is being developed on a computer using a display simulator before being deployed to a Raspberry Pi and physical e-ink display.

## Current Features

* Custom home menu with physical-button navigation
* EPUB library browsing
* EPUB file detection and organization
* Book cover extraction and display
* Reading progress tracking
* Custom settings menu
* Font selection
* Adjustable reading font size
* Persistent settings using JSON
* Light and dark display modes
* Restore-default-settings functionality
* Automatic date and time display
* E-ink display support through Waveshare's `epd3in7` display
* Display simulator for development without physical hardware

## Planned Features

* [ ] FBReader integration for improved EPUB reading
* [ ] Book metadata display
* [ ] Page navigation
* [ ] Improved reading progress and resume functionality
* [ ] Physical Raspberry Pi button integration
* [ ] Additional font options
* [ ] Further e-ink display optimization
* [ ] Hardware testing and refinement

## Technology

**Languages & Libraries**

* Python
* Pillow
* EbookLib
* BeautifulSoup

**Hardware**

* Raspberry Pi
* Waveshare 3.7-inch e-Paper Display (`epd3in7`)
* 4-button physical input

**Development**

* Git / GitHub
* Display simulator
* JSON-based configuration and persistence

## Project Structure

```text
Custom E-Reader/
├── main.py              # Application entry point
├── menu.py              # Home and settings menus
├── library.py           # EPUB library management
├── reader.py            # EPUB processing and reading functionality
├── fbreader.py          # FBReader integration
├── display.py           # Display abstraction and rendering
├── simulator.py         # Development display simulator
├── settings.py          # Settings management
├── settings.json        # Saved user settings
├── fonts/               # Application fonts
├── books/               # EPUB library
└── protected books/     # Local protected-book files
```

Protected books and other user-specific content are kept outside version control.

## Development

The project uses a display simulator during development so that the interface can be tested without connecting the Raspberry Pi and physical e-ink display.

The application is designed so that display-specific functionality is separated from the rest of the application. This allows the same interface code to be tested in the simulator and later deployed to the Waveshare display.

## Goals

The long-term goal is to create a functional, portable e-reader that combines:

* Embedded Linux development
* Python application development
* Hardware/software integration
* E-ink display rendering
* EPUB processing
* Persistent application settings
* A simple physical user interface

This project is currently under active development.
