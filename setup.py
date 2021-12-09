from cx_Freeze import setup, Executable

setup(
        name = "Showdown Import BDSP",
        version = "1.0",
        description = "Exports masterdatas for easy editing into Pokemon Showdown Style",
        executables = [Executable("Extract.py"), Executable("Compress.py")])