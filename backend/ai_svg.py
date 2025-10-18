from textwrap import dedent

def generate_svg_from_prompt(prompt: str) -> str:
    """
    MVP stub: returns a simple SVG outline based on keywords.
    Replace this later with a real AI SVG generator (OpenAI / Replicate).
    """
    p = prompt.lower()
    if "heart" in p:
        path_d = "M10,30 C-20,-10 40,-10 10,10 C-20,-10 40,-10 10,30 Z"
        viewbox = "-10 -20 60 60"
    elif "bone" in p or "dog" in p:
        path_d = "M0,10 C-5,8 -5,2 0,0 H30 C35,2 35,8 30,10 H0 Z"
        viewbox = "-10 -10 60 30"
    else:
        # default circle
        return dedent("""\
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="-20 -20 140 140">
          <circle cx="50" cy="50" r="50" />
        </svg>""")
    return dedent(f"""\
    <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="{viewbox}">
      <path d="{path_d}" />
    </svg>""")
