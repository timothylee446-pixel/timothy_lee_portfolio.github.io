import html, re

SITE = "Timothy Lee"
NAV = [("index.html#work","Work","work"),("projects.html","Projects","projects"),("index.html#about","About","about")]

# (slug, title, summary, tags, thumbnail)
# Projects still in progress get an "Ongoing" marker on their card and page.
ONGOING = {"cas"}

PROJECTS = [
 ("cas","CAS","Contamination-aware sampling robot that takes water samples, then cleans and verifies its own sampling tool.",["Robotics","Fluid systems","Patent pending"],"cas-cad.jpg"),
 ("vtol","VTOL","Quadcopter VTOL UAV with an FEA-validated wing structure.",["Aircraft","FEA","SolidWorks"],"vtol-hero.jpg"),
 ("hexacopter","Hexacopter","Drone frame for a 20 lb payload, plus a modular tool-changing system.",["Drones","Mechanisms","Vibration"],"hexa-hero.jpg"),
 ("pneumatic-gripper","Pneumatic Gripper","Soft robotic gripper for a drone, funded by a $1,500 PEAK grant.",["Soft robotics","Molding","Research"],"gripper-hero.jpg"),
 ("assistive-powder-board","Assistive Powder Board","Low-cost powder board that motivates children in wheelchairs to do physical therapy.",["Client work","Woodworking","Sensors"],"powder-hero.jpg"),
 ("whistle-controlled-decorations","Whistle Controlled Decorations","Arduino circuit that switches a light strip when I whistle.",["Arduino","IR","Circuits"],"whistle-hero.jpg"),
 ("gravity-gambit-game","Gravity Gambit","Two-player plinko and target game with automatic scoring.",["Laser cutting","AutoCAD","Teamwork"],"gambit-hero.jpg"),
 ("chess-set","Chess Set","SolidWorks chess set themed on famous buildings.",["SolidWorks","Surfacing"],"chess-hero-1.jpg"),
]

# (slug, company, role, summary, tags, thumbnail)
EXPERIENCE = [
 ("notch","Notch","Co-op","Replaced brittle radomes, automated a paint process, and built a ventilated fume enclosure.",["Composites","CNC","G-code","Fusion 360"],"notch-logo.jpg"),
 ("sharkninja","SharkNinja","Mechanical engineering co-op","A patented airflow component headed for 500,000 units, Tesla-valve nozzle research, and test development.",["DFM","Fluids","Testing","Patent"],"sharkninja-logo.jpg"),
]

FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=JetBrains+Mono:wght@400;500&display=swap"
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23FF5A1F'/%3E"
           "%3Ctext x='32' y='43' font-family='Arial,sans-serif' font-size='30' font-weight='800' text-anchor='middle' fill='%23111417'%3ETL%3C/text%3E%3C/svg%3E")

PENDING = ' data-pending="Awaiting confidentiality approval"'

def esc(s): return html.escape(s, quote=True)

# Text wrapped in [brackets] is a note to self ("[Caption]", "[Text: ...]"). It renders hidden and only shows in draft mode.
def is_draft(s): return bool(s) and s.startswith("[") and s.endswith("]")

def slugify(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

# pending=True marks media waiting on approval: until the file is added, the live site shows a labeled placeholder instead of hiding it.
def fig_html(name, cap, pending=False):
    cap = "" if is_draft(cap) else cap
    capel = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
    return f'<figure><img src="images/{name}" alt="{esc(cap)}" loading="lazy" data-name="{name}"{PENDING if pending else ""}>{capel}</figure>'

def render_blocks(blocks, pending=False):
    out=[]; run=[]
    def flush():
        if len(run)==1: out.append(run[0])
        elif run: out.append(f'<div class="gallery g{min(len(run),3)}">'+"".join(run)+"</div>")
        run.clear()
    for b in blocks:
        k=b[0]
        if k=="fig":
            run.append(fig_html(b[1], b[2] if len(b)>2 else "", pending)); continue
        if k=="figw":  # a figure that always gets its own full-width row, for detailed images like tables
            flush(); out.append(fig_html(b[1], b[2] if len(b)>2 else "", pending).replace("<figure>","<figure class=\"wide\">",1)); continue
        if k=="loop":
            cap = b[2] if len(b)>2 else ""
            capel = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
            run.append(f'<figure class="loop"><video autoplay muted loop playsinline preload="metadata" src="videos/{b[1]}" data-name="{b[1]}" aria-label="{esc(cap)}"></video>{capel}</figure>'); continue
        flush()
        if k=="h2": out.append(f'<h2 id="{slugify(b[1])}">{esc(b[1])}</h2>')
        elif k=="h3": out.append(f"<h3>{esc(b[1])}</h3>")
        elif k=="p": out.append(f'<p class="draft">{esc(b[1])}</p>' if is_draft(b[1]) else f"<p>{esc(b[1])}</p>")
        elif k=="ul": out.append("<ul>"+"".join(f"<li>{esc(i)}</li>" for i in b[1])+"</ul>")
        elif k=="ol": out.append("<ol>"+"".join(f"<li>{esc(i)}</li>" for i in b[1])+"</ol>")
        elif k=="video":
            cap = b[2] if len(b)>2 and not is_draft(b[2]) else ""
            capel = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
            out.append(f'<figure class="media"><video controls preload="metadata" src="videos/{b[1]}" data-name="{b[1]}"{PENDING if pending else ""}></video>{capel}</figure>')
        elif k=="yt":
            draft = ' draft' if b[1]=="VIDEO_ID" else ''
            out.append(f'<figure class="embed{draft}"><iframe src="https://www.youtube.com/embed/{b[1]}" title="{esc(b[2])}" loading="lazy" allowfullscreen></iframe><figcaption>{esc(b[2])}</figcaption></figure>')
        elif k=="link":
            out.append(f'<p><a class="ext" href="{b[1]}">{esc(b[2])} <span aria-hidden="true">↗</span></a></p>')
    flush()
    return "\n".join(out)

def page(fname, title, desc, body, current):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if key==current else ""}>{esc(t)}</a>' for h,t,key in NAV)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {SITE}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#F3F1EC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D1013" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="top-in">
  <a class="brand" href="index.html"><span class="mark" aria-hidden="true">TL</span><span class="brand-name">{SITE}</span></a>
  <nav aria-label="Main">{nav}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
  <div class="foot-meta">
    <p><strong>{SITE}</strong><br>Mechanical engineering, Northeastern University<br>Boston, MA</p>
    <a class="totop" href="#top">Back to top <span aria-hidden="true">↑</span></a>
  </div>
</div></footer>
<script src="site.js"></script>
</body>
</html>
"""
    open(fname,"w",encoding="utf-8",newline="\n").write(doc)

def tags_html(tags): return '<span class="tags">'+"".join(f"<span>{esc(t)}</span>" for t in tags)+"</span>"

ONGOING_BADGE = '<span class="badge"><span class="pulse" aria-hidden="true"></span>Ongoing</span>'

def card(slug,title,summary,tags,thumb,num):
    return f"""<a class="card" href="{slug}.html">
  <span class="card-media"><img src="images/{thumb}" alt="" loading="lazy" data-thumb>{ONGOING_BADGE if slug in ONGOING else ""}</span>
  <span class="card-body"><span class="card-num">{num:02d}</span><span class="card-t">{esc(title)}</span><span class="card-d">{esc(summary)}</span>{tags_html(tags)}</span>
</a>"""

def project_cards(): return '<div class="cards">'+"".join(card(s,t,d,tg,th,i+1) for i,(s,t,d,tg,th) in enumerate(PROJECTS))+"</div>"

def xp_cards():
    out=[]
    for i,(slug,co,role,summ,tags,thumb) in enumerate(EXPERIENCE):
        out.append(f"""<a class="xp" href="{slug}.html">
  <span class="xp-media{' logo' if '-logo' in thumb else ''}"><img src="images/{thumb}" alt="" loading="lazy" data-thumb><span class="xp-mono" aria-hidden="true">{esc(co[0])}</span></span>
  <span class="xp-body"><span class="card-num">{role}</span><span class="xp-t">{esc(co)}</span><span class="card-d">{esc(summ)}</span>{tags_html(tags)}<span class="more">Read the case study <span aria-hidden="true">→</span></span></span>
</a>""")
    return '<div class="xps">'+"".join(out)+"</div>"

def project_page(slug,title,summary,meta,blocks,kicker,back,current,thumb=None,prev=None,nxt=None,pending=False):
    blocks=list(blocks)
    cover=""
    if blocks and blocks[0][0]=="fig" and blocks[0][1]==thumb:
        cap = blocks[0][2] if len(blocks[0])>2 else ""
        cover = f'<div class="wrap">{fig_html(thumb, cap).replace("<figure>","<figure class=\"cover\">",1).replace(" loading=\"lazy\"","",1)}</div>'
        blocks=blocks[1:]
    metahtml = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k,v in meta)
    h2s=[b[1] for b in blocks if b[0]=="h2"]
    toc = ""
    if len(h2s)>=2:
        toc = '<aside class="toc" aria-label="On this page"><p class="toc-h">On this page</p><ol>'+"".join(f'<li><a href="#{slugify(h)}">{esc(h)}</a></li>' for h in h2s)+"</ol></aside>"
    pager=""
    if prev or nxt:
        def pl(cls,label,p):
            return f'<a class="{cls}" href="{p[0]}.html"><span>{label}</span><strong>{esc(p[1])}</strong></a>' if p else '<span></span>'
        pager = f'<nav class="pager wrap" aria-label="More work">{pl("prev","Previous",prev)}{pl("next","Next",nxt)}</nav>'
    body = f"""<article class="project">
<header class="proj-head"><div class="wrap">
<a class="back" href="{back[0]}"><span aria-hidden="true">←</span> {esc(back[1])}</a>
<p class="kicker">{kicker}</p>
<h1>{esc(title)}</h1>
<p class="lede">{esc(summary)}</p>
<dl class="meta">{metahtml}</dl>
</div></header>
{cover}
<div class="proj-body wrap{' has-toc' if toc else ''}">
{toc}
<div class="prose">
{render_blocks(blocks, pending)}
</div>
</div>
{pager}
</article>"""
    page(f"{slug}.html", title, summary, body, current)

# ---------------- content ----------------
P = {}

P["cas"]=("CAS","A contamination-aware sampling robot that takes water samples, then cleans its sampling tool and verifies that it is clean.",
 [("Status","Ongoing"),("Type","Venture group project"),("IP","Patent pending"),("Skills","Part specification, materials, research, CAD, 3D printing")],
 [("fig","cas-cad.jpg","CAD of the CAS system"),
  ("p","CAS (contamination-aware sampling) is a venture group project with a patent pending. The objective is a robot that takes water samples, then cleans the sampling tool and verifies that it is clean before the next sample."),
  ("p","The system has three main parts:"),
  ("ul",["A central robot arm","A sample rack","A decontamination station"]),
  ("h2","Decontamination station"),
  ("p","The decontamination station cleans the sampling tool after each sample and checks that it is clean."),
  ("p","[Text: the challenges of designing the decontamination station]"),
  ("figw","cas-decon-diagram.jpg","Fluid system control diagram"),
  ("figw","cas-bom.png","Order BOM for the decontamination station"),
 ])

P["vtol"]=("VTOL","Create a quadcopter VTOL (vertical take-off and landing) UAV.",
 [("Status","Fabrication ongoing"),("Tools","SolidWorks CAD and FEA"),("Materials","Aero PLA, woven carbon fiber tubes")],
 [("fig","vtol-hero.jpg","The VTOL airframe"),
  ("h2","Skeleton reference model"),
  ("h3","Internal fuselage"),
  ("p","Optimized for strength and weight. The main body is printed from lightweight aero PLA and strengthened with woven carbon fiber tubes."),
  ("fig","vtol-fuselage-1.jpg",""),("fig","vtol-fuselage-2.jpg",""),("fig","vtol-fuselage-3.jpg",""),("fig","vtol-fuselage-4.jpg",""),
  ("h3","Horizontal stabilizer"),
  ("fig","vtol-stabilizer.jpg",""),
  ("h2","Wing simulations"),
  ("p","The wings must hold the lifting force without fracturing or deforming and losing their airfoil shape. I considered loading cases for normal flight, climbing, and sharp banking. Lifting force per wing is the G load times the predicted plane mass (3062 g). All studies used SolidWorks FEA."),
  ("h3","Empty wing (baseline)"),
  ("p","With no inner ribs and no added mass, the simulation fails at the 3G loading case."),
  ("fig","vtol-wing-baseline.jpg","1G loading case"),
  ("h3","Wing v1"),
  ("p","Variably spaced inner ribs maintain the structural integrity of the wing, at a cost of 43.47 g added mass per wing."),
  ("fig","vtol-wing-v1-1g.jpg","1G loading case"),
  ("fig","vtol-wing-v1-6g.jpg","6G loading case"),
  ("fig","vtol-wing-v1-9g.jpg","9G loading case (6G with a 1.5 safety factor). No issues at any prescribed loading case."),
 ])

P["hexacopter"]=("Hexacopter","Create a hexacopter drone frame that can support a 20 lb dynamic payload, optimized for weight, stiffness, and strength.",
 [("My contribution","All CAD shown is mine unless noted"),("Current mass","670 g, without the modular tool-changing system"),("Materials","PLA, nylon, steel, carbon fiber")],
 [("fig","hexa-hero.jpg","Reference scale: 5 cm side length"),
  ("p","Skills used: CAD, 3D printing, iterative design, part sourcing, BOM management, leadership, interdisciplinary teamwork, and project management."),
  ("h2","Version 1.0"),
  ("fig","hexa-v10-1.jpg",""),("fig","hexa-v10-2.jpg",""),
  ("h2","Version 1.1"),
  ("fig","hexa-v11-1.jpg",""),("fig","hexa-v11-2.jpg",""),("fig","hexa-v11-3.jpg",""),("fig","hexa-v11-4.jpg",""),("fig","hexa-v11-5.jpg",""),
  ("h3","Rotating arm"),
  ("p","Rotating the arms to change their angle can help stability and maneuverability. I made several iterations of a gear that holds set positions. The gears lock together on both sides of the bracket and are held in place by a bolt."),
  ("fig","hexa-gear-v1.jpg","Version 1"),("fig","hexa-gear-v2.jpg","Version 2"),("fig","hexa-gear-v3.jpg","Version 3"),
  ("h2","Version 1.2"),
  ("p","An assembly containing real parts: airframe, battery, Pixhawk, and Raspberry Pi."),
  ("fig","hexa-v12.jpg",""),
  ("h2","Version 1.3"),
  ("p","This model is filled with hardware and includes a custom bracket that holds the airframes together, optimized with SolidWorks simulation."),
  ("fig","hexa-v13-1.jpg",""),("fig","hexa-v13-2.jpg",""),
  ("h3","Assembly"),
  ("p","I cut the carbon fiber tubes with PPE and a steel Dremel wheel."),
  ("fig","hexa-assembly-1.jpg",""),("fig","hexa-assembly-2.jpg",""),
  ("h2","Modular tool-changing system"),
  ("p","I did not design this version of the system, but I made the mounts for the motors and the PCB."),
  ("fig","hexa-motor-mount.jpg","Motor mount"),("fig","hexa-pcb-mount.jpg","PCB mount"),
  ("h3","Toolchanger v3 (not my design)"),
  ("p","Design requirements:"),
  ("ol",["Push balls to lock the tool and drone couplers together.","Connect a barrel jack for data transfer."]),
  ("fig","hexa-tc3-unlocked.jpg","Unlocked position"),
  ("fig","hexa-tc3-locked.jpg","Locked position"),
  ("p","This system has several problems:"),
  ("ul",["Unnecessarily high complexity","Very difficult to assemble","Heavy","Little tolerance for error when aligning the couplers","Needs three pins for a higher data rate","Susceptible to impacts and vibration"]),
  ("video","mtc_lock_test.mp4","Locking: balls push out into the outer coupler (outer coupler removed for viewing)"),
  ("video","mtc_retract_test.mp4","Unlocking: balls retract and release the outer coupler (outer coupler removed for viewing)"),
  ("h2","Fourth iteration (my design)"),
  ("p","Objective: redesign the system to fix the weaknesses of the prior version."),
  ("fig","hexa-tc4-1.jpg","Fewer parts, reduced complexity"),
  ("fig","hexa-tc4-2.jpg","Coupler geometry leaves more room for alignment error"),
  ("fig","hexa-tc4-3.jpg","The cam platform is shaped to work with two motor assemblies instead of three"),
  ("fig","hexa-tc4-4.jpg","Three barrel jacks for data"),
  ("h3","Error adjustment"),
  ("ul",["The square couplers absorb rotational error.","Contact forces at the edges align the outer coupler to the inner one.","The funnel shape of the couplers absorbs translational error."]),
  ("fig","hexa-tc4-error.jpg",""),
  ("h3","Two-motor assembly"),
  ("ul",["Three points are needed to define a plane and keep the platform level.","Two motors alone are not enough: the platform can tilt along the axis between them.","Curved walls keep the platform from tilting more than a degree.","The three plane-defining points are the two motors and the contact walls."]),
  ("fig","hexa-tc4-motors.jpg",""),
  ("h3","Three barrel jacks"),
  ("p","TPU cone nuts (brown) screw down between walls and squeeze the barrel jacks (bronze) to hold them in place."),
  ("fig","hexa-tc4-jacks.jpg",""),
  ("h3","No magnets"),
  ("p","The differently shaped platform forces the locking balls into place and lets them fall back passively when unlocking, so magnets are no longer needed. Tolerances still need adjusting."),
  ("h2","Vibration study: motor mount"),
  ("fig","hexa-vib-mount.jpg","A simple clamping motor mount I designed for our motors"),
  ("p","The parts are modeled as isotropic. The bolts are locally bonded to the parts and the clamping face is a fixed geometry. The motors spin at about 14,000 rpm at hover, so I ran the study around the 250 Hz range. The first four modes are shown below."),
  ("fig","hexa-vib-1.jpg","Mode 1: 202.73 Hz"),
  ("fig","hexa-vib-2.jpg","Mode 2: 262.42 Hz"),
  ("fig","hexa-vib-3.jpg","Mode 3: 356.4 Hz"),
  ("fig","hexa-vib-4.jpg","Mode 4: 1726.1 Hz"),
  ("p","The first two modes sit closest to the propeller operating range, so I redesigned the mount around them."),
 ])

P["pneumatic-gripper"]=("Pneumatic Gripper","A soft robotic end-effector for a drone that can pick up many different object shapes.",
 [("Funding","Northeastern PEAK research grant ($1,500)"),("My contribution","Everything except the pump and valve breadboard"),("Material","30A silicone")],
 [("fig","gripper-hero.jpg",""),
  ("p","Soft robotics is a developing field in which air pumps inflate a shape so that it actuates under different pressures. Skills used: researching, writing a research proposal, making molds, iterative design, pumps and valves, and material science."),
  ("h2","Theory"),
  ("p","One side of each finger has bellows that inflate under higher internal pressure while the other side stays the same length. That makes the finger curl."),
  ("fig","gripper-theory-1.jpg","A basic inflatable gripper in action"),
  ("fig","gripper-theory-2.jpg",""),
  ("h2","First iteration"),
  ("p","As a proof of concept we used a four-finger mold sourced online that came as a single part. We printed the mold, degassed the silicone in a vacuum chamber, and poured it. To test strength, we rigged the gripper against a scale and inflated a single finger with a manual pump. The fingers inflated asymmetrically, so we moved to another model."),
  ("fig","gripper-v1-1.jpg",""),("fig","gripper-v1-2.jpg",""),("fig","gripper-v1-3.jpg",""),
  ("h2","Second iteration"),
  ("p","The second model, also sourced online and cast the same way, had three fingers instead of four. It showed the same asymmetry. Next we tried casting individual fingers and joining them to a central hub. Most online models are closed source, so I designed the mold myself."),
  ("fig","gripper-v2-inspiration.jpg","The inspiration"),
  ("fig","gripper-v2-mold.jpg","Mold shells and core"),
  ("fig","gripper-v2-printed.jpg","Printed pieces"),
  ("fig","gripper-v2-cast.jpg",""),
  ("yt","cd79CXBYNtk","Gripper test video 1"),
  ("yt","jf_uEUaGd-g","Gripper test video 2"),
  ("h2","First functional gripper"),
  ("p","After several iterations and many castings, this was the first functional gripper."),
  ("fig","gripper-final-1.jpg",""),
  ("fig","gripper-final-2.jpg","The variable grip geometry system uses involute gears to switch between X-shaped and H-shaped grip configurations, so it can hold different object geometries."),
  ("link","https://www.youtube.com/shorts/UY0K_xbwRZg","Watch the variable grip geometry demonstration"),
 ])

P["assistive-powder-board"]=("Assistive Powder Board","A low-cost powder board designed to motivate young users to do their physical therapy exercises.",
 [("Type","Client project"),("Skills","Designing for a client, woodworking with power tools, electronics assembly, construction")],
 [("fig","powder-hero.jpg",""),
  ("h2","What is a powder board?"),
  ("p","A powder board is an exercise table that physical therapists use to help patients rehabilitate and improve leg mobility. Wheelchair users are common users. Sitting all day is unhealthy for them, and moving their legs as much as they can is extremely beneficial."),
  ("h2","If powder boards exist, what's the problem?"),
  ("p","They are expensive. These simple boards cost anywhere from $300 to $6,000. Physical therapy is also difficult and boring, especially for our target user: children in wheelchairs."),
  ("fig","powder-problem.jpg",""),
  ("h2","The solution"),
  ("p","A custom powder board that is cheap and rewarding to use. Our first idea was a skateboard-like object with lights, satisfying sounds, and songs that activate when it detects movement. The patient would rest a leg on it and roll it back and forth."),
  ("fig","powder-idea.jpg",""),
  ("h3","First concept design"),
  ("fig","powder-concept.jpg",""),
  ("h3","Meeting our client"),
  ("p","After consulting our client online, we chose a different solution: a table with holes for infrared sensors and an omnidirectional skate, like a traditional powder board."),
  ("fig","powder-poc.jpg","Proof of concept"),
  ("fig","powder-wood.jpg","Woodworking the board"),
  ("fig","powder-wiring.jpg","Wiring the board"),
  ("h3","Final demonstration"),
  ("video","final_demo.mp4",""),
 ])

P["whistle-controlled-decorations"]=("Whistle Controlled Decorations","Turn off my lights from bed by whistling, with no remote and no controller.",
 [("Skills","Wiring circuits, reading and transmitting IR signals, Arduino libraries"),("Status","Working prototype")],
 [("fig","whistle-hero.jpg",""),
  ("h2","Objective"),
  ("p","My lamps are not near my bed, so I have to get up to turn them off before sleeping. I wanted to switch them off without getting up and without a remote or other controller. I'm good at whistling, so the idea was to control the lights by whistling."),
  ("h2","Components"),
  ("fig","whistle-mic.jpg","Microphone"),("fig","whistle-irrx.jpg","IR receiver"),("fig","whistle-irled.jpg","IR LED"),("fig","whistle-strip.jpg","LED strip"),
  ("p","I pointed the light strip's remote at the receiver circuit and recorded the hex values for power and several colors. Then I built the transmitter circuit, with match frequencies spaced 300 Hz apart, to send those commands."),
  ("fig","whistle-circuit.jpg",""),
  ("video","light_test_1.mp4","First test"),
  ("h2","Next steps"),
  ("ol",["Add a capacitor to smooth the input signal and avoid accidental triggering.","Adjust the code so inputs are more distinct, which allows more commands."]),
 ])

P["gravity-gambit-game"]=("Gravity Gambit","Design a two-player, 1v1 game. My small team designed three iterations.",
 [("My contribution","All CAD, laser cutting, the point trigger and collection system, and most of the large physical assembly"),("Skills","AutoCAD, laser cutting, teamwork")],
 [("fig","gambit-hero.jpg","The board detects balls thrown into the holes, counts the points automatically, and shows them on an LCD screen inset into the board."),
  ("p","I drew the CAD files for both the plinko board and the target board, laser cut the parts, designed the point trigger and collection system, and assembled most of the large parts."),
  ("fig","gambit-2.jpg",""),("fig","gambit-3.jpg",""),("fig","gambit-4.jpg",""),("fig","gambit-5.jpg",""),
 ])

P["chess-set"]=("Chess Set","A custom chess set themed on famous buildings, built as an exercise in SolidWorks CAD.",
 [("Tool","SolidWorks"),("Theme","Famous buildings")],
 [("fig","chess-hero-1.jpg",""),("fig","chess-hero-2.jpg",""),
  ("h3","Taipei 101: King"),("fig","chess-king.jpg",""),
  ("h3","Prudential Tower: Queen"),("fig","chess-queen.jpg",""),
  ("h3","One WTC: Bishop"),("fig","chess-bishop.jpg",""),
  ("h3","Empire State Building: Knight"),("fig","chess-knight.jpg",""),
  ("h3","Burj Khalifa: Rook"),("fig","chess-rook.jpg",""),
  ("h3","Leaning Tower of Pisa: Pawn"),
 ])


for i,(slug,title,summ,tags,thumb) in enumerate(PROJECTS):
    t,s,meta,blocks = P[slug]
    prev = PROJECTS[i-1][:2] if i>0 else None
    nxt = PROJECTS[i+1][:2] if i<len(PROJECTS)-1 else None
    project_page(slug,t,s,meta,blocks,f"<span>Project {i+1:02d}</span><span>/ {len(PROJECTS):02d}</span>"+(ONGOING_BADGE if slug in ONGOING else ""),
                 ("projects.html","All projects"),"projects",thumb,prev,nxt)

# ---- Notch
notch_meta=[("Role","Co-op"),("Tools","SolidWorks, Fusion 360, CNC machining, G-code, 3D printing"),("Focus","Radomes, automated painting, fume enclosure")]
notch_blocks=[
 ("p","Three projects from my co-op at Notch."),
 ("h2","Glass-fiber-reinforced polyurethane radomes"),
 ("p","I replaced brittle 3D-printed radomes with glass-fiber-reinforced polyurethane radomes by designing and 3D-printing the molds in SolidWorks. The new radomes are now on production units and survive 10 ft drops that shattered the previous version."),
 ("fig","notch-radome-1.jpg","A glass-fiber-reinforced polyurethane radome"),
 ("p","The previous radomes were 3D printed. We optimized them to be as strong and good looking as possible, but even with specialty filaments and extremely fine print resolution they were severely limited."),
 ("fig","notch-radome-2.jpg","Mold with PLA outer halves and a soft TPU inner shell"),
 ("p","The new radomes are cast in 3D-printed molds. The outer halves are hard, made from PLA. The inner shell is soft TPU with a rigid skeleton, so the mold comes apart easily after casting. The soft TPU part also leaves threaded inserts in the radome, which are used to mount the antenna inside."),
 ("fig","notch-radome-3.jpg","Mold with a vapor-smoothed ASA inner jacket"),
 ("p","This type of mold has a vapor-smoothed ASA inner jacket that leaves the cast radome with a smooth finish that needs no post-processing. On previous versions, sanding out the layer lines left by the molds took a lot of time and effort."),
 ("fig","notch-radome-4.jpg","[Caption]"),
 ("p","[Text: drop testing and results]"),
 ("fig","notch-radome-5.jpg","[Caption]"),
 ("p","[Text: the radomes on production units]"),
 ("h2","Automated paint application with a CNC spray gantry"),
 ("p","I automated a proprietary paint application process by building a CNC spray gantry and writing custom G-code to drive the paint gun. The project combined mechanical, electrical, and software design to produce consistent coats for a performance-sensitive application."),
 ("fig","notch-gantry-1.jpg","An early version of the spray gantry"),
 ("p","The gantry is built from an HVLP spray gun mounted on a commercial laser engraver. Air for the gun comes from a compressor, passes through a solenoid valve and a regulator, and then enters the gun."),
 ("fig","notch-gantry-2.jpg","The engraver's motherboard"),
 ("p","Controlling the spray with G-code is the best approach, and that means controlling the air through G-code too. To do that, I used a DMM to test different ports and G-code commands on the board, looking for one that gave a high/low output, which is what a solenoid needs. I found a working port that responds to mist coolant commands, and I built a driver circuit on it to switch the solenoid valve."),
 ("fig","notch-gantry-3.jpg","A spray pattern drawn in Fusion 360"),
 ("fig","notch-gantry-4.jpg","The Python script that processes the G-code"),
 ("p","Any pattern drawn in Fusion 360 can be turned into G-code, but that G-code has to be processed specifically for the spray gantry. I wrote a Python script that, among other things, wraps the spindle commands in coolant commands so the G-code switches the air on and off and applies the paint correctly."),
 ("fig","notch-gantry-5.jpg","Universal G-code Sender (UGS)"),
 ("p","After I send the G-code with UGS, the gantry goes to work."),
 ("yt","VIDEO_ID","The gantry applying a coat"),
 ("video","notch-gantry-video-2.mp4","[Caption]"),
 ("p","[Text: coating results and consistency]"),
 ("h2","Ventilated fume enclosure with active exhaust"),
 ("p","I enabled the automated coating process to run safely in-house by designing a ventilated fume enclosure with active exhaust in Fusion 360 and CNC-machining parts of it."),
 ("fig","notch-fume-1.jpg","CAD model of the full fume enclosure"),
 ("p","The enclosure frame is made from 8020, with polycarbonate panels cut to fit in the sides. 3D-printed clamps hold each panel in place and squeeze themselves tight when the sheet is inserted. A plastic cover is velcroed onto the front and sides to give access to the spray gantry."),
 ("fig","notch-fume-2.jpg","The control board and exhaust fan"),
 ("p","To ventilate the toxic fumes, I printed custom brackets that hold an exhaust fan in place and connected it to foil ducting that carries the fumes out through the window. To protect the board from the spray, I made another custom bracket that mounts the board and solenoid driver outside the enclosure."),
 ("fig","notch-fume-3.jpg","The complete enclosure"),
]
project_page("notch","Notch",EXPERIENCE[0][3],notch_meta,notch_blocks,"<span>Experience 01</span><span>/ 02</span>",
             ("index.html#work","All work"),"work",None,None,("sharkninja","SharkNinja"),pending=True)

# ---- SharkNinja
sn_meta=[("Role","Mechanical engineering co-op"),("Focus","Corded vacuums"),("Note","Unreleased product details are under NDA")]
sn_blocks=[
 ("loop","sn-transformer-transformation.mp4","The Shark PowerDetect Transformer, released in June 2026"),
 ("p","I worked on several projects at SharkNinja. One major project was a new type of vacuum, the Shark Transformer, which released in June 2026. Another was improving vacuum nozzle technology."),
 ("loop","sn-transformer-reveal.mp4",""),("loop","sn-transformer-versatility.mp4",""),("loop","sn-transformer-cleaningpower.mp4",""),
 ("link","https://www.sharkninja.com/shark-powerdetect-transformer-upright-vacuum/LX5000.html","See the Transformer on sharkninja.com"),
 ("p","Along the way I learned to design for manufacture (DFM) for plastic injection molding, navigate a PLM, use basic electrical test equipment, work in a laboratory, run provided tests and create my own, collect highly accurate data, present to leadership, and analyze and debug complex fluid and mechanical systems."),
 ("h2","Improved suction"),
 ("p","The goal was to improve suction while the vacuum is in use."),
 ("p","When our team received the first off-tool build, we saw several problems, and loss of suction force was the root cause. I designed and prototyped a component that changes the behavior of the internal airflow and drastically reduced the loss. I pressure tested it inside the unit and iterated several times."),
 ("fig","sn-suction-chart.jpg","Suction % as debris enters the system. Orange: legacy design. Blue: my design."),
 ("fig","sn-suction-2.jpg",""),
 ("p","Steel molds have been cut to produce the component at mass-production scale for a projected initial 500,000 units. The patent is still being processed."),
 ("h2","Castellation design for reverse cleaning"),
 ("p","I designed castellations to improve reverse cleaning, a requirement for vacuums in the EU that is likely to reach the US. A current solution is an articulating squeegee that flips up to let debris through on the backstroke. A common problem is that the brushroll shoots debris out the back during that backstroke."),
 ("video","LA490_spitting.mp4","Articulating squeegee (current design): severe debris spitting"),
 ("video","coil_14.1_spitting.mp4","Coiled castellations (my design): debris spitting highly mitigated"),
 ("p","The castellations are based on Tesla valves, which let flow pass much more easily in one direction than the other. In the video, the castellations create vortexes that keep debris from shooting out the back of the nozzle."),
 ("fig","sn-castellation-1.jpg",""),
 ("video","LA490_hf.mp4","Hard floor, current design: some debris spitting"),
 ("video","coil_14.1_hf.mp4","Hard floor, my design: much less debris spitting"),
 ("p","Hard floor results looked extremely promising. Last, I tested cleanability with sand spread over thick carpet (my own tests, not equivalent to third-party testing standards). Cleanability scores dropped too much. I concluded the castellations made the nozzle ride up on the carpet and lose suction, so I dropped the project."),
 ("fig","sn-carpet-1.jpg",""),("fig","sn-carpet-2.jpg",""),
 ("video","carpet_test_recording.mp4",""),
 ("h2","Valve door design"),
 ("p","I designed valve doors for a vacuum. Criteria:"),
 ("ul",["Don't stick out","Robust","No sliding contact that could wear down the seal"]),
 ("h2","Pressure and current testing"),
 ("p","One cleaning cycle needed a high pressure delta to work, but the motor ramp-up tripped home circuit breakers. I tested different cycle programs that lowered peak current while keeping a high pressure delta."),
 ("fig","sn-pressure-1.jpg","The newer program shows a much lower pressure delta."),
 ("p","Using an oscilloscope and a pressure sensor, I compared the old working program (orange, top) with the new failing one (blue, bottom)."),
 ("fig","sn-pressure-2.jpg",""),("fig","sn-pressure-3.jpg",""),
]
project_page("sharkninja","SharkNinja co-op","Corded vacuum design and testing: a patented airflow component, nozzle research, and test development.",sn_meta,sn_blocks,
             "<span>Experience 02</span><span>/ 02</span>",("index.html#work","All work"),"work",None,("notch","Notch"),("vtol","Projects: VTOL"))

# ---- projects index
page("projects.html","Projects","Mechanical, robotics, and electronics projects by Timothy Lee.",
 f"""<section class="list-page wrap">
<p class="kicker"><span>Index</span><span>/ {len(PROJECTS):02d} projects</span></p>
<h1>Projects</h1>
<p class="lede">Drones, soft robots, assistive devices, and a few things built for fun. Every one of them went through CAD, a prototype, and more than one redesign.</p>
{project_cards()}
</section>""","projects")

# ---- home
FIGS = [("vtol-hero.jpg","Fig. 01","VTOL airframe"),("hexa-hero.jpg","Fig. 02","Hexacopter frame"),("gripper-hero.jpg","Fig. 03","Soft gripper")]
figs = "".join(f'<figure class="hf hf{i+1}"><img src="images/{f}" alt="{esc(c)}" data-thumb><figcaption><span>{n}</span>{esc(c)}</figcaption></figure>' for i,(f,n,c) in enumerate(FIGS))
STATS = [("500k","projected initial units of my patent-pending SharkNinja airflow component"),
         ("2","patents pending: one at SharkNinja and one for CAS, a contamination-aware sampling venture"),
         ("$1,500","Northeastern PEAK research grant for a soft robotic gripper")]
stats = "".join(f'<div class="stat"><dt>{esc(v)}</dt><dd>{esc(d)}</dd></div>' for v,d in STATS)
home = f"""<section class="hero"><div class="wrap hero-in">
  <div class="hero-text">
    <p class="kicker"><span>Mechanical engineering</span><span>Northeastern University</span></p>
    <h1>Timothy<br>Lee<span class="dot" aria-hidden="true">.</span></h1>
    <p class="hero-sub">I design and build drones, soft robotic grippers, and consumer products, plus the molds and machines that make them, from CAD and simulation to the shop floor.</p>
    <p class="cta"><a class="btn" href="#work">See my work <span aria-hidden="true">↓</span></a><a class="btn ghost" href="#about">About me</a></p>
  </div>
  <div class="hero-art">{figs}</div>
</div></section>
<section class="stats-band"><dl class="wrap stats">{stats}</dl></section>
<section class="section wrap" id="work">
  <div class="sec-head"><p class="kicker"><span>01</span><span>Experience</span></p><h2>Work</h2></div>
  {xp_cards()}
</section>
<section class="section wrap" id="projects">
  <div class="sec-head"><p class="kicker"><span>02</span><span>Selected projects</span></p><h2>Projects</h2><a class="sec-link" href="projects.html">Project index <span aria-hidden="true">→</span></a></div>
  {project_cards()}
</section>
<section class="section wrap about" id="about">
  <div class="sec-head"><p class="kicker"><span>03</span><span>About</span></p><h2>Hi, I'm Timothy.</h2></div>
  <div class="about-body">
    <p class="about-lead">I'm a third-year mechanical engineering major at Northeastern University, from Boston, Massachusetts.</p>
    <p>I love throwing myself into new things, which has led me to hiking, camping, travel, competitive spikeball, table tennis, and other sports. At school I'm an active member of AerospaceNU and Rev, an entrepreneurship club.</p>
    <p>My first co-op was at SharkNinja, working on corded vacuums. My proudest achievement there was inventing a patented component that greatly improved the performance of a headlining Shark product.</p>
    <p>Next I want to learn as much as I can in industry, then take those skills out on my own and start a tech company.</p>
    <dl class="facts">
      <div><dt>Clubs</dt><dd>{tags_html(["AerospaceNU","Rev"])}</dd></div>
      <div><dt>Toolbox</dt><dd>{tags_html(["SolidWorks","Fusion 360","FEA","AutoCAD","3D printing","CNC","Laser cutting","Arduino","Python"])}</dd></div>
      <div><dt>Off the clock</dt><dd>{tags_html(["Hiking","Camping","Travel","Spikeball","Table tennis"])}</dd></div>
    </dl>
  </div>
</section>"""
page("index.html","Portfolio","Timothy Lee, mechanical engineering student at Northeastern University. Drones, soft robotics, and consumer product design.",home,"home")
print("built")
