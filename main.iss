; Kurulum Bilgileri
[Setup]
AppName=mdkaresofthydrandcrunch
AppVersion=1.2
DefaultDirName={pf}\mdkaresofthydrandcrunch
DefaultGroupName=mdkaresofthydrandcrunch
OutputDir=output
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

; Çalıştırılabilir Dosya
[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
; Gerekli Python ve Kütüphane Yükleyicileri
Source: "C:\Users\mehme\Desktop\python-3.13.1-amd64.exe"; DestDir: "{tmp}"; Flags: ignoreversion
; Gerekli kütüphane dosyalarını indirmeniz ve burada eklemeniz gerekebilir.

; Masaüstü Kısayolu Oluşturma
[Icons]
Name: "{userdesktop}\mdkaresofthydrandcrunch"; Filename: "{app}\main.exe"

; Python ve Gerekli Kütüphaneleri Yüklemek İçin Çalıştırma Komutları
[Run]
Filename: "{tmp}\python-3.9.5.exe"; Parameters: "/quiet InstallAllUsers=1 PrependPath=1"
Filename: "{app}\main.exe"; Description: "mdkaresofthydrandcrunch'i Başlat"; Flags: nowait postinstall skipifsilent
