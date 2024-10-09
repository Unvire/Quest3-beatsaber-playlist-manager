import subprocess

result = subprocess.run(["adb/adb", "shell", "ls", "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongCore/CustomLevels"], capture_output=True, text=True)

output = result.stdout

print(output)

files_and_folders = output.splitlines()
for name in files_and_folders:
    print(name)
