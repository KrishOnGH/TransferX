import os
import sys
import platform
import subprocess
import winreg

name = "TransferX"  # Context menu item name

def add_context_menu_item_windows():
    python_executable = sys.executable
    script_path = os.path.abspath('gui.py')

    # Create context menu for files
    reg_path = r'Software\Classes\*\shell\{}'.format(name)
    command = f'"{python_executable}" "{script_path}" "%1"'
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        winreg.SetValue(key, '', winreg.REG_SZ, name)
        sub_key = winreg.CreateKey(key, r'command')
        winreg.SetValue(sub_key, '', winreg.REG_SZ, command)
        winreg.CloseKey(sub_key)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error adding context menu for files: {e}")

    # Create context menu for folders
    reg_path = r'Software\Classes\Directory\shell\{}'.format(name)
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        winreg.SetValue(key, '', winreg.REG_SZ, name)
        sub_key = winreg.CreateKey(key, r'command')
        winreg.SetValue(sub_key, '', winreg.REG_SZ, command)
        winreg.CloseKey(sub_key)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error adding context menu for folders: {e}")

def remove_context_menu_item_windows():
    reg_paths = [
        r'Software\Classes\*\shell\{}'.format(name),
        r'Software\Classes\Directory\shell\{}'.format(name)
    ]

    for reg_path in reg_paths:
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path + r'\command')
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
            print(f"Removed context menu item: {reg_path}")
        except FileNotFoundError:
            print(f"Context menu item not found: {reg_path}")
        except Exception as e:
            print(f"Failed to remove context menu item {reg_path}: {e}")

def add_context_menu_item_mac():
    service_name = name
    service_path = os.path.expanduser(f"~/Library/Services/{service_name}.workflow")

    if not os.path.exists(service_path):
        os.makedirs(service_path)

    shell_script = f"""#!/bin/bash
python3 "{os.path.abspath('gui.py')}" "$@"
"""
    workflow_script = f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSServicesContextMenuName</key>
    <string>{service_name}</string>
    <key>ServiceDescription</key>
    <string>{name}</string>
    <key>ServiceInputType</key>
    <string>public.file-url</string>
    <key>ServiceInputUUID</key>
    <string>79D5EB25-4384-469E-A1F8-0003C3AE41D6</string>
    <key>ServiceMenuTitle</key>
    <string>{service_name}</string>
    <key>ServiceName</key>
    <string>{service_name}</string>
    <key>actions</key>
    <array>
        <dict>
            <key>actionID</key>
            <string>com.apple.Automator.RunShellScriptAction</string>
            <key>actionName</key>
            <string>Run Shell Script</string>
            <key>actionParameters</key>
            <dict>
                <key>Shell</key>
                <string>/bin/bash</string>
                <key>Script</key>
                <string>{shell_script}</string>
                <key>inputMethod</key>
                <string>as arguments</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
"""

    os.makedirs(os.path.join(service_path, "Contents"), exist_ok=True)
    with open(os.path.join(service_path, "Contents", "Info.plist"), 'w') as f:
        f.write(workflow_script)

    with open(os.path.join(service_path, "Contents", "document.sh"), 'w') as f:
        f.write(shell_script)

    subprocess.run(['chmod', '+x', os.path.join(service_path, "Contents", "document.sh")])

def remove_context_menu_item_mac():
    service_name = name
    service_path = os.path.expanduser(f"~/Library/Services/{service_name}.workflow")

    if os.path.exists(service_path):
        subprocess.run(['rm', '-rf', service_path])
        print(f"Removed service: {service_name}")
    else:
        print(f"Service not found: {service_name}")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        if len(sys.argv) > 1 and sys.argv[1] == 'remove':
            remove_context_menu_item_windows()
        else:
            add_context_menu_item_windows()
    elif platform.system() == 'Darwin':  # macOS
        if len(sys.argv) > 1 and sys.argv[1] == 'remove':
            remove_context_menu_item_mac()
        else:
            add_context_menu_item_mac()
