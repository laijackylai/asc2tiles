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
@click.option('--max-zoom', prompt='max zoom', default=20, help='maximum zoom level')
# * hk boundaries: [113.825288215, 22.137987659, 114.444071614, 22.57161074] (min_lon, min_lat, max_lon, max_lat)
def main(input_file, skip_rows, min_lat, max_lat, min_lon, max_lon, max_zoom):
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
    for zoom in range(1, max_zoom + 1):
        ll_tile = lat_lon_to_tile(min_lat, min_lon, zoom)
        ur_tile = lat_lon_to_tile(max_lat, max_lon, zoom)
        if(ll_tile != ur_tile):
            print(ll_tile, ur_tile)


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
