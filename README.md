# Signal Server GUI

Signal Server GUI is designed as a companion to Signal Server. Signal Server GUI provides a simple and intuitive interface to manage the many configuration options available within Signal Server. This web interface allows you to build and save three item types (Stations, Antennas, and Plots). As you develop plots you are afforded opportunity to manipulate some of the many parameters which can affect propagation. Reasonable default values are provided, which can be changed as you develop and refine your model.
## Getting Started

### Installation

Clone repository

```shell
    $ git clone https://github.com/thetacom/signalserver_gui
```

Install external dependencies

- [Signal Server](https://github.com/Cloud-RF/Signal-Server)
- [ImageMagick](https://github.com/ImageMagick/ImageMagick)

Install python dependencies

```shell
$ cd signalserver_gui
    (No output)
$ python -m venv .venv
    (virtual environment creation output)
$ pip install -rrequirements.txt
    (pip installation output)
```

### Configuration

Update required parameters config.ini

```

### Usage

```shell
$ cd signalserver_gui
    (No output)
$ source .venv/bin/activate
    (No output)
$ python -m signalserver_gui
    (Bottle server console log)...
    Listening on http://localhost:8080/
```

Once signalserver_gui is running, open a browser to the url indicated
in the console log. 
    Example: http://localhost:8080/