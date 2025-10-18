from pathlib import Path
import io
import trimesh
from trimesh.path.exchange import load_svg

def svg_string_to_stl(svg_text: str, out_path: str, height: float = 2.0) -> str:
    """
    Convert SVG text to an extruded mesh and write to STL using trimesh.
    """
    svg_io = io.BytesIO(svg_text.encode("utf-8"))
    path2d = load_svg(svg_io)

    # Convert to polygons if supported; create path; extrude
    path2d = path2d.to_polygon() if hasattr(path2d, "to_polygon") else path2d
    if hasattr(path2d, "to_polygons"):
        polygons = path2d.to_polygons()
        p2d = trimesh.path.creation.path_from_polygons(polygons)
    else:
        p2d = path2d

    mesh = p2d.extrude(height)

    # Basic cleanup
    mesh.remove_unreferenced_vertices()
    mesh.merge_vertices()

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(out, file_type="stl")
    return str(out.resolve())
