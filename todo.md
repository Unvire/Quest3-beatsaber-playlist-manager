# quest-beatsaber-playlist-manager
 Python tool for managing BeatSaber custom playlists on Quest3 for songs downloaded from beatsvaer.com.
 Required mods for beatsaber: Playlist manager.
 Author used ths release for modding https://mbf.bsquest.xyz/.
 
# Communication with Quest
 ADB - https://developer.android.com/tools/adb

# TO DO
 1. Communicate with Quest3 and get folder names od songs in the folder. Each folder name contains map ID. Get exisitng playlists.
 2. Use api for getting map's hash: https://api.beatsaver.com/maps/id/{id}, and build a structure with keys "key", "hash", "songName"
 3. Build a structure for holding a playlist. Header must contain keys: "playlistTitle", "playlistAuthor", "image" and "songs". It must be possible for user to perform add, remove and change order of songs
 4. ADB is dependant on operating system, make a tool for downloading proper version and unzipping it. (factory?)
 5. Build a GUI
 6. Build a tool for selecting image: Let user load image and select square area to be cropped. Image will be then scaled down to 256x256 px (in working playlist image is 256x251...)
 
 # Used packages
 - pytest
 - requests
 
 