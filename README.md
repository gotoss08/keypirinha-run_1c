# Keypirinha Plugin: run_1c

This is `run_1c`, a plugin for the
[Keypirinha](http://keypirinha.com) launcher.


## Download

https://github.com/gotoss08/keypirinha-run_1c/releases


## Build

1. You will need [Keypirinha SDK](https://github.com/Keypirinha/SDK)
2. Set SDK's environment variables with `%sdk_path%/cmd/kpenv.cmd`
3. Build project `%project_path%/build.cmd`


## Install

Once the `run_1c.keypirinha-package` file is installed,
move it to the `InstalledPackage` folder located at:

* `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
* **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode** (the
  final path would look like
  `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)


## Usage

Run **keypirinha**, type `Run 1C`, type valid server base path.

For example: `Run 1C` -> `Srvr="srv-1c:1234";Ref="base";`


## Configuration

In order to use this plugin, you will need 1C to be installed on your computer.

Once 1C is installed, you will need to specify path to `1cestart.exe` file.

You can do this using keypirinha's default configuraion manager: `keypirinha/Configure Package/run_1c`

Default `1cestart.exe` file location set to: `"C:\Program Files\1cv8\common\1cestart.exe"`


## License

This package is distributed under the terms of the MIT license.


## Credits

Author - gotoss08@gmail.com


## Contribute

1. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.
2. Fork this repository on GitHub to start making your changes to the **dev**
   branch.
3. Send a pull request.
4. Add yourself to the *Contributors* section below (or create it if needed)!
