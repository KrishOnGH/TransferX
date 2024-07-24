import os
import sys
import winreg

def add_context_menu_item():
    python_executable = sys.executable
    script_path = os.path.abspath('gui.pyw')

    # Create context menu for files
    reg_path = r'Software\Classes\*\shell\TransferX'
    command = f'"{python_executable}" "{script_path}" "%1"'
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        winreg.SetValue(key, '', winreg.REG_SZ, 'TransferX')
        sub_key = winreg.CreateKey(key, r'command')
        winreg.SetValue(sub_key, '', winreg.REG_SZ, command)
        winreg.CloseKey(sub_key)
        winreg.CloseKey(key)
    except Exception as e:
        pass

    # Create context menu for folders
    reg_path = r'Software\Classes\Directory\shell\TransferX'
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        winreg.SetValue(key, '', winreg.REG_SZ, 'TransferX')
        sub_key = winreg.CreateKey(key, r'command')
        winreg.SetValue(sub_key, '', winreg.REG_SZ, command)
        winreg.CloseKey(sub_key)
        winreg.CloseKey(key)
    except Exception as e:
        pass

def remove_context_menu_item():
    reg_paths = [
        r'Software\Classes\*\shell\TransferX',
        r'Software\Classes\Directory\shell\TransferX'
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

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'remove':
        remove_context_menu_item()
    else:
        add_context_menu_item()
