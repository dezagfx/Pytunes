import sys
import os


PY2APP_FREEZER_ON_OSX = True 
APP_NAME = 'pyTunes'
MAIN_SCRIPT_NAME = 'pytunes'
MAIN_SCRIPT = MAIN_SCRIPT_NAME + '.py'


if sys.platform == 'darwin' and PY2APP_FREEZER_ON_OSX:

    from setuptools import setup

    app = [
        MAIN_SCRIPT,
    ]
    
    build_options = {
        'argv_emulation': True,
        'iconfile': '_icons/Books2/Books2.icns',
        'includes': 'sip',
    }

    data_files = [
        MAIN_SCRIPT_NAME + '.ui',
        'book_details.ui', 
    ]

    setup(
        name=APP_NAME,
        version='1.0',
        description='Book catalog viewer',
        app=app,
        data_files=data_files,
        options={'py2app': build_options},
        setup_requires=['py2app'],
    )

else:

    from cx_Freeze import setup, Executable

    # We need to reference the icon in two places:
    # - in the Executable, so that it's inserted into the exe file on
    #   Windows; on Linux the icon is just bundled but that's 
    #   irrelevant because we always need to bundle it manually (read
    #   the next point)
    # - in the files to be copied (include_files), so that QApplication 
    #   loads it as the application icon (the .ico format is also a 
    #   valid Qt image file) and this is required on both platforms
    # icon_file = '_icons/Books2/Books2.ico'
    # base = 'Win32GUI' if sys.platform == 'win32' else None
    base = 'Win32GUI' #if sys.platform == 'win32' else None

    executables = [
        Executable(MAIN_SCRIPT, base=base)
    ]

    build_options = {
        'packages': [], 
        'excludes': [],
        'include_files': [
            
        ],
    }
    if sys.platform == 'linux':
        QT_LIB_PATH = '/opt/Qt/5.5/gcc_64/lib'
        build_options['include_files'].extend([
            MAIN_SCRIPT_NAME + '.linux',
            (os.path.join(QT_LIB_PATH, 'libQt5XcbQpa.so.5'), 'libQt5XcbQpa.so.5'),
            (os.path.join(QT_LIB_PATH, 'libQt5DBus.so.5'), 'libQt5DBus.so.5'),
        ])

    setup(
        name=APP_NAME,
        version='1.0',
        description='Projecto 2 - pyTunes',
        options={'build_exe': build_options},
        executables=executables
    )
