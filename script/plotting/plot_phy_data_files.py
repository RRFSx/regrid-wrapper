import glob
from pathlib import Path

from regrid_wrapper.geom.grid import Grid
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def main() -> None:
    # output_dir = Path(r"C:\Users\bkozi\Dropbox\rlps\rsandbox\regrid-wrapper\data\plots")
    # root_dir = Path(r"C:\Users\bkozi\Dropbox\rlps\rsandbox\regrid-wrapper\data")
    output_dir = Path("/home/Benjamin.Koziol/htmp/phyf-plots")
    root_dir = Path(
        "/scratch1/NCEPDEV/stmp2/Benjamin.Koziol/sandbox/srw/benkozi/develop/expt_dirs/smoke_dust_conus3km"
    )

    slug = "**/*phyf*nc"
    filenames = glob.glob(slug, root_dir=root_dir, recursive=True)
    for ctr, filename in enumerate(filenames):
        path = root_dir / filename
        print(path)
        grid = Grid(path=path, lat_name="grid_latt", lon_name="grid_lont")
        # grid = Grid(path=path, lat_name="geolat", lon_name="geolon")
        # print(grid.describe())

        # Create a figure and set the projection
        fig, ax = plt.subplots(
            figsize=(8, 6), subplot_kw={"projection": ccrs.PlateCarree()}
        )

        # Add map features
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=":")
        ax.add_feature(cfeature.STATES)
        ax.gridlines(draw_labels=True)

        lon_grid = grid.get(grid.lon_name)
        lat_grid = grid.get(grid.lat_name)
        data = grid.get("ebu_smoke")
        data = data[0, :, :, :]
        mesh = ax.pcolormesh(
            lon_grid,
            lat_grid,
            data,
            cmap="viridis",
            shading="auto",
            transform=ccrs.PlateCarree(),
        )

        ax.set_extent(grid.get_bounding_box().get_padded_extent(5))

        plt.title(grid.path.name)

        cbar = plt.colorbar(mesh, ax=ax, orientation="vertical", shrink=0.7, pad=0.05)
        cbar.set_label("Data Values")

        plt.savefig(output_dir / f"{ctr}-{path.name}.png")
        # plt.show()


if __name__ == "__main__":
    main()
