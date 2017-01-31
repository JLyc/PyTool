from winreg import *

Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
RawKey = CreateKey(Registry, "SOFTWARE\Microsoft\Active Setup\Installed Components\StubPath")
