import fitz
import os

PDF_PATH = '/Users/rozbehmobile/Downloads/Innovo Infra Presentation/Company Profile - Innovo Infra.pdf'
OUTPUT_DIR = '/Users/rozbehmobile/Downloads/Innovo Infra Presentation/extracted-images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Page → ordered list of meaningful image names
# Order matches PDF content stream (generally top-left to bottom-right)
PAGE_IMAGE_NAMES = {
    4: [  # Board of Directors
        'board-lord-philip-hammond-chairman',
        'board-bishoy-azmy-ceo',
        'board-mei-chen-non-exec-director',
        'board-juergen-maier-cbe-non-exec-director',
        'board-neil-martin-non-exec-director',
        'board-abdulaziz-bin-shafar-director',
        'board-tom-tildesley-cfo',
        'board-kate-teh-general-counsel',
    ],
    5: [  # Leadership Team (14 people)
        'leadership-bishoy-azmy-ceo-innovo-group',
        'leadership-mariam-azmy-chief-people-officer',
        'leadership-raouf-ezzat-ceo-innovo-international',
        'leadership-sameh-fam-ceo-innovo-build',
        'leadership-paul-woodman-ceo-capital-projects',
        'leadership-ibrahim-salib-ceo-real-estate',
        'leadership-tom-tildesley-cfo-innovo-group',
        'leadership-roger-wahl-cto-innovo-group',
        'leadership-kate-teh-general-counsel',
        'leadership-arsany-thabet-md-innovo-solutions',
        'leadership-rayan-el-eid-md-innovo-roads-infra',
        'leadership-mohamad-gamal-md-innovo-build-egypt',
        'leadership-khalid-sharbatly-md-innovo-mep',
        'leadership-ahmed-saleh-md-innovo-ventures',
    ],
    8: [  # Infrastructure MD Intro page
        'rayan-el-eid-managing-director-portrait',
    ],
    9: [  # Sectors of Expertise Part 1
        'sector-enabling-works-desert-earthworks',
        'sector-roads-roundabout-construction',
        'sector-bridges-bridge-under-construction',
        'sector-infrastructure-utilities-site',
        'sector-marine-works-aerial-view',
        'sector-landscape-completed-streetscape',
    ],
    10: [  # Sectors of Expertise Part 2
        'sector-pump-stations-construction',
        'sector-substations-building',
        'sector-ground-improvement-drilling-rig',
        'sector-ndrc-horizontal-directional-drilling',
        'sector-dewatering-equipment-site',
    ],
    12: [  # Innovo Offices & Awards
        'office-wellness-award-trophy',
        'office-dubai-interior-workspace',
        'office-guinness-world-record-badge',
        'office-top-employer-uae-2025-badge',
    ],
    13: [  # UAE 23+ Projects Map
        'uae-projects-overview-map',
        'uae-projects-map-site-01',
        'uae-projects-map-site-02',
        'uae-projects-map-site-03',
        'uae-projects-map-site-04',
        'uae-projects-map-site-05',
        'uae-projects-map-site-06',
        'uae-projects-map-site-07',
        'uae-projects-map-site-08',
        'uae-projects-map-site-09',
        'uae-projects-map-site-10',
        'uae-projects-map-site-11',
        'uae-projects-map-site-12',
    ],
    15: [  # Landscape Nursery Facility
        'nursery-greenhouse-interior-plants',
        'nursery-aerial-view-facility',
        'nursery-greenhouse-pathway-interior',
        'nursery-mature-tree-rows',
    ],
    16: [  # Nursery Stats & Photos
        'nursery-open-field-trees-01',
        'nursery-innovo-signage-entrance',
        'nursery-shaded-growing-area-01',
        'nursery-shaded-growing-area-02',
        'nursery-open-field-trees-02',
        'nursery-groundcover-production',
    ],
    17: [  # Nursery Landscape Photos
        'nursery-flowering-ruellia-plants',
        'nursery-tree-avenue-rows',
        'nursery-innovo-roads-signboard',
        'nursery-shade-house-trees',
    ],
    18: [  # Main Store
        'main-store-satellite-map-razeen-road',
        'main-store-aerial-photo',
    ],
    20: [  # Services - Enabling Works
        'service-enabling-works-earthworks-aerial',
        'service-enabling-works-grading-equipment-01',
        'service-enabling-works-grading-roller',
        'service-enabling-works-grading-equipment-02',
    ],
    21: [  # Services - Roadworks
        'service-roadworks-completed-roundabout-aerial',
        'service-roadworks-road-roller-compaction',
        'service-roadworks-cbr-testing',
        'service-roadworks-asphalt-paving',
    ],
    22: [  # Services - Infrastructure & Utilities
        'service-infrastructure-utilities-aerial-site',
        'service-infrastructure-utilities-pipe-trench',
        'service-infrastructure-utilities-pipe-installation',
        'service-infrastructure-utilities-large-pipe-laying',
    ],
    23: [  # Services - Structure Works
        'service-structure-works-bridge-aerial',
        'service-structure-works-underpass-construction',
        'service-structure-works-culvert-road',
        'service-structure-works-scaffolding-construction',
    ],
    24: [  # Services - Marine Works
        'service-marine-works-dredging-aerial',
        'service-marine-works-rock-revetment-construction',
        'service-marine-works-harbor-aerial-completed',
    ],
    25: [  # Services - Agriculture & Landscaping
        'service-landscape-completed-streetscape-furniture',
        'service-landscape-park-shade-structure',
        'service-landscape-coastal-roadside-planting',
        'service-landscape-tree-roundabout',
    ],
    27: [  # Technology - Drone, GPR, CCTV
        'tech-drone-survey-operator-road',
        'tech-gpr-operator-scanning-ground',
        'tech-gpr-pipe-detection-equipment',
        'tech-cctv-robotic-pipe-inspection',
        'tech-gpr-additional-view',
    ],
    28: [  # Technology - Crack Detection, Laser Scanning
        'tech-asphalt-crack-detection-vehicle',
        'tech-laser-scanning-survey-team-01',
        'tech-laser-scanning-road-marking-vehicle',
    ],
    29: [  # Technology - Power BI & BIM
        'tech-powerbi-live-dashboard-screenshot',
        'tech-bim-3d-model-infrastructure-01',
        'tech-bim-3d-model-infrastructure-02',
    ],
    33: [  # Ongoing Projects - Dubai Master + Eden Hills
        'project-dubai-master-developments-site-plan',
        'project-eden-hills-villas-aerial-render',
    ],
    34: [  # Ongoing Projects - Ghaf Woods + Dubai Police
        'project-ghaf-woods-infrastructure-aerial-render',
        'project-dubai-police-academy-aerial-render',
    ],
    35: [  # Ongoing Projects - Golf Lane + Grand Polo
        'project-shallow-services-golf-lane-master-plan',
        'project-grand-polo-club-resort-aerial',
    ],
    36: [  # Ongoing Projects - E11 + Prime Dubai
        'project-e11-tie-in-siniya-island-aerial',
        'project-prime-dubai-arm-holding-render',
    ],
    37: [  # Ongoing Projects - Valley Mid Parcel + Flood Protection
        'project-valley-mid-parcel-emaar-aerial-render',
        'project-junction-b-flood-protection-sharjah-map',
    ],
    38: [  # Ongoing Projects - Dubai South + Saadiyat Lagoons
        'project-boulevard-roads-dubai-south-render',
        'project-saadiyat-lagoons-pkg3-aerial-render',
    ],
    39: [  # Ongoing Projects - Al Faya + Bloom Living
        'project-al-faya-razeen-street-lighting-night',
        'project-bloom-living-abu-dhabi-render',
    ],
    40: [  # Ongoing Projects - Al Sader + Al Wiqan
        'project-al-sader-housing-infrastructure-plan',
        'project-al-wiqan-roads-232-plots-map',
    ],
    41: [  # Ongoing Projects - North Al Bahia + Naseem Al Jurf
        'project-north-al-bahia-residential-aerial-render',
        'project-naseem-al-jurf-phase3b-aerial-render',
    ],
    44: [  # Completed Projects - Mudon + Nad Al Sheba
        'completed-mudon-central-park-ph56-aerial-render',
        'completed-nad-al-sheba-gardens-park-aerial',
    ],
    45: [  # Completed Projects - Haven-Athlon + Marsa Al Arab
        'completed-haven-athlon-wilds-enabling-aerial',
        'completed-marsa-al-arab-storm-water-burj-al-arab',
    ],
    46: [  # Completed Projects - Al Qou'a Al Ain
        'completed-al-qoua-al-ain-262-plots-aerial-render',
    ],
    48: [  # Machinery & Equipment photos
        'machinery-fleet-parade-overview',
        'machinery-motor-grader',
        'machinery-excavators-fleet',
        'machinery-compactors-rollers-fleet',
        'machinery-bulldozers-fleet',
    ],
    50: [  # Staff photos
        'staff-team-innovo-branded-site-group',
        'staff-team-uae-national-day',
        'staff-team-celebration-indoor',
    ],
    60: [  # ISO Certificates
        'certificate-iso-14001-2015-environmental',
        'certificate-iso-9001-2015-quality',
        'certificate-iso-45001-2018-ohs',
    ],
    61: [  # ICV Certificate
        'certificate-icv-abu-dhabi-61percent',
    ],
    62: [  # OSHMS Certificate
        'certificate-oshms-adphc-approval',
    ],
}

MIN_W, MIN_H = 80, 80
MIN_AREA = MIN_W * MIN_H

doc = fitz.open(PDF_PATH)
extracted = []
seen_xrefs = set()

for page_num in range(len(doc)):
    page_idx = page_num + 1
    page = doc[page_num]
    images = page.get_images(full=True)

    if page_idx not in PAGE_IMAGE_NAMES:
        continue

    names = PAGE_IMAGE_NAMES[page_idx]

    meaningful = []
    for img in images:
        xref = img[0]
        if xref in seen_xrefs:
            continue
        base = doc.extract_image(xref)
        w, h = base['width'], base['height']
        if w >= MIN_W and h >= MIN_H and w * h >= MIN_AREA:
            meaningful.append((xref, base))

    print(f"\nPage {page_idx}: {len(images)} total images → {len(meaningful)} meaningful")

    for i, (xref, base) in enumerate(meaningful):
        name = names[i] if i < len(names) else f'page{page_idx}-extra-{i+1}'
        ext = base['ext']
        if ext in ('jpx', 'jp2'):
            ext = 'jpg'
        filename = f'{name}.{ext}'
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(base['image'])
        seen_xrefs.add(xref)
        extracted.append(filename)
        print(f"  [{i+1}] {filename}  ({base['width']}x{base['height']})")

doc.close()
print(f"\n✓ Done. {len(extracted)} images saved to: {OUTPUT_DIR}")
