import json

# cytoscape
GROUP = "group"
NODES = "nodes"
ID = "id"
EDGE_ID = "edge_id"
SOURCE = "source"
TARGET = "target"
EDGES = "edges"
ELEMENTS = "elements"
STYLE = "style"
LAYOUT = "layout"
SELECTOR = "selector"

# schema constants, these come from json schema
ADDITIONAL_PROPERTIES = "additionalProperties"
PROPERTIES = "properties"
PATTERN_PROPERTIES = "patternProperties"
DESCRIPTION = "description"
TITLE = "title"
TYPE = "type"
ITEMS = "items"
PATTERN = "pattern"
REQUIRED = "required"
MIN_ITEMS = "minItems"
OPTIONS = "options"
DEPENDENCIES = "dependencies"
DEFAULT = "default"
ENUM = "enum"
MINIMUM = "minimum"
MAXIMUM = "maximum"
ARRAY = "array"
ONEOF = "oneOf"
STRING = "string"
NUMBER = "number"
INTEGER = "integer"
BOOLEAN = "boolean"
ARRAY = "array"
OBJECT = "object"
COLOR_INFO = (
    "Colours may be specified by name (e.g. red), hex (e.g. #ff0000 or #f00), RGB (e.g. rgb(255, 0, 0)),"
    " or HSL (e.g. hsl(0, 100%, 50%))."
)
ARROW_TYPES = [
    "triangle",
    "triangle-tee",
    "circle-triangle",
    "triangle-cross",
    "triangle-backcurve",
    "vee",
    "tee",
    "square",
    "circle",
    "diamond",
    "chevron",
    "none",
]
ELEMENTS = "elements"


def build_cytoscape_schema():
    schema = {
        "$schema": "http://json-schema.org/draft/2019-09/schema#",
        "title": "Cytoscape Schema",
        DESCRIPTION: "Dictionary that follows https://js.cytoscape.org/",
        TYPE: OBJECT,
        PROPERTIES: {
            ELEMENTS: {
                TYPE: ARRAY,
                DESCRIPTION: "An array of elements specified as plain objects. For convenience, this option can"
                " alternatively be specified as a promise that resolves to the elements JSON.",
                ITEMS: {
                    TYPE: OBJECT,
                    PROPERTIES: {
                        GROUP: {
                            TYPE: STRING,
                            DESCRIPTION: "nodes' for a node, 'edges' for an edge. NB the group field can be"
                            " automatically inferred for you but specifying it gives you nice debug"
                            " messages if you mis-init elements",
                            ENUM: [NODES, EDGES],
                        },
                        "data": {
                            TYPE: OBJECT,
                            REQUIRED: [ID],
                            DESCRIPTION: "element data",
                            PROPERTIES: {
                                ID: {
                                    TYPE: STRING,
                                    DESCRIPTION: "mandatory (string) id for each element, assigned"
                                    " automatically on undefined",
                                },
                                "parent": {
                                    TYPE: STRING,
                                    DESCRIPTION: "indicates the compound node parent id; not defined => no parent",
                                },
                                SOURCE: {
                                    TYPE: STRING,
                                    DESCRIPTION: "the source node id (edge comes from this node)",
                                },
                                TARGET: {
                                    TYPE: STRING,
                                    DESCRIPTION: "the target node id (edge goes to this node)",
                                },
                            },
                        },
                        "position": {
                            TYPE: OBJECT,
                            DESCRIPTION: "the model position of the node",
                            PROPERTIES: {"x": {TYPE: NUMBER}, "y": {TYPE: NUMBER},},
                        },
                        "renderedPosition": {
                            TYPE: OBJECT,
                            DESCRIPTION: "can alternatively specify position in rendered on-screen pixels",
                            PROPERTIES: {"x": {TYPE: NUMBER}, "y": {TYPE: NUMBER},},
                        },
                        "selected": {TYPE: BOOLEAN, DESCRIPTION: "", DEFAULT: False},
                        "selectable": {
                            TYPE: BOOLEAN,
                            DESCRIPTION: "whether the selection state is mutable",
                            DEFAULT: True,
                        },
                        "locked": {
                            TYPE: BOOLEAN,
                            DESCRIPTION: "when locked a node's position is immutable",
                            DEFAULT: False,
                        },
                        "grabbable": {
                            TYPE: BOOLEAN,
                            DESCRIPTION: "whether the node can be grabbed and moved by the user",
                            DEFAULT: True,
                        },
                        "pannable": {
                            TYPE: BOOLEAN,
                            DESCRIPTION: "whether dragging the node causes panning instead of grabbing",
                            DEFAULT: False,
                        },
                        "classes": {  # add oneOf for a space separated string
                            TYPE: ARRAY,
                            DESCRIPTION: "an array of class names that the element has",
                            ITEMS: {TYPE: STRING},
                        },
                    },
                },
            },
            LAYOUT: {
                TYPE: OBJECT,
                DESCRIPTION: "Placement of the nodes see https://js.cytoscape.org/#layouts",
                REQUIRED: ["name"],
                PROPERTIES: {
                    "name": {
                        TYPE: STRING,
                        DEFAULT: "random",
                        ENUM: [
                            "null",
                            "random",
                            "preset",
                            "grid",
                            "circle",
                            "concentric",
                            "breadthfirst",
                            "cose",
                        ],
                        DESCRIPTION: "Type of layout",
                    },
                    "fit": {
                        TYPE: BOOLEAN,
                        DEFAULT: True,
                        DESCRIPTION: "whether to fit to viewport",
                    },
                    "padding": {TYPE: NUMBER, DEFAULT: 30, DESCRIPTION: "fit padding"},
                    "boundingBox": {
                        TYPE: OBJECT,
                        DESCRIPTION: "constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }",
                    },
                    "animate": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "whether to transition the node positions",
                    },
                    "animationDuration": {
                        TYPE: NUMBER,
                        DESCRIPTION: "duration of animation in ms if enabled",
                        DEFAULT: 500,
                    },
                    "positions": {
                        TYPE: OBJECT,
                        DESCRIPTION: "layout = preset, map of (node id) => (position obj);"
                        " or function(node){ return somPos; }",
                    },
                    "avoidOverlap": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is grid, circle, concentric, breathfirst. prevents node overlap, may"
                        " overflow boundingBox if not enough space",
                        DEFAULT: True,
                    },
                    "avoidOverlapPadding": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is grid. Extra spacing around nodes when avoidOverlap: true",
                        DEFAULT: 10,
                    },
                    "nodeDimensionsIncludeLabels": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "Excludes the label when calculating"
                        " node bounding boxes for the layout algorithm",
                        DEFAULT: False,
                    },
                    "spacingFactor": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is grid, circle, breadthfirst. "
                        "grid, circle: Applies a multiplicative factor (>0) to expand or"
                        " compress the overall area that the nodes take up."
                        "breathfirst: positive spacing factor, larger => more space between nodes"
                        " (N.B. n/a if causes overlap)",
                        DEFAULT: 1,
                        MINIMUM: 0,
                    },
                    "condense": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is grid. uses all available space on false,"
                        " uses minimal space on true",
                        DEFAULT: False,
                    },
                    "rows": {
                        TYPE: INTEGER,
                        DESCRIPTION: "When layout is grid. force num of rows in the grid",
                    },
                    "cols": {
                        TYPE: INTEGER,
                        DESCRIPTION: "When layout is grid. force num of columns in the grid",
                    },
                    "radius": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is circle. the radius of the circle",
                    },
                    "startAngle": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is circle, concentric. where nodes start in radians",
                        DEFAULT: 4.712,
                    },
                    "sweep": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is circle, concentric. how many radians should be between"
                        " the first and"
                        " last node (defaults to full circle)",
                    },
                    "clockwise": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is circle, concentric. "
                        "whether the layout should go clockwise (true) or counterclockwise/anticlockwise"
                        " (false)",
                    },
                    "equidistant": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is concentric. "
                        "whether levels have an equal radial distance betwen them, "
                        "may cause bounding box overflow",
                    },
                    "minNodeSpacing": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is concentric. min spacing between outside of nodes"
                        " (used for radius adjustment)",
                    },
                    "directed": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is breadthfirst. whether the tree is directed downwards"
                        " (or edges can point in any direction if false)",
                        DEFAULT: False,
                    },
                    "circle": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is breadthfirst. put depths in concentric circles if true, put"
                        " depths top down if false",
                        DEFAULT: False,
                    },
                    "grid": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is breadthfirst. whether to create an even grid into which the DAG"
                        " is placed (circle:false only)",
                        DEFAULT: False,
                    },
                    "roots": {
                        TYPE: STRING,
                        DESCRIPTION: "When layout is breadthfirst. Format of selector, the roots of the trees",
                    },
                    "maximal": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is breadthfirst. whether to shift nodes down their natural BFS depths"
                        " in order to avoid upwards edges (DAGS only)",
                        DEFAULT: False,
                    },
                    "randomize": {
                        TYPE: BOOLEAN,
                        DESCRIPTION: "When layout is cose. Randomize the initial positions of the nodes (true) or"
                        " use existing positions (false)",
                        DEFAULT: False,
                    },
                    "componentSpacing": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Extra spacing between components in non-compound graphs",
                        DEFAULT: 40,
                    },
                    "nodeOverlap": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Node repulsion (overlapping) multiplier",
                        DEFAULT: 4,
                    },
                    "nestingFactor": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Nesting factor (multiplier) to compute ideal edge length"
                        " for nested edges",
                        DEFAULT: 1.2,
                    },
                    "gravity": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Gravity force (constant)",
                        DEFAULT: 1,
                    },
                    "numIter": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Maximum number of iterations to perform",
                        DEFAULT: 1000,
                    },
                    "initialTemp": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Initial temperature (maximum node displacement)",
                        DEFAULT: 1000,
                    },
                    "coolingFactor": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Cooling factor (how the temperature is "
                        "reduced between consecutive iterations)",
                        DEFAULT: 0.99,
                    },
                    "minTemp": {
                        TYPE: NUMBER,
                        DESCRIPTION: "When layout is cose. Lower temperature threshold (below this"
                        " point the layout will end)",
                        DEFAULT: 1.0,
                    },
                },
            },
            STYLE: {
                TYPE: ARRAY,
                DESCRIPTION: "Style applied to a group, e.g. all nodes, all edges, nodes in a certain class"
                " or a single node, etc. "
                "Each element is CSS-like, See https://js.cytoscape.org/#style",
                ITEMS: {
                    TYPE: OBJECT,
                    REQUIRED: [SELECTOR, STYLE],
                    PROPERTIES: {
                        SELECTOR: {
                            TYPE: STRING,
                            DESCRIPTION: "Where to apply the style element, common inputs are *node* or *edge*,"
                            " Also takes in css selector, e.g. *.foo* to apply to all edges and nodes of"
                            ' class *foo*, #foo (or [id="foo"]) for node or edge of with id foo.'
                            " See https://js.cytoscape.org/#selectors/notes-amp-caveats",
                        },
                        STYLE: {
                            TYPE: OBJECT,
                            DESCRIPTION: "Specify the styles",
                            PROPERTIES: {
                                "width": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The width of the node’s body or the width of an edge’s line.",
                                },
                                "height": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The height of the node’s body",
                                },
                                "shape": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The shape of the node’s body. Note that each shape fits within the"
                                    " specified width and height, and so you may have to adjust width and"
                                    " height if you desire an equilateral shape"
                                    " (i.e. width !== height for several equilateral shapes)",
                                    ENUM: [
                                        "ellipse",
                                        "triangle",
                                        "round-triangle",
                                        "rectangle",
                                        "round-rectangle",
                                        "bottom-round-rectangle",
                                        "cut-rectangle",
                                        "barrel",
                                        "rhomboid",
                                        "diamond",
                                        "round-diamond",
                                        "pentagon",
                                        "round-pentagon",
                                        "hexagon",
                                        "round-hexagon",
                                        "concave-hexagon",
                                        "heptagon",
                                        "round-heptagon",
                                        "octagon",
                                        "round-octagon",
                                        "star",
                                        "tag",
                                        "round-tag",
                                        "vee",
                                    ],
                                },
                                "background-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The colour of the node’s body. "
                                    + COLOR_INFO,
                                },
                                "background-blacken": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "Blackens the node’s body for values from 0 to 1;"
                                    " whitens the node’s body for values from 0 to -1.",
                                    MAXIMUM: 1,
                                    MINIMUM: -1,
                                },
                                "background-opacity": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The opacity level of the node’s background colour",
                                    MAXIMUM: 1,
                                    MINIMUM: 0,
                                },
                                "border-width": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The size of the node’s border.",
                                    MINIMUM: 0,
                                },
                                "border-style": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The style of the node’s border",
                                    ENUM: ["solid", "dotted", "dashed", "double"],
                                },
                                "border-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The colour of the node’s border. "
                                    + COLOR_INFO,
                                },
                                "border-opacity": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The opacity of the node’s border",
                                    MINIMUM: 0,
                                    MAXIMUM: 1,
                                },
                                "padding": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The amount of padding around all sides of the node.",
                                    MINIMUM: 0,
                                },
                                "curve-style": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The curving method used to separate two or more edges between two"
                                    " nodes; may be haystack (very fast, bundled straight edges"
                                    " for which loops and compounds are unsupported), straight (straight"
                                    " edges with all arrows supported), bezier (bundled curved edges),"
                                    " unbundled-bezier (curved edges for use with manual control points),"
                                    " segments (a series of straight lines), taxi (right-angled lines,"
                                    " hierarchically bundled). Note that haystack edges work best with"
                                    " ellipse, rectangle, or similar nodes. Smaller node shapes, like"
                                    " triangle, will not be as aesthetically pleasing. Also note that"
                                    " edge endpoint arrows are unsupported for haystack edges.",
                                    DEFAULT: "straight",
                                    ENUM: [
                                        "straight",
                                        "haystack",
                                        "bezier",
                                        "unbundled-bezier",
                                        "segments",
                                        "taxi",
                                    ],
                                },
                                "line-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The colour of the edge’s line. "
                                    + COLOR_INFO,
                                },
                                "line-style": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The style of the edge’s line.",
                                    ENUM: ["solid", "dotted", "dashed"],
                                },
                                "line-cap": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The cap style of the edge’s line; may be butt (default), round, or"
                                    " square. The cap may or may not be visible, depending on the shape"
                                    " of the node and the relative size of the node and edge. Caps other"
                                    " than butt extend beyond the specified endpoint of the edge.",
                                    ENUM: ["butt", "round", "square"],
                                    DEFAULT: "butt",
                                },
                                "line-opacity": {
                                    TYPE: NUMBER,
                                    MINIMUM: 0,
                                    MAXIMUM: 1,
                                    DEFAULT: 1,
                                    DESCRIPTION: "The opacity of the edge’s line and arrow. Useful if you wish to have"
                                    " a separate opacity for the edge label versus the edge line. Note"
                                    " that the opacity value of the edge element affects the effective"
                                    " opacity of its line and label subcomponents.",
                                },
                                "target-arrow-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The colour of the edge’s source arrow. "
                                    + COLOR_INFO,
                                },
                                "target-arrow-shape": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The shape of the edge’s source arrow",
                                    ENUM: ARROW_TYPES,
                                },
                                "target-arrow-fill": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The fill state of the edge’s source arrow",
                                    ENUM: ["filled", "hollow"],
                                },
                                "mid-target-arrow-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The colour of the edge’s source arrow. "
                                    + COLOR_INFO,
                                },
                                "mid-target-arrow-shape": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The shape of the edge’s source arrow",
                                    ENUM: ARROW_TYPES,
                                },
                                "mid-target-arrow-fill": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The fill state of the edge’s source arrow",
                                    ENUM: ["filled", "hollow"],
                                },
                                "arrow-scale": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "Scaling for the arrow size.",
                                    MINIMUM: 0,
                                },
                                "opacity": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The opacity of the element."
                                    " See https://js.cytoscape.org/#style/visibility",
                                    MINIMUM: 0,
                                    MAXIMUM: 1,
                                },
                                "z-index": {
                                    TYPE: INTEGER,
                                    DESCRIPTION: "An integer value that affects the relative draw order of elements."
                                    " In general, an element with a higher z-index will be drawn on top"
                                    " of an element with a lower z-index. Note that edges are under nodes"
                                    " despite z-index.",
                                },
                                "label": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The text to display for an element’s label. Can give a path, e.g. "
                                    "data(id) will label with the elements id",
                                },
                                "source-label": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The text to display for an edge’s source label. Can give a path, e.g. "
                                    "data(id) will label with the elements id",
                                },
                                "target-label": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The text to display for an edge’s target label. Can give a path, e.g. "
                                    "data(id) will label with the elements id",
                                },
                                "color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The color of the element's label. "
                                    + COLOR_INFO,
                                },
                                "text-opacity": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The opacity of the label text, including its outline.",
                                    MINIMUM: 0,
                                    MAXIMUM: 1,
                                },
                                "font-family": {
                                    TYPE: STRING,
                                    DESCRIPTION: "A comma-separated list of font names to use on the label text.",
                                },
                                "font-size": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The size of the label text.",
                                },
                                "font-style": {
                                    TYPE: STRING,
                                    DESCRIPTION: "A CSS font style to be applied to the label text.",
                                },
                                "font-weight": {
                                    TYPE: STRING,
                                    DESCRIPTION: "A CSS font weight to be applied to the label text.",
                                },
                                "text-transform": {
                                    TYPE: STRING,
                                    DESCRIPTION: "A transformation to apply to the label text",
                                    ENUM: ["none", "uppercase", "lowercase"],
                                },
                                "text-halign": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The horizontal alignment of a node’s label",
                                    ENUM: ["left", "center", "right"],
                                },
                                "text-valign": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The vertical alignment of a node’s label",
                                    ENUM: ["top", "center", "bottom"],
                                },
                                "ghost": {
                                    TYPE: STRING,
                                    DESCRIPTION: "Whether to use the ghost effect, a semitransparent duplicate of"
                                    " the element drawn at an offset.",
                                    DEFAULT: "no",
                                    ENUM: ["yes", "no"],
                                },
                                "active-bg-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The colour of the indicator shown when the background is grabbed"
                                    " by the user. Selector needs to be *core*. "
                                    + COLOR_INFO,
                                },
                                "active-bg-opacity": {
                                    TYPE: STRING,
                                    DESCRIPTION: " The opacity of the active background indicator."
                                    " Selector needs to be *core*.",
                                },
                                "active-bg-size": {
                                    TYPE: STRING,
                                    DESCRIPTION: " The opacity of the active background indicator."
                                    " Selector needs to be *core*.",
                                },
                                "selection-box-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The background colour of the selection box used for"
                                    " drag selection. Selector needs to be *core*. "
                                    + COLOR_INFO,
                                },
                                "selection-box-border-width": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The size of the border on the selection box."
                                    " Selector needs to be *core*",
                                },
                                "selection-box-opacity": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The opacity of the selection box.  Selector needs to be *core*",
                                    MINIMUM: 0,
                                    MAXIMUM: 1,
                                },
                                "outside-texture-bg-color": {
                                    TYPE: STRING,
                                    DESCRIPTION: "The colour of the area outside the viewport texture when"
                                    " initOptions.textureOnViewport === true.  Selector needs to be *core*"
                                    ". " + COLOR_INFO,
                                },
                                "outside-texture-bg-opacity": {
                                    TYPE: NUMBER,
                                    DESCRIPTION: "The opacity of the area outside the viewport texture."
                                    " Selector needs to be *core*",
                                    MINIMUM: 0,
                                    MAXIMUM: 1,
                                },
                            },
                        },
                    },
                },
            },
            "zoom": {
                TYPE: NUMBER,
                DESCRIPTION: "The initial zoom level of the graph. Make sure to disable viewport"
                " manipulation options, such as fit, in your layout so that it is not overridden"
                " when the layout is applied. You can set options.minZoom and"
                " options.maxZoom to set restrictions on the zoom level",
                DEFAULT: "1",
            },
            "pan": {
                TYPE: OBJECT,
                DESCRIPTION: "The initial panning position of the graph. Make sure to disable viewport"
                " manipulation options, such as fit, in your layout so that it is not"
                " overridden when the layout is applied.",
                PROPERTIES: {
                    "x": {TYPE: NUMBER, DEFAULT: 0},
                    "y": {TYPE: NUMBER, DEFAULT: 0},
                },
                ADDITIONAL_PROPERTIES: False,
            },
            "minZoom": {
                TYPE: NUMBER,
                DESCRIPTION: "A minimum bound on the zoom level of the graph. The viewport cannot be"
                " scaled smaller than this zoom level.",
            },
            "maxZoom": {
                TYPE: NUMBER,
                DESCRIPTION: "A maximum bound on the zoom level of the graph. The viewport cannot"
                " be scaled larger than this zoom level.",
            },
            "zoomingEnabled": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether zooming the graph is enabled, both by user events"
                " and programmatically.",
                DEFAULT: True,
            },
            "userZoomingEnabled": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether user events (e.g. mouse wheel, pinch-to-zoom) are allowed to zoom"
                " the graph. Programmatic changes to zoom are unaffected by this option.",
                DEFAULT: True,
            },
            "panningEnabled": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether panning the graph is enabled, both by user"
                " events and programmatically.",
                DEFAULT: True,
            },
            "userPanningEnabled": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether user events (e.g. dragging the graph background) are allowed"
                " to pan the graph. Programmatic changes to pan are unaffected by this option.",
                DEFAULT: True,
            },
            "boxSelectionEnabled": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether box selection (i.e. drag a box overlay around, and release it to"
                " select) is enabled. If enabled while panning is also enabled, the user must"
                " use a modifier key (shift, alt, control, or command) to use box selection.",
                DEFAULT: True,
            },
            "selectionType": {
                TYPE: STRING,
                DESCRIPTION: "A string indicating the selection behaviour from user input. For 'additive',"
                " a new selection made by the user adds to the set of currently selected"
                " elements. For 'single', a new selection made by the user becomes the entire"
                " set of currently selected elements (i.e. the previous elements are"
                " unselected).",
                ENUM: ["single", "additive"],
                DEFAULT: "single",
            },
            "touchTapThreshold": {
                TYPE: NUMBER,
                DESCRIPTION: "A non-negative integer that indicates the maximum allowable distance that"
                " a user may move during a tap gesture on touch devices. This makes tapping"
                " easier for users. These values have sane defaults, so it is not advised to"
                " change these options unless you have very good reason for doing so."
                " Large values will almost certainly have undesirable consequences.",
                DEFAULT: 8,
            },
            "desktopTapThreshold": {
                TYPE: NUMBER,
                DESCRIPTION: "A non-negative integer that indicates the maximum allowable distance that"
                " a user may move during a tap gesture on desktop devices. This makes tapping"
                " easier for users. These values have sane defaults, so it is not advised to"
                " change these options unless you have very good reason for doing so."
                " Large values will almost certainly have undesirable consequences.",
                DEFAULT: 4,
            },
            "autoungrabify": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether nodes should be ungrabified (not grabbable by user) by default"
                " (if true, overrides individual node state)",
                DEFAULT: False,
            },
            "autolock": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether nodes should be locked (not draggable at all) by default (if true,"
                " overrides individual node state).",
                DEFAULT: False,
            },
            "autounselectify": {
                TYPE: BOOLEAN,
                DESCRIPTION: "Whether nodes should be unselectified (immutable selection state) by default"
                " (if true, overrides individual element state).",
                DEFAULT: False,
            },
            "headless": {
                TYPE: BOOLEAN,
                DESCRIPTION: "A convenience option that initialises the instance to run headlessly."
                " You do not need to set this in environments that are implicitly headless"
                " (e.g. Node.js). However, it is handy to set headless: true if you want a"
                " headless instance in a browser.",
                DEFAULT: False,
            },
            "styleEnabled": {
                TYPE: BOOLEAN,
                DESCRIPTION: "A boolean that indicates whether styling should be used. For headless "
                "(i.e. outside the browser) environments, display is not necessary and so"
                " neither is styling necessary — thereby speeding up your code. You can"
                " manually enable styling in headless environments if you require it for a"
                " special case. Note that it does not make sense to disable style if you plan"
                " on rendering the graph. Also note that cy.destroy() must be called to clean"
                " up a style-enabled, headless instance.",
                DEFAULT: False,
            },
            "wheelSensitivity": {
                TYPE: NUMBER,
                DEFAULT: 1,
                DESCRIPTION: "Changes the scroll wheel sensitivity when zooming. This is a multiplicative"
                " modifier. So, a value between 0 and 1 reduces the sensitivity (zooms slower),"
                " and a value greater than 1 increases the sensitivity (zooms faster). This"
                " option is set to a sane value that works well for mainstream mice (Apple,"
                " Logitech, Microsoft) on Linux, Mac, and Windows. If the default value seems"
                " too fast or too slow on your particular system, you may have non-default"
                " mouse settings in your OS or a niche mouse. You should not change this value"
                " unless your app is meant to work only on specific hardware. Otherwise, you"
                " risk making zooming too slow or too fast for most users.",
            },
        },
    }
    return schema


if __name__ == "__main__":
    schema = build_cytoscape_schema()
    with open("cytoscape_schema.json", "w") as outfile:
        json.dump(schema, outfile, indent=4)
