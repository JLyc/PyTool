import subprocess

subprocess.call(["SIGNTOOL.EXE", "sign", "/F", "MDM_cert.pfx", "/P", "nbusr123", "/T",
                 "http://timestamp.digicert.com",
                 '[A0119]_Powershell_CurrentUser_AllHosts_profile_modified6.exe', ])