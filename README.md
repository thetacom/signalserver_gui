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

Config entries listed below are required.

```
[signalservergui]
data_dir = data
output_dir = downloads
database_dir = db

[signalserver]
path = /usr/bin/signalserver

[convert]
path = /usr/bin/convert
output_type = png
```

- `signalservergui` - Config section with signalservergui settings
  - `data_dir` - Specifies the directory containing various types of data. This option is used to automatically infer the subdirectories for all specific data types.
    - **Example**
      - data_dir = data
      - *(inferred)* elevation_data_dir = data/elevation
      - *(inferred)* lidar_data_dir = data/lidar
      - *(inferred)* user_data_dir = data/user
      - *(inferred)* clutter_data_dir = data/clutter
      - *(inferred)* antenna_profiles_dir = data/antennas
      - *(inferred)* color_profiles_dir = data/color_profiles
      - *(inferred)* color_profile = data/color_profiles/rainbow.dcf
  - `output_dir` - Specifies the directory into which signalservergui will generate files and make available for download.
    - Each time a plot is generate, a subfolder will be created using the plot_id. This folder will contain all files available for that plot.
  - `database_dir` - Specifies the directory where the sqlite database (signalserver_gui.db) will be created.
- `signalserver` - Config section with signalserver settings
  - `path` - Specifies the path to the signal server binary. Signal Server GUI assumes the signalserverHD and signalserverLIDAR binaries are co-located with the base signalserver binary.
    - **Example**
      - path = /usr/bin/signalserver
      - *(inferred)* /usr/bin/signalserverHD
      - *(inferred)* /usr/bin/signalserverLIDAR
- `convert` - Config section with convert settings
  - `path` - Specifies the path to the convert binary. Convert is included with the ImageMagick suite of tools.
  - `output_type` - Specifies the preferred image format for graphics. Recommend `png` to allow image transparency.
### Usage

Starting Signal Server GUI:

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

### Testing

Populate database with sample sites and plots.

**Caution:**
    **Loading test data with re-initialize database and all existing data will be lost.**

```shell
$ cd signalserver_gui
    (No output)
$ source .venv/bin/activate
    (No output)
$ python -m db.test_init