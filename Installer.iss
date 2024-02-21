#define MyAppName "Scares Scrambler S"
#define MyAppVersion "Build 22"
#define MyAppPublisher "scares009"
#define MyAppURL "https://github.com/Cocoatwix/Scares-Scrambler-S"
#define MyAppExeName "Scrambler.py"

[Setup]
AppId={{900D4AAE-7773-4811-BB61-019837747139}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=.
OutputBaseFilename={#MyAppName} Setup
Compression=lzma2/max
SolidCompression=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=classic

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Scrambler.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "Engine.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "Themes.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "Assets\banner.png"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\darkBanner.png"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\darkLogo.png"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\dubbyBanner.png"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\dubbyLogo.jpg"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\dubbyLogo.png"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\favi.ico"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\favi.xbm"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\logo.png"; DestDir: "{app}\Assets"; Flags: ignoreversion
Source: "Assets\Streak_Icon.png"; DestDir: "{app}\Assets"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
