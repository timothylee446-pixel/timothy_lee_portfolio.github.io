import html, os

SITE = "Timothy Lee"
NAV = [("index.html","Home"),("sharkninja.html","SharkNinja co-op"),("projects.html","Projects")]

PROJECTS = [
 ("vtol","VTOL","Quadcopter VTOL UAV with an FEA-validated wing structure."),
 ("hexacopter","Hexacopter","Drone frame for a 20 lb payload, plus a modular tool-changing system."),
 ("pneumatic-gripper","Pneumatic Gripper","Soft robotic gripper for a drone, funded by a $1,500 PEAK grant."),
 ("assistive-powder-board","Assistive Powder Board","Low-cost powder board that motivates children in wheelchairs to do physical therapy."),
 ("whistle-controlled-decorations","Whistle Controlled Decorations","Arduino circuit that switches a light strip when I whistle."),
 ("gravity-gambit-game","Gravity Gambit","Two-player plinko and target game with automatic scoring."),
 ("chess-set","Chess Set","SolidWorks chess set themed on famous buildings."),
]

def esc(s): return html.escape(s, quote=True)

def render_blocks(blocks):
    out=[]
    for b in blocks:
        k=b[0]
        if k=="h2": out.append(f"<h2>{esc(b[1])}</h2>")
        elif k=="h3": out.append(f"<h3>{esc(b[1])}</h3>")
        elif k=="p": out.append(f"<p>{esc(b[1])}</p>")
        elif k=="ul": out.append("<ul>"+"".join(f"<li>{esc(i)}</li>" for i in b[1])+"</ul>")
        elif k=="ol": out.append("<ol>"+"".join(f"<li>{esc(i)}</li>" for i in b[1])+"</ol>")
        elif k=="fig":
            cap = f"<figcaption>{esc(b[2])}</figcaption>" if len(b)>2 and b[2] else ""
            out.append(f'<figure><img src="images/{b[1]}" alt="{esc(b[2]) if len(b)>2 else ""}" loading="lazy" data-name="{b[1]}">{cap}</figure>')
        elif k=="video":
            cap = f"<figcaption>{esc(b[2])}</figcaption>" if len(b)>2 and b[2] else ""
            out.append(f'<figure><video controls preload="metadata" src="videos/{b[1]}" data-name="{b[1]}"></video>{cap}</figure>')
        elif k=="yt":
            out.append(f'<figure class="embed"><iframe src="https://www.youtube.com/embed/{b[1]}" title="{esc(b[2])}" loading="lazy" allowfullscreen></iframe><figcaption>{esc(b[2])}</figcaption></figure>')
        elif k=="link":
            out.append(f'<p><a class="ext" href="{b[1]}">{esc(b[2])}</a></p>')
    return "\n".join(out)

def page(fname, title, desc, body, current):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{esc(t)}</a>' for h,t in NAV)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {SITE}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="index.html">{SITE}</a>
  <nav aria-label="Main">{nav}</nav>
</header>
<main>
{body}
</main>
<footer>
  <p>{SITE}, mechanical engineering at Northeastern University. Boston, MA.</p>
</footer>
<script src="site.js"></script>
</body>
</html>
"""
    open(fname,"w",encoding="utf-8").write(doc)

def project_page(slug,title,summary,meta,blocks,back=("projects.html","All projects")):
    metahtml = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k,v in meta)
    body = f"""<article class="project">
<a class="back" href="{back[0]}">{esc(back[1])}</a>
<h1>{esc(title)}</h1>
<p class="lede">{esc(summary)}</p>
<dl class="meta">{metahtml}</dl>
{render_blocks(blocks)}
</article>"""
    page(f"{slug}.html", title, summary, body, back[0])

# ---------------- content ----------------
P = {}

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

for slug,title,summ in PROJECTS:
    t,s,meta,blocks = P[slug]
    project_page(slug,t,s,meta,blocks)

# ---- SharkNinja
sn_meta=[("Role","Mechanical engineering co-op"),("Focus","Corded vacuums"),("Note","Unreleased product details are under NDA")]
sn_blocks=[
 ("p","I worked on several projects at SharkNinja. One major project was a new type of vacuum set to release in May 2026. Another was improving vacuum nozzle technology."),
 ("p","Along the way I learned to design for manufacture (DFM) for plastic injection molding, navigate a PLM, use basic electrical test equipment, work in a laboratory, run provided tests and create my own, collect highly accurate data, present to leadership, and analyze and debug complex fluid and mechanical systems."),
 ("h2","Improved suction"),
 ("p","The goal was to improve suction while the vacuum is in use. The product is unreleased and the specifics are under NDA."),
 ("p","When our team received the first off-tool build, we saw several problems, and loss of suction force was the root cause. I designed and prototyped a component that changes the behavior of the internal airflow and drastically reduced the loss. I pressure tested it inside the unit and iterated several times."),
 ("fig","sn-suction-chart.jpg","Suction % as debris enters the system. Orange: legacy design. Blue: my design."),
 ("fig","sn-suction-2.jpg",""),
 ("p","Steel molds are being cut to produce the component at mass-production scale, for 500,000 units over the next three years. The patent is still being processed."),
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
project_page("sharkninja","SharkNinja co-op","Corded vacuum design and testing: a patented airflow component, nozzle research, and test development.",sn_meta,sn_blocks,back=("index.html","Home"))
# fix nav highlight for sharkninja
s=open("sharkninja.html",encoding="utf-8").read()
s=s.replace('<a href="index.html">Home</a>','<a href="index.html">Home</a>',1)
open("sharkninja.html","w",encoding="utf-8").write(s)

# ---- projects index
rows="".join(f'<li><a href="{s}.html"><span class="t">{esc(t)}</span><span class="d">{esc(d)}</span></a></li>' for s,t,d in PROJECTS)
page("projects.html","Projects","Mechanical, robotics, and electronics projects by Timothy Lee.",
 f'<section class="list-page"><h1>Projects</h1><ul class="rows">{rows}</ul></section>',"projects.html")

# ---- home
home = f"""<section class="hero">
  <h1>Timothy Lee</h1>
  <p class="hero-sub">Mechanical engineering student at Northeastern University, building drones, grippers, and consumer products.</p>
</section>
<section class="about">
  <p>I'm a third-year mechanical engineering major at Northeastern University, from Boston, Massachusetts. I love throwing myself into new things, which has led me to hiking, camping, travel, competitive spikeball, table tennis, and other sports. At school I'm an active member of AerospaceNU and Rev, an entrepreneurship club.</p>
  <p>My first co-op was at SharkNinja, working on corded vacuums. My proudest achievement there was inventing a patented component that greatly improved the performance of a headlining Shark product.</p>
  <p>Next I want to learn as much as I can in industry, then take those skills out on my own and start a tech company.</p>
</section>
<section class="featured">
  <h2>Experience</h2>
  <ul class="rows">
    <li><a href="sharkninja.html"><span class="t">SharkNinja co-op</span><span class="d">A patented airflow component headed for 500,000 units, Tesla-valve nozzle research, and test development.</span></a></li>
  </ul>
  <h2>Projects</h2>
  <ul class="rows">{rows}</ul>
</section>"""
page("index.html","Portfolio","Timothy Lee, mechanical engineering student at Northeastern University. Drones, soft robotics, and consumer product design.",home,"index.html")
print("built")
