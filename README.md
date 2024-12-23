# Quest beatsaber playlist manager

## About
Python tool for managing BeatSaber custom playlists on Quest3 for songs downloaded from beatsaver.com.
Required mods for beatsaber: Playlist manager.
Required external libraries: FFMPEG, adb
Author used this release for modding beatsaber: https://mbf.bsquest.xyz/.

## How to run
1. Install python. Application was developed with python 3.11.
2. Clone/download repository. 
3. Open terminal in the cloned/downloaded repository and install required python packages with a command:
`pip install -r requirements.txt`
4. Create folder named *adb* in the cloned/downloaded repository. Download Android Debug Bridge (https://developer.android.com/tools/adb) and unzip it into that folder.
5. Download FFMPEG (https://www.ffmpeg.org/) and install it.
6. Run *main.pyw*.

**Warning!**
When closing application cmd terminal can appear. It is desired function - application is killing adb.exe process with a command `taskkill -f -im "adb.exe"`.

## Drop down menus
- **Playlist** - options for managing playlist
-- **New -> Empty playlist** - creates new empty playlist
-- **New -> From local downloaded maps** - user should select the folder with downloaded maps (zipped or unzipped) and application will add them to a new playlist
-- **Load** - loads a playlist from folder *playlists*
-- **Save** - saves playlist to a *playlists*folder

- **Quest** - options for communicating with Quest using ADB
-- **Connect** - opens a dialog window for connecting with Quest. Connection is successful when user allows for debug connection in VR device
-- **Get songs** - checks the songs downloaded in the Quest and adds them to Quest maps Table
-- **Check missing maps** - compares playlist with Quest Maps. If there are any missing maps on VR device a dialog window with download links will appear.
-- **Pull playlists from Quest** - downloads playlists from Quest to the *playlists* folder. This action wil overwrite files with the same name.
-- **Push playlists to Quest** - uploads all playlists from *playlists* folder. This action wil overwrite files with the same name.
-- **Delete playlists from Quest** - opens a dialog window for deleting playlists.

## Building the playlist
- drag row from "Quest maps" to "Playlist maps" to add a new song. In case of adding an already exisitng song a marching row will be highloghted green.
- to modify songs order of playlist:
-- select maps with *left click*. Multiple maps can be selected with *CTRL + left click*
-- move maps with *Up* or *Down* buttons
-- delete maps with *Delete* button
- modify header of playlist with *Header* button

## Playlist header
Playlist header consists of: 
- name
- author
- image (images will be scaled to 256 x 256 px)

## Filtering maps
Tables can be filtered with a corresponding *Filter maps* button. Clicking it open a dialog window when filter criteria can be written. Criterias are:
- **regex search** - filter *Title, Author, Mapper, Tags, Levels' names, Levels' characteristic* with a regular expression
- **length, BPM, Notes Per Second, Notes Jump Speed, Stars** - the values can be either range or exact value. Range is given as;
-- **[num1;num2]** - searches values from num1 to num2
-- **[;num2]** - searches values from *-Inf* to num2
-- **[num1;]** - searches values from num1 to *Inf*
-- **[;]** - searches values from *-Inf* to *Inf*
- **Ranked State, mods** - select checkbox for required values

To remove filters press corresponding *Reset filters* button.

## Quest maps order
Quest maps order can be changed with *Sorting Order* list and *Reverse Order* button. Using these widgets will reset filters, because playlist is Quest Maps Table is regenerated.


# Files and classes
## Quest maps and playlists
Playlist class hierarchy:
- **beatSaberMapLevel.py -> BeatSaberMapLevel**: data class for a one beatsaber level.
- **beatSaberMap.py -> beatSaberMap**: class for a beatsaber map. Typically build from JSON data from api.beatsaver.com. Each map have *BeatSaberMapLevel* classes 
- **beatSaberPlaylist.py -> BeatSaberPlaylist** class for a playlist. Playlist consists of *BeatSaberMap* classes

Adb handling:
- **adbWrapperFactory.py -> AdbWrapperFactory**: factory for operating systen ADB wrappers. Each wrapper must implement methods in the factory
- **adbWindowsWrapper.py -> AdbWindowsWrapper**: ADB handler for windows operating system. Other operating systems haven't been implemented yet.

Getting songs data:
- **beatSaverAPICaller.py -> BeatSaverAPICaller**: namespace for methods dedicated to get data of maps from api.beatsaver.com

GUIs:
- **main.pyw**: main window
- **connectQuestDialog.py -> ConnectQuestThread**: dialog window for establishing communication with Quest,
- **deletePlaylistsDialog.py**: dialog window for deleting playlists from Quest,
- **downloadMissingMapsDialog.py**: dialog window for downloading missing maps,
- **filterMapsDialog.py**: dialog window for filtering maps,
- **playlistDataDialog.py**: dialog window for modifing playlist header.

Helper classes:
-**tabletWidgetWrapper.py**: mixin patterns that extends default QTableWidget. Used for encapsulating Quest maps table and Playlist Table
-**mapDetailsWrapper.py**: classes that encapsulates map details (right column of the main window). 
--**labelWrapper.py**:  mixin pattern that extends default QLabel with elided text. Used for map details
-- **byteStringMusicPlayer.py -> ByteStringMusicPlayer**: music player which takes byte string as a music source. Used in main window.
-- **filterMapCacheDecorators.py**: Decrator patterns for applying search filers. Multiple criteria are chained in a structure similiar to a linked list: criteria1 -> criteria2 -> ...-> criteriaN and evaluated one by one as a stack.