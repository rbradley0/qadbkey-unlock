# Quectel EG25-G ADBKEY Unlock script

As the README title suggests, this is a simple python script that can be used to generate a `QADBKEY` for the Quectel EG25-G modem used in the [PinePhone](https://www.pine64.org/pinephone/). The original source by igem can be found [here](https://xnux.eu/devices/feature/qadbkey-unlock.c)

### How To Use

To use this script, you must have the following:

* Some variant of Linux, macOS, BSD, whatever... as long as it's not Windows, this script should work.
* `Python >= 3`
* `pySerial >= 3.5`
* A `QADBKEY` for the input, read [here](https://xnux.eu/devices/feature/modem-pp.html) under the `Unlock ADB Access` section.

Enter the virtualenv and install the required Python dependencies using:

```sh
$ python -m venv .venv # generates a python virtualenv...
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

Once you have obtained the prerequisites, run the script with either of the following commands:

```sh
$ ./qadbkey-unlock.py -d <device> [-b <baudrate> -t <timeout>] # device is usually /dev/ttyUSB2 @ 115200 baud on PinePhone.
...OR...
$ python qadbkey-unlock.py -d <device> [-b <baudrate> -t <timeout>] # device is usually /dev/ttyUSB2 @ 115200 baud on PinePhone.
```

### Contributors

* [hornetfighter515](https://github.com/hornetfighter515) — Basic script structure and debugging.
* [Ryan Bradley](https://github.com/rbradley0) – Tweaking and debugging.
