import numpy as np
import click
import math


@click.command()
@click.option('--input-file', prompt='input file', default='test.asc', help='input file path', show_default=True)
@click.option('--skip-rows', prompt='rows to skip for the asc file', default=6, help='rows to skip if input is an ascii file')
@click.option('--min-lat', prompt='min lat', default=22.137987659, help='minimum latitude of the input data')
@click.option('--max-lat', prompt='max lat', default=22.57161074, help='maximum latitude of the input data')
@click.option('--min-lon', prompt='min lon', default=113.825288215, help='minimum longitude of the input data')
@click.option('--max-lon', prompt='max lon', default=114.444071614, help='maximum longitude of the input data')
@click.option('--max-zoom', prompt='max zoom', default=15, help='maximum zoom level')
@click.option('--detail', prompt='detail level', default=0.5, help='detail level decrease per zoom level')
# * hk boundaries: [113.825288215, 22.137987659, 114.444071614, 22.57161074] (min_lon, min_lat, max_lon, max_lat)
def main(input_file, skip_rows, min_lat, max_lat, min_lon, max_lon, max_zoom, detail):
    """main function"""
    check_file_type(input_file)

    asc_data = np.loadtxt(input_file, skiprows=skip_rows)
    data_shape = np.shape(asc_data)
    lat_2d = get_lat(data_shape, min_lat, max_lat)
    lon_2d = get_lon(data_shape, min_lon, max_lon)
    get_tiles(min_lat, max_lat, min_lon, max_lon, max_zoom)
    # load_and_parse_asc(input_file, skip_rows)


def get_lat(shape, min_lat, max_lat):
    step = (max_lat - min_lat) / shape[0]
    arr = np.arange(start=min_lat, stop=max_lat, step=step)
    arr2d = np.repeat(arr[:, np.newaxis], shape[1], axis=1)
    return arr2d


def get_lon(shape, min_lon, max_lon):
    step = (max_lon - min_lon) / shape[1]
    arr = np.arange(start=min_lon, stop=max_lon, step=step)
    arr2d = np.repeat(arr[:, np.newaxis], shape[1], axis=1)
    return arr2d.T


def get_tiles(min_lat, max_lat, min_lon, max_lon, max_zoom):
    """get the metadata on how to slice the input"""
    for z in reversed(range(1, max_zoom + 1)):
        ll_tile = lat_lon_to_tile(min_lat, min_lon, z)
        ur_tile = lat_lon_to_tile(max_lat, max_lon, z)
        if(ll_tile != ur_tile):
            x_tile_range = np.array([ll_tile[0], ur_tile[0]])
            y_tile_range = np.array([ur_tile[1], ll_tile[1]])
            for x in range(x_tile_range[0], x_tile_range[1] + 1):
                for y in range(y_tile_range[0], y_tile_range[1] + 1):
                    tl_corner = num2deg(x, y, z)
                    tr_corner = num2deg(x + 1, y, z)
                    bl_corner = num2deg(x, y + 1, z)
                    br_corner = num2deg(x + 1, y + 1, z)
                    print(tl_corner, tr_corner, bl_corner, br_corner)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def lat_lon_to_tile(lat_deg, lon_deg, zoom):
    """translate lat lon to it's corresponding tile numbers with zoom level"""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def check_file_type(input_file):
    """check whether the input file type is the same as actual input file type"""
    actual_file_type = input_file.split('.')[1]
    if(actual_file_type != 'asc'):
        print('File type not matched!')
        exit()


def load_and_parse_asc(input_file, skip_rows):
    """load data from input asc file"""
    print('loading asc file...')
    asc_data = np.loadtxt(input_file, skiprows=skip_rows)
    print(np.shape(asc_data))


if __name__ == '__main__':
    main()
