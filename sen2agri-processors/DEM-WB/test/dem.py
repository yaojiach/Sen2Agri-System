#!/usr/bin/env python
from __future__ import print_function
import argparse
import re
import glob
import gdal
import osr
import subprocess
#import logging
import math
import os
import sys
import pipes
import zipfile


def GetExtent(gt, cols, rows):
    ext = []
    xarr = [0, cols]
    yarr = [0, rows]

    for px in xarr:
        for py in yarr:
            x = gt[0] + px * gt[1] + py * gt[2]
            y = gt[3] + px * gt[4] + py * gt[5]
            ext.append([x, y])
        yarr.reverse()
    return ext


def ReprojectCoords(coords, src_srs, tgt_srs):
    trans_coords = []
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)
    for x, y in coords:
        x, y, z = transform.TransformPoint(x, y)
        trans_coords.append([x, y])
    return trans_coords


def get_dtm_tiles(points):
    """
    Returns a list of dtm tiles covering the given extent
    """
    # extract
    a_x, a_y, b_x, b_y = points
    #logger.debug("points ")
    #logger.debug(points)

    # check a is upper left corner
    if a_x < b_x and a_y > b_y:
        a_bb_x = int(math.floor(a_x / 5) * 5)
        a_bb_y = int(math.floor((a_y + 5) / 5) * 5)
        b_bb_x = int(math.floor((b_x + 5) / 5) * 5)
        b_bb_y = int(math.floor(b_y / 5) * 5)

        print("bounding box {} {} {} {}".format(
            a_bb_x, a_bb_y, b_bb_x, b_bb_y))

        # get list of zip
        x_numbers_list = [((x + 180) / 5) + 1
                          for x in range(min(a_bb_x, b_bb_x), max(a_bb_x, b_bb_x), 5)]
        x_numbers_list_format = ["%02d" % (x,) for x in x_numbers_list]
        y_numbers_list = [(60 - x) / 5
                          for x in range(min(a_bb_y, b_bb_y), max(a_bb_y, b_bb_y), 5)]
        y_numbers_list_format = ["%02d" % (x,) for x in y_numbers_list]

        #logger.debug(x_numbers_list_format)
        #logger.debug(y_numbers_list_format)

        srtm_zips = ["srtm_" + str(x) + "_" + str(y) + ".tif"
                     for x in x_numbers_list_format
                     for y in y_numbers_list_format]

        #logger.debug("zip to take ")
        #logger.debug(srtm_zips)

        print(srtm_zips)

        return srtm_zips


def run_command(args):
    print(" ".join(map(pipes.quote, args)))
    subprocess.call(args)


def get_landsat_tile_id(image):
    m = re.match("[A-Z][A-Z]\d(\d{6})\d{4}\d{3}[A-Z]{3}\d{2}_B\d{1,2}\.TIF", image)
    return m and ('LANDSAT', m.group(1))


def get_sentinel2_tile_id(image):
    m = re.match("\w+_T(\w{5})_B\d{2}\.\w{3}", image)
    return m and ('SENTINEL', m.group(1))


def get_tile_id(image):
    name = os.path.basename(image)
    return get_landsat_tile_id(name) or get_sentinel2_tile_id(name)


class Context(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def format_filename(output_directory, tile_id, suffix):
    filename_template = "L8_TEST_AUX_REFDE2_{0}_0001_{1}.TIF"
    filename_template = "S2__TEST_AUX_REFDE2_{0}____5001_{1}.TIF"
    filename_template = "S2A_TEST_AUX_REFDE2_{0}_0001_{1}.TIF"

    return os.path.join(output_directory,
                        filename_template.format(tile_id, suffix))


def create_context(args):
    mode, tile_id = get_tile_id(args.input)

    dataset = gdal.Open(args.input, gdal.gdalconst.GA_ReadOnly)

    size_x = dataset.RasterXSize
    size_y = dataset.RasterYSize

    geo_transform = dataset.GetGeoTransform()

    spacing_x = geo_transform[1]
    spacing_y = geo_transform[5]

    extent = GetExtent(geo_transform, size_x, size_y)

    source_srs = osr.SpatialReference()
    source_srs.ImportFromWkt(dataset.GetProjection())
    epsg_code = source_srs.GetAttrValue("AUTHORITY", 1)
    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(4326)

    wgs84_extent = ReprojectCoords(extent, source_srs, target_srs)

    swbd_directory = os.path.join(args.working_dir, "swbd")
    if not os.path.exists(swbd_directory):
        os.mkdir(swbd_directory)

    d = dict(image=args.input,
             mode=mode,
             dtm_directory=args.dtm, working_directory=args.working_dir,
             swbd_directory=swbd_directory,
             tile_id=tile_id,
             dem_vrt=os.path.join(args.working_dir, "dem.vrt"),
             dem_nodata=os.path.join(args.working_dir, "dem.tif"),
             dem_coarse=format_filename(args.output, tile_id, "ALC"),
             slope_degrees=os.path.join(args.working_dir, "slope_degrees.tif"),
             aspect_degrees=os.path.join(args.working_dir, "aspect_degrees.tif"),
             slope_coarse=format_filename(args.output, tile_id, "SLC"),
             aspect_coarse=format_filename(args.output, tile_id, "ASC"),
             wb=os.path.join(args.working_dir, "wb.shp"),
             wb_reprojected=os.path.join(
                 args.working_dir, "wb_reprojected.shp"),
             water_mask=format_filename(args.output, tile_id, "MSK"),
             size_x=size_x, size_y=size_y,
             spacing_x=spacing_x, spacing_y=spacing_y,
             extent=extent, wgs84_extent=wgs84_extent,
             epsg_code=epsg_code)

    if mode == 'LANDSAT':
        d['dem_r1'] = format_filename(args.output, tile_id, "ALT")
        d['slope_r1'] = format_filename(args.output, tile_id, "SLP")
        d['aspect_r1'] = format_filename(args.output, tile_id, "ASP")

        d['dem_r2'] = None
        d['slope_r2'] = None
        d['aspect_r2'] = None
    else:
        d['dem_r1'] = format_filename(args.output, tile_id, "ALT_R1")
        d['dem_r2'] = format_filename(args.output, tile_id, "ALT_R2")
        d['slope_r1'] = format_filename(args.output, tile_id, "SLP_R1")
        d['slope_r2'] = format_filename(args.output, tile_id, "SLP_R2")
        d['aspect_r1'] = format_filename(args.output, tile_id, "ASP_R1")
        d['aspect_r2'] = format_filename(args.output, tile_id, "ASP_R2")

    return Context(**d)


def process_DTM(context):
    if abs(context.spacing_x) > abs(context.spacing_y):
        grid_spacing = abs(context.spacing_x)
    else:
        grid_spacing = abs(context.spacing_y)

    dtm_tiles = get_dtm_tiles([context.wgs84_extent[0][0],
                               context.wgs84_extent[0][1],
                               context.wgs84_extent[2][0],
                               context.wgs84_extent[2][1]])

    dtm_tiles = [os.path.join(context.dtm_directory, tile)
                 for tile in dtm_tiles]

    missing_tiles = []
    for tile in dtm_tiles:
        if not os.path.exists(tile):
            missing_tiles.append(tile)

    if missing_tiles:
        print("The following SRTM tiles are missing: {}. Please provide them in the DTM directory ({}).".format(
            [os.path.basename(tile) for tile in missing_tiles], context.dtm_directory))
        sys.exit(1)

    run_command(["gdalbuildvrt",
                 context.dem_vrt] + dtm_tiles)
    run_command(["otbcli_BandMath",
                 "-il", context.dem_vrt,
                 "-out", context.dem_nodata,
                 "-exp", "im1b1 == -32768 ? 0 : im1b1"])
    # run_command(["otbcli_OrthoRectification",
    #              "-io.in", context.dem_nodata,
    #              "-io.out", context.dem_r1,
    #              "-map", "epsg",
    #              "-map.epsg.code", context.epsg_code,
    #              "-outputs.sizex", str(context.size_x),
    #              "-outputs.sizey", str(context.size_y),
    #              "-outputs.spacingx", str(context.spacing_x),
    #              "-outputs.spacingy", str(context.spacing_y),
    #              "-outputs.ulx", str(context.extent[0][0]),
    #              "-outputs.uly", str(context.extent[0][1]),
    #              "-opt.gridspacing", str(grid_spacing)])

    if context.dem_r2:
        run_command(["gdal_translate",
                     "-outsize", str(int(round(context.size_x / 2.0))), str(int(round(context.size_y
                         / 2.0))),
                     context.dem_r1,
                     context.dem_r2])
        # run_command(["otbcli_RigidTransformResample",
        #              "-in", context.dem_r1,
        #              "-out", context.dem_r2,
        #              "-transform.type.id.scalex", "0.5",
        #              "-transform.type.id.scaley", "0.5"])

    if context.mode == 'LANDSAT':
        scale = 1.0 / 8
        inv_scale = 8.0
    else:
        # scale = 1.0 / 23.9737991266  # almost 1/24
        scale = 1.0 / 24
        inv_scale = 24.0

        run_command(["gdal_translate",
                     "-outsize", str(int(round(context.size_x / inv_scale))), str(int(round(context.size_y /
                         inv_scale))),
                     context.dem_r1,
                     context.dem_coarse])
        # run_command(["otbcli_RigidTransformResample",
        #              "-in", context.dem_r1,
        #              "-out", context.dem_coarse,
        #              "-transform.type.id.scalex", str(scale),
        #              "-transform.type.id.scaley", str(scale)])

    run_command(["gdaldem", "slope",
                 # "-s", "111120",
                 "-compute_edges",
                 context.dem_r1,
                 context.slope_degrees])
    run_command(["gdaldem", "aspect",
                 # "-s", "111120",
                 "-compute_edges",
                 context.dem_r1,
                 context.aspect_degrees])

    run_command(["gdal_translate",
                 "-ot", "Int16",
                 "-scale", "0", "90", "0", "157",
                 context.slope_degrees,
                 context.slope_r1])
    run_command(["gdal_translate",
                 "-ot", "Int16",
                 "-scale", "0", "368", "0", "628",
                 context.aspect_degrees,
                 context.aspect_r1])

    if context.slope_r2:
        run_command(["otbcli_Superimpose",
                     "-inr", context.dem_r2,
                     "-inm", context.slope_r1,
                     "-interpolator", "linear",
                     "-lms", "40",
                     "-out", context.slope_r2])

    if context.aspect_r2:
        run_command(["otbcli_Superimpose",
                     "-inr", context.dem_r2,
                     "-inm", context.aspect_r1,
                     "-interpolator", "linear",
                     "-lms", "40",
                     "-out", context.aspect_r2])

    run_command(["otbcli_Superimpose",
                 "-inr", context.dem_coarse,
                 "-inm", context.slope_r1,
                 "-interpolator", "linear",
                 "-lms", "40",
                 "-out", context.slope_coarse])

    run_command(["otbcli_Superimpose",
                 "-inr", context.dem_coarse,
                 "-inm", context.aspect_r1,
                 "-interpolator", "linear",
                 "-lms", "40",
                 "-out", context.aspect_coarse])


def process_WB(context):
    run_command(["otbcli",
                 "DownloadSWBDTiles",
                 "-il", context.image,
                 "-mode.download.outdir", context.swbd_directory])

    for file in glob.glob(os.path.join(context.swbd_directory, "*.zip")):
        # don't use before Python 2.7.4
        with zipfile.ZipFile(file) as zf:
            zf.extractall(context.swbd_directory)

    run_command(["otbcli_ConcatenateVectorData",
                 "-out", context.wb,
                 "-vd"] + glob.glob(os.path.join(context.swbd_directory,
                                                 "*.shp")))

    run_command(["ogr2ogr",
                 "-s_srs", "EPSG:4326",
                 "-t_srs", "EPSG:" + context.epsg_code,
                 context.wb_reprojected,
                 context.wb])

    run_command(["otbcli_Rasterization",
                 "-in", context.wb_reprojected,
                 "-out", context.water_mask, "uint8",
                 "-im", context.dem_coarse,
                 "-mode.binary.foreground", "1"])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Creates DEM and WB data for MACCS")
    parser.add_argument('-i', '--input', required=True, help="input image")
    parser.add_argument('-d', '--dtm', required=True, help="SRTM dataset path")
    parser.add_argument('-w', '--working-dir', required=True,
                        help="working directory")
    parser.add_argument('-o', '--output', required=True, help="output location")

    args = parser.parse_args()

    return create_context(args)

context = parse_arguments()
print(context.tile_id)
process_DTM(context)
process_WB(context)