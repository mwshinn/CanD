# Fontant
import matplotlib
from matplotlib.font_manager import findSystemFonts
from matplotlib import ft2font
import os

def get_fonts():
    # Get default matplotlib paths
    paths = [os.path.join(matplotlib.get_data_path(), 'fonts', subdir)
             for subdir in ['ttf', 'afm', 'pdfcorefonts']]
    # Get paths from OS
    for pathname in ['TTFPATH', 'AFMPATH']:
        if pathname in os.environ:
            ttfpath = os.environ[pathname]
            if ttfpath.find(';') >= 0:  # win32 style
                paths.extend(ttfpath.split(';'))
            elif ttfpath.find(':') >= 0:  # unix style
                paths.extend(ttfpath.split(':'))
            else:
                paths.append(ttfpath)
    # "ttf" here means "otf" and "ttc" too
    fonts_ttf_mpl = findSystemFonts(paths, fontext="ttf")
    fonts_ttf_sys = findSystemFonts(fontext="ttf")
    # We are going to try to avoid postscript fonts at all costs
    # fonts_afm_mpl = font_manager.findSystemFonts(paths, fontext="afm")
    # fonts_afm_sys = font_manager.findSystemFonts(fontext="afm")
    return fonts_ttf_mpl + fonts_ttf_sys# + fonts_afm_mpl + fonts_afm_sys

WEIGHTS = {
    # Originally from fontconfig's FcFreeTypeQueryFaceInternal, here backported
    # from latest matplotlib
    "thin": 100,
    "extralight": 200,
    "extra light": 200,
    "ultralight": 200,
    "ultra light": 200,
    "demilight": 350,
    "demi light": 350,
    "semilight": 350,
    "semi light": 350,
    "light": 300,  # Needs to come *after* demi/semilight!
    "book": 380,
    "regular": 400,
    "roman": 400,
    "normal": 400,
    "medium": 500,
    "demibold": 600,
    "demi": 600,
    "semibold": 600,
    "extrabold": 800,
    "extra bold": 800,
    "superbold": 800,
    "super bold": 800,
    "ultrabold": 800,
    "ultra bold": 800,
    "bold": 700,  # Needs to come *after* extra/super/ultrabold!
    "ultrablack": 1000,
    "ultra black": 1000,
    "superblack": 1000,
    "super black": 1000,
    "extrablack": 1000,
    "extra black": 1000,
    "ultra": 1000,
    "black": 900,  # Needs to come *after* ultra/super/extrablack!
    "heavy": 900,
}

STRETCH = {
    'ultracondensed':  -1,
    'ultra-condensed': 1,
    'extracondensed':  -1,
    'extra-condensed': 2,
    'narrow':          -1,
    'condensed':       3,
    'semicondensed':   -1,
    'semi-condensed':  4,
    'normal':          5,
    'semiexpanded':    -1,
    'semi-expanded':   6,
    'semiextended':    -1,
    'semi-extended':   -1,
    'expanded':        7,
    'extended':        -1,
    'extraexpanded':   -1,
    'extra-expanded':  8,
    'extraextended':   -1,
    'extra-extended':  -1,
    'ultraexpanded':   -1,
    'ultra-expanded':  9,
    'ultraextended':   -1,
    'ultra-extended':  -1,
}

SPECIALS = [
    'sc',
    'caps',
    'alt',
]

FOUNDRIES = {
    "Adobe": "Adobe",
    "Bigelow": "B&H",
    "Bitstream": "Bitstream",
    "Gnat": "Culmus",
    "Iorsh": "Culmus",
    "HanYang System": "Hanyang",
    "Font21": "Hwan",
    "Google": "Google",
    "IBM": "IBM",
    "International Typeface Corporation": "ITC",
    "ITC": "ITC",
    "Linotype": "Linotype",
    "LINOTYPE-HELL": "Linotype",
    "Microsoft": "Microsoft",
    "Monotype": "Monotype",
    "Omega": "Omega",
    "STIX": "STIX",
    "TeX": "TeX",
    "Tiro Typeworks": "Tiro",
    "URW": "URW",
    "XFree86": "XFree86",
    "Xorg": "Xorg",
}

FOUNDRIES_NAME = {
    "Adobe": "Adobe",
    "A2": "A2",
    "ADF": "Arkandis",
    "AEF": "Altered Ego Fonts",
    "AS": "Alphabet Soup",
    "AT": "Agfa",
    "BT": "Bitstream",
    "CC": "Comicraft",
    "CG": "Compugraphic",
    "EF": "Elsner+Flake",
    "FB": "Font Bureau",
    "F2F": "Face2Face",
    "FF": "FontFont",
    "FP": "FontPartners",
    "FTN": "Fountain",
    "GFS": "Greek Font Society",
    "ITC": "ITC",
    "LFT": "Leftloft",
    "LP": "Letter Perfect",
    "LT": "Linotype",
    "LTC": "Lanston",
    "MT": "Monotype",
    "MVB": "MVB",
    "ND": "Neufville Digital",
    "P22": "P22",
    "PL": "Photo Lettering",
    "PT": "Paratype",
    "PTF": "Porchez",
    "PTL": "Primetype",
    "RB": "Richard Beatty",
    "RTF": "Rimmer",
    "SG": "Scangraphic",
    "TC": "Typesettra",
    "URW": "URW++",
    "URW++": "URW++",
    "WTC": "WTC",
}

OPTICAL_SIZES = ["display", "caption", "subhead", "re",
                 "text", "headline", "banner", "micro", "deck"]

def get_property(font, props):
    PROPS = {
        "ps_notice": ("ps", 1), # Copyright notice
        "ps_fullname": ("ps", 2),
        "ps_familyname": ("ps", 3),
        "ps_weight": ("ps", 4),
        "ps_italicangle": ("ps", 5),
        "ps_monospace": ("ps", 6),
        "os2_vendorid": ("os2", "achVendID"),
        "os2_widthclass": ("os2", "usWidthClass"),
        "os2_weightclass": ("os2", "usWeightClass"),
        #"os2_familytype": ("panose", 0), # panose is a weird string from the OS/2 table
        #"os2_weight": ("panose", 2),
        "sfnt_copyright": ("sfnt", 0),
        "sfnt_family": ("sfnt", 1), # Only four fonts can share this: normal, italic/oblique, bold, and bold+italic/oblique.  For fonts with more variants, use 16 and 17.
        "sfnt_subfamily": ("sfnt", 2), # For style and weight variants only
        "sfnt_identifier": ("sfnt", 3), # Unique font identifier
        "sfnt_fullname": ("sfnt", 4), # Combines 1/2/16/17, but only when each of these is relevant (e.g. "regular" is not relevant for Arial Black)
        "sfnt_version": ("sfnt", 5), # Version string
        "sfnt_postscriptname": ("sfnt", 6),
        "sfnt_trademark": ("sfnt", 7),
        "sfnt_manufacturer": ("sfnt", 8),
        "sfnt_designer": ("sfnt", 9),
        "sfnt_description": ("sfnt", 10),
        "sfnt_vendorurl": ("sfnt", 11),
        "sfnt_designerurl": ("sfnt", 12),
        "sfnt_licensedescription": ("sfnt", 13), # In plain English, describe how the font can be used
        "sfnt_licenseurl": ("sfnt", 14),
        "sfnt_typographicfamily": ("sfnt", 16), # Just the overall font name with no subtypes included, e.g. "Helvetica Neue LT"
        "sfnt_typographicsubfamily": ("sfnt", 17), # All subtypes, e.g. "Semibold Caption Thin"
        "sfnt_wwsfamily": ("sfnt", 21), # Base name and everything except weight and italics
        "sfnt_wwssubfamily": ("sfnt", 22), # Weight and italic style
    }
    # For example, Minion Pro Semibold Italic Caption:
    # sfnt_familyname:           Minion Pro SmBd Capt
    # sfnt_subfamilyname:        Italic
    # sfnt_typographicfamily:    Minion Pro
    # sfnt_typographicsubfamily: Semibold Italic Caption
    # sfnt_wwsfamily:            Minion Pro Caption
    # sfnt_wwssubfamily:         Semibold Italic
    # For more info see https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
    # For more info on postscript fields, see:
    # https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html
    # https://docs.microsoft.com/en-us/typography/opentype/spec/post


    returns = []
    returnstr = False
    if isinstance(props, str):
        props = [props]
        returnstr = True
    for prop in props:
        table, key = PROPS[prop]
        if table == "ps":
            try:
                psinfo = font.get_ps_font_info()
                returns.append(psinfo[key])
            except:
                pass
        elif table == "os2":
            os2 = font.get_sfnt_table("OS/2")
            if os2 and os2['version'] != 0xffff:
                if os2.get(key, ""):
                    returns.append(os2[key])
        elif table == "sfnt":
            sfnt_name = font.get_sfnt()
            keyval = sfnt_name.get((3,1,1033,key), b"").decode('utf_16_be')
            if keyval:
                returns.append(keyval)
            else:
                keyval = sfnt_name.get((1,0,0,key), b"").decode('latin-1')
                if keyval:
                    returns.append(keyval)
        else:
            raise ValueError("Invalid property passed: "+prop)
    if returnstr:
        return returns[0] if len(returns) == 1 else None
    return returns

def get_familyname(font):
    names = get_property(font, ["sfnt_typographicfamily", "ps_familyname",
                                "sfnt_family", "sfnt_wwsfamily", "ps_fullname",
                                "sfnt_fullname"])
    return (names+[""])[0]

def get_fullname(font):
    names = get_property(font, ["ps_fullname", "sfnt_fullname"])
    return (names+[""])[0]

def get_style(font):
    # First check the fields devoted to this.  Even though the sfnt
    # subfamily is supposed to have the best version of this information, we
    # check the postscript full font name first because sometimes the others
    # mix up italic and oblique.  If "oblique" is in the full name, we know for
    # sure it shouldn't be italic.
    familynames = get_property(font, ["ps_fullname", "sfnt_typographicsubfamily",
                                      "sfnt_wwssubfamily", "sfnt_subfamily",
                                      "sfnt_fullname"])
    for familyname in familynames:
        for style in ["italic", "oblique", "kursiv"]:
            if style in familyname.lower().replace("-", " ").split(" "):
                return style
    # Now check properties of the font
    if font.style_flags & ft2font.ITALIC:
        return "italic"
    # if get_property(font, "ps_italicangle") != 0:
    #     return "italic"
    return "normal"

def get_monospace(font):
    # First check if it is in postscript information.  If so, this makes our
    # life easy.
    ismono = get_property(font, "ps_monospace")
    if ismono is not None:
        return bool(ismono)
    # If not, use the font object
    return bool(font.face_flags & ft2font.FIXED_WIDTH)
    # # If not, let's render two characters that should be different widths.  If
    # # they are the same width, we can assume the font is monospace.
    # font.set_text(".")
    # width_dot = font.get_width_height()[0]
    # font.set_text("M")
    # width_M = font.get_width_height()[0]
    # return (width_dot == width_M)


def get_foundry(font):
    # First try to extract it from the name
    names = get_property(font, ["sfnt_typographicfamily", "sfnt_family",
                                "ps_familyname", "ps_fullname", "sfnt_fullname"])
    for name in names:
        for abbrev,fname in FOUNDRIES_NAME.items():
            if abbrev in name.replace("-", " ").split(" "):
                return fname
    # Then extract from "manufacturer" text
    manufac = get_property(font, "sfnt_manufacturer")
    if manufac:
        for ftext,fname in FOUNDRIES.items():
            if ftext in manufac:
                return fname
        return manufac
    # Now look in license text
    licensetexts = get_property(font, ["sfnt_trademark", "ps_notice",
                                       "sfnt_copyright"])
    for licensetext in licensetexts:
        for ftext,fname in FOUNDRIES.items():
            if ftext in licensetext:
                return fname
        for fname in FOUNDRIES_NAME.values():
            if fname in licensetext:
                return fname
    return ""

def get_opticalsize(font):
    # The only way I can find to get this is from the name.
    names = get_property(font, ["sfnt_typographicsubfamily",
                                "sfnt_wwsfamily", "sfnt_family",
                                "ps_fullname", "sfnt_fullname"])
    for name in names:
        for opsz in OPTICAL_SIZES:
            if opsz in name.lower().replace("-", " ").split(" "):
                return opsz
    return "normal"

def get_stretch(font):
    # First try based on the name
    names = get_property(font, ["sfnt_typographicsubfamily",
                                "sfnt_wwsfamily", "sfnt_family",
                                "ps_fullname", "sfnt_fullname"])
    for name in names:
        for stretch in STRETCH.keys():
            if stretch in name.lower().replace("-", " ").split(" "):
                return stretch
    # If the name failed, then try using os2 information
    width = get_property(font, "os2_weightclass")
    if width:
       for stretch,val in STRETCH.items():
           if val == width:
               return stretch
    return "normal"

def get_weightnumber(font):
    # First try the OS/2 table weight class
    os2weight = get_property(font, "os2_weightclass")
    if os2weight:
        return os2weight
    # Otherwise, try to get it from the name
    weightname = get_weight(font)
    return WEIGHTS.get(weightname, None)

def get_weight(font):
    # First, try to extract it from the font name
    weightnames = get_property(font, ["sfnt_typographicsubfamily",
                                      "sfnt_subfamily", "sfnt_wwssubfamily",
                                      "ps_fullname", "sfnt_fullname"])
    for weightname in weightnames:
        for w in WEIGHTS.keys():
            if w in weightname.lower().replace("-", " ").split(" ") or \
               (" " in w and w in weightname.lower()): # Some weight names have spaces
                return w
    # Now try postscript weight.  We don't do this first because this field is
    # often wrong.
    weight = get_property(font, "ps_weight")
    if weight:
        return weight.lower()
    # As a last ditch, look at flags
    if font.style_flags & ft2font.BOLD:
        return "bold"
    return "regular"

def get_identifier(font):
    # First, get the item guaranteed to be a unique identifier
    uniqueid = get_property(font, "sfnt_identifier")
    if uniqueid:
        return uniqueid
    # If that doesn't work, just use the filename and call it a day.
    return os.path.split(font.fname)[-1]

def get_special(font):
    varnames = get_property(font, ["sfnt_typographicsubfamily",
                                   "sfnt_subfamily", "sfnt_wwssubfamily",
                                   "ps_fullname", "sfnt_fullname"])
    allspecs = []
    for varname in varnames:
        for s in SPECIALS:
            if s in varname.lower().replace("-", " ").split(" "):
                allspecs.append(s)
    if allspecs:
        return " ".join(sorted(set(allspecs)))
    else:
        return "none"

def get_version(font):
    return get_property(font, "sfnt_version")

def get_base_style(font):
    base_style = font.style_flags
    # Sometimes italic/bold versions are mistakenly detected as base_style 0.
    if base_style == 0:
        if get_weight(font) == "bold":
            base_style += 2
        if get_style(font) != "normal":
            base_style += 1
    return base_style

def loadttf(path):
    try:
        font = ft2font.FT2Font(path)
    except RuntimeError:
        return None
    props = {
        "fname": font.fname,
        "full_name": get_fullname(font),
        "postscript_name": font.postscript_name,
        "family_name": get_familyname(font),
        "style": get_style(font),
        "weight": get_weight(font),
        "weight_number": get_weightnumber(font),
        "foundry": get_foundry(font),
        "stretch": get_stretch(font),
        "opticalsize": get_opticalsize(font),
        "monospace": get_monospace(font),
        "identifier": get_identifier(font),
        "version": get_version(font),
        "special": get_special(font),
        "num_faces": font.num_faces,
        "base_style": get_base_style(font), # 0 = regular, 1 = italic, 2 = bold, 3 = bolditalic
    }
    return props

class NoFontFoundError(ValueError):
    pass

class MultipleFontsFoundError(ValueError):
    pass

_find_font_cache = {}

def find_font(name, *, weight=None, style=None, stretch=None, opticalsize=None, monospace=None, foundry=None, special=None, multiple=False):
    global _find_font_cache
    cachename = (name, weight, style, stretch, opticalsize, monospace, foundry, special, multiple)
    if cachename in _find_font_cache.keys():
        return _find_font_cache[cachename]
    # Check if they passed a filename for the name.  If so, return that.
    if name is not None and os.path.isfile(name):
        loadedttf = loadttf(name)
        if loadedttf is None:
            print(f"Warning: font path {name} could not be loaded, trying a more thorough search")
        else:
            _find_font_cache[cachename] = loadedttf
            return loadedttf
    # If not, firs, find all fonts which contain the specified name as a
    # substring.  This first expression uses the "for lf in [...]" hack like a
    # "let" statement in lisp so that we can still use list comprehensions and
    # filter for None without running the loadttf function twice.  (I think
    # there might be special syntax for this in newer versions of Python?)
    fonts = [lf for p in get_fonts() for lf in [loadttf(p)] if lf is not None]
    fonts = [f for f in fonts if name.lower() in f["full_name"].lower() or
                                 name.lower() in f["family_name"].lower() or
                                 name.lower() in f["postscript_name"].lower()]
    if len(fonts) == 0:
        raise NoFontFoundError("Invalid font name")
    # Next, try to narrow it down based on family name.
    _fonts = [f for f in fonts if name.lower() in f["family_name"].lower()]
    fonts = _fonts or fonts
    # Next, check if there is an exact match in full name, family name, or postscript name
    _fonts = [f for f in fonts if name.lower() in [f["family_name"].lower(),
                                                   f["full_name"].lower(),
                                                   f["postscript_name"].lower()]]
    fonts = _fonts or fonts
    # Now we filter by each of the properties which was passed as an argument
    def filter_if_exists(fonts, prop, val):
        lower = lambda x : x.lower() if isinstance(x, str) else x
        if val is None:
            return fonts
        allprops = set(lower(f[prop]) for f in fonts)
        if lower(val) in allprops:
            return [f for f in fonts if lower(val) == lower(f[prop])]
        else:
            errortext = f"No selected fonts have {prop} = \"{val}\", options are:\n    "
            errortext += ", ".join(f'"{p}"' for p in sorted(allprops))
            raise NoFontFoundError(errortext)
    if isinstance(weight, int):
        fonts = filter_if_exists(fonts, "weight_number", weight)
    elif isinstance(weight, str):
        fonts = filter_if_exists(fonts, "weight", weight)
    fonts = filter_if_exists(fonts, "stretch", stretch)
    fonts = filter_if_exists(fonts, "monospace", monospace)
    fonts = filter_if_exists(fonts, "opticalsize", opticalsize)
    fonts = filter_if_exists(fonts, "foundry", foundry)
    fonts = filter_if_exists(fonts, "special", special)
    # We want "italic" to fall back to "oblique".  We don't need the reverse.
    try:
        fonts = filter_if_exists(fonts, "style", style)
    except NoFontFoundError as e:
        if style == "italic":
            try:
                fonts = filter_if_exists(fonts, "style", "oblique")
            except NoFontFoundError as e2:
                raise e
        else:
            raise e
    # If there is more than one option, give the user a chance to narrow it down.
    if len(fonts) > 1 and not multiple:
        differing_props = []
        for prop in ["family_name", "weight", "weight_number", "stretch", "monospace",
                     "opticalsize", "style", "foundry", "special"]:
            allprops = set(f[prop] for f in fonts)
            if len(allprops) > 1:
                if prop == "weight_number":
                    prop = "weight"
                differing_props.append((prop, allprops))
        if len(differing_props) > 0:
            errortext = "Multiple matching fonts, please specify one or more of the following:\n"
            errortext += "\n".join([f"    '{prop}' is one of: {sorted(vals)}"
                                    for prop,vals in differing_props])
            raise MultipleFontsFoundError(errortext)
        else:
            fonts = sorted(fonts, key=lambda x : x['fname'])
            warningtext = "Warning: Multiple versions of the specified font are installed:\n"
            for f in fonts:
                warningtext += "    " + f['fname'] + "\n"
            warningtext += "We are arbitrarily choosing:"
            warningtext += "    " + fonts[0]['fname'] + "\n"
            matchingfonts = fonts[0:1]
            print(warningtext)
    if multiple:
        loadedttf = fonts
    else:
        loadedttf = fonts[0]
    _find_font_cache[cachename] = loadedttf
    return loadedttf

_find_font_family_cache = {}
def find_font_family(name, *, stretch=None, opticalsize=None, monospace=None, foundry=None, special=None):
    global _find_font_family_cache
    cachename = (name, stretch, opticalsize, monospace, foundry, special)
    if cachename in _find_font_family_cache.keys():
        return _find_font_family_cache[cachename]
    # Get all the fonts which match the user's search criteria
    allfonts = find_font(name, stretch=stretch, opticalsize=opticalsize, monospace=monospace, foundry=foundry, special=special, multiple=True)
    # Check to make sure that only one family was returned.
    familynames = list(sorted(set([f['family_name'] for f in allfonts])))
    if len(familynames) > 1:
        errortext = "Please be more specific in specifying font family.\nSpecify one of the following font names:\n    "
        errortext += ", ".join(f'"{f}"' for f in familynames)
        foundries = list(sorted(set([f['foundry'] for f in allfonts])))
        if len(foundries) > 1:
            errortext += "\nor one of the following foundries:\n    "
            errortext += ", ".join(f'"{f}"' for f in foundries)
        raise MultipleFontsFoundError(errortext)
    # Now we try to prune everything down to just one font.  We start by making
    # sure there is only one stretch and optical size.
    opticalsizes = set(f['opticalsize'] for f in allfonts)
    if len(opticalsizes) > 1:
        errortext = "Please specify an optical size using the function argument opticalsize=[value].  Valid values for this font are:\n    "
        errortext += ", ".join(f'"{os}"' for os in opticalsizes)
        raise MultipleFontsFoundError(errortext)
    stretches = set(f['stretch'] for f in allfonts)
    if len(stretches) > 1:
        errortext = "Please specify a stretch using the function argument stretch=[value].  Valid values for this font are:\n    "
        errortext += ", ".join(f'"{s}"' for s in stretches)
        raise MultipleFontsFoundError(errortext)
    def find_member(allfonts, bold, italic):
        basestyle = 0
        if bold:
            basestyle += 2
            weights = ["bold", "semibold"]
        else:
            weights = ["roman", "normal", "book", "regular", "medium"]
        if italic:
            basestyle += 1
            styles = ['italic', 'oblique']
        else:
            styles = ['normal']
        # Now let's try to find the base font for this family.  We will do this
        # by slowly pruning the list down to only one font.  The "base_style"
        # should be 0 for the base font, so we check that first.
        matchingfonts = [f for f in allfonts if f['base_style'] == basestyle]
        # If that didn't narrow it down, first filter out all of the italic fonts,
        # assuming there is at least one non-italic font.
        if len(matchingfonts) > 1 and len(set(f['style'] for f in matchingfonts)) > 1:
            # This would fail if a font family only had italic and oblique with a
            # base_style of 0, but the chance of a font designer screwing up so
            # badly is very low.
            matchingfonts = [f for f in matchingfonts if f['style'] in styles]
        # Next, check to see if there are multiple version of the font
        # installed.  If so, pick the most recent version.  This is a crude
        # method of choosing the most recent version, but it is the best easy
        # solution given the heterogeneity in naming conventions for the
        # version string across fonts.
        versions = list(sorted(set(f['version'] for f in matchingfonts)))
        if len(matchingfonts) > 1 and len(versions) > 1:
            matchingfonts = [f for f in matchingfonts if f['version'] == versions[-1]]
        # If things still aren't working, now we check the foundry for
        # duplicates.  We hold off on checking the foundry information for as
        # long as possible (instead of doing it above) because it is often
        # inconsistent.
        foundries = list(sorted(set(f['foundry'] for f in matchingfonts)))
        if len(matchingfonts) > 1 and len(foundries) > 1:
            errortext = "Please specify a foundry using the function argument foundry=[value].  Valid values for this font are:\n    "
            errortext += ", ".join(f'"{f}"' for f in foundries)
            raise MultipleFontsFoundError(errortext)
        # Now do the same thing for the special property, which can also be
        # inconsistent.
        specials = list(sorted(set(f['special'] for f in matchingfonts)))
        if len(matchingfonts) > 1 and len(specials) > 1:
            errortext = "Please specify a special property using the function argument special=[value].  Valid values for this font are:\n    "
            errortext += ", ".join(f'"{s}"' for s in specials)
            raise MultipleFontsFoundError(errortext)
        # If we still have too many fonts, start to filter based on the name of the
        # font's weight.
        if len(matchingfonts) > 1 and len(set(f['weight'] for f in matchingfonts)) > 1:
            # We loop through these because it allows us to prioritize the first
            # ones, e.g. if a font contains both "medium" and "book".
            for weight in weights:
                newmatchingfonts = [f for f in matchingfonts if f['weight'] == weight]
                if newmatchingfonts:
                    matchingfonts = newmatchingfonts
                    break
        # If there are multiple matching fonts, check to see if they have the
        # same identifier.  If so, they are the same font and we can choose
        # either arbitrarily.  For consistency, we sort them first based on
        # filename.
        if len(matchingfonts) > 1 and len(set(f['identifier'] for f in matchingfonts)) == 1:
            matchingfonts = sorted(matchingfonts, key=lambda x : x['fname'])
            matchingfonts = matchingfonts[0:1]
        # Now we really should only have one font.  If not, it's an error and we
        # should alert the user.
        if len(matchingfonts) > 1:
            matchingfonts = sorted(matchingfonts, key=lambda x : x['fname'])
            warningtext = "Warning: Multiple versions of the specified font are installed:\n"
            for f in matchingfonts:
                warningtext += "    " + f['fname'] + "\n"
            warningtext += "We are arbitrarily choosing:"
            warningtext += "    " + matchingfonts[0]['fname'] + "\n"
            matchingfonts = matchingfonts[0:1]
            print(warningtext)
        _find_font_family_cache[cachename] = matchingfonts[0]
        return matchingfonts[0]
    styles = {}
    try:
        styles['regular'] = find_member(allfonts, bold=False, italic=False)
    except:
        print("Warning, regular font not found")
    try:
        styles['italic'] = find_member(allfonts, bold=False, italic=True)
    except:
        print("Warning, italic font not found")
    try:
        styles['bold'] = find_member(allfonts, bold=True, italic=False)
    except:
        print("Warning, bold font not found")
    try:
        styles['bolditalic'] = find_member(allfonts, bold=True, italic=True)
    except:
        print("Warning, bold-italic font not found")
    for style in styles:
        if styles[style]['num_faces'] > 1:
            print(f"Warning, font is a .ttc file with {styles[style]['num_faces']} embedded faces.  CanD can only use one.  If you have problems, try using a ttf or otf font instead.")
            break
    _find_font_family_cache[cachename] = styles
    return styles

#TODO: Neutraface, EB Garamond, penumbra, gotham, fell, stone sans, univers arkandis (chooses condensed by default), Bell
# Universalis is has the wrong value for typographic subfamily
# Fell has crazy labeling
