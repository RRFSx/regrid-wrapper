from pathlib import Path

import typer
from pyremap import MpasCellMeshDescriptor

app = typer.Typer()


@app.command()
def main(src_path: Path, dst_path: Path, mesh_name: str = "na15km.init") -> None:
    mpas_desc = MpasCellMeshDescriptor(str(src_path), mesh_name)
    mpas_desc.to_scrip(str(dst_path))


if __name__ == "__main__":
    app()
