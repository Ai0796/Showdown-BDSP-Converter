from cx_Freeze import setup, Executable

build_exe_options = {"excludes": ["tkinter", "PyQt4.QtSql", "sqlite3", 
                                  "scipy.lib.lapack.flapack",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "numpy.core._dotblas", 
                                  "PyQt5", "numpy"],
                     "include_files": ["Resources"],
                     "optimize": 2}

setup(
        name = "Showdown Import BDSP",
        version = "1.0",
        options = {"build_exe": build_exe_options},
        description = "Exports masterdatas for easy editing into Pokemon Showdown Style",
        executables = [Executable("Unpack.py"), Executable("Repack.py"), Executable("Verify.py"), Executable("maxAI.py")])