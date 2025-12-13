PEST_DB = {

# --------------------------------------------------
# 🌴 ARECA NUT
# --------------------------------------------------
"areca nut": {
    "Mite Infestation": {
        "temp_gt": 30,
        "humidity_lt": 60,
        "rainfall_lt": 1000,
        "season": ["February", "March", "April"],
        "stage": ["pre_planting", "planting_cultivation", "fruiting"],
        "symptoms": "Brown nuts, rough husk, webbing.",
        "preventive": "Maintain irrigation, avoid drought stress.",
        "corrective": "Spray neem oil 0.5% or sulphur dust."
    },
    "Yellow Leaf Disease": {
        "rainfall_gt": 1800,
        "humidity_gt": 80,
        "season": ["July", "August", "September"],
        "stage": ["vegetative"],
        "symptoms": "Midrib yellowing, leaf drooping.",
        "preventive": "Improve drainage, apply lime.",
        "corrective": "Trichoderma root feeding + Bordeaux spray."
    }
},

# --------------------------------------------------
# 🌾 PADDY / RICE
# --------------------------------------------------
"paddy": {
    "Blast Disease": {
        "humidity_gt": 85,
        "temp_range": [18, 28],
        "season": ["July", "August", "September"],
        "symptoms": "Spindle-shaped lesions on leaves.",
        "preventive": "Avoid excess urea, maintain spacing.",
        "corrective": "Spray Tricyclazole 0.6 gm/ltr."
    },
    "Brown Planthopper": {
        "humidity_gt": 80,
        "temp_gt": 28,
        "season": ["August", "September", "October"],
        "symptoms": "Hopper burn patches in field.",
        "preventive": "Avoid over-irrigation, maintain field sanitation.",
        "corrective": "Spray Buprofezin 1 ml/ltr."
    }
},

# --------------------------------------------------
# 🌿 COTTON
# --------------------------------------------------
"cotton": {
    "Pink Bollworm": {
        "temp_range": [26, 34],
        "humidity_gt": 60,
        "season": ["September", "October", "November"],
        "symptoms": "Pink larvae inside boll, rosette flowers.",
        "preventive": "Use pheromone traps, timely sowing.",
        "corrective": "Spray Emamectin Benzoate 0.4 gm/ltr."
    },
    "Whitefly": {
        "temp_gt": 32,
        "humidity_gt": 70,
        "symptoms": "Honeydew deposits, sooty mold.",
        "preventive": "Remove alternate hosts, use sticky traps.",
        "corrective": "Spray Neem oil or Imidacloprid 0.3 ml/ltr."
    }
},

# --------------------------------------------------
# 🌽 MAIZE
# --------------------------------------------------
"maize": {
    "Fall Armyworm": {
        "temp_range": [22, 30],
        "humidity_gt": 60,
        "season": ["June", "July", "August"],
        "symptoms": "Whorl feeding, window-pane damage.",
        "preventive": "Apply neem cake 50kg/acre.",
        "corrective": "Spray Emamectin Benzoate 0.4 gm/ltr."
    },
    "Stem Borer": {
        "temp_gt": 30,
        "humidity_gt": 70,
        "symptoms": "Dead heart symptoms in early stage.",
        "preventive": "Use light traps and timely planting.",
        "corrective": "Apply Carbofuran 3G."
    }
},

# --------------------------------------------------
# 🌾 RAGI (Finger Millet)
# --------------------------------------------------
"ragi": {
    "Blast Disease": {
        "humidity_gt": 80,
        "temp_range": [20, 28],
        "season": ["July", "August"],
        "symptoms": "Diamond-shaped lesions on leaf.",
        "preventive": "Use resistant varieties, avoid late sowing.",
        "corrective": "Spray Carbendazim 1 gm/ltr."
    }
},

# --------------------------------------------------
# 🥜 GROUNDNUT
# --------------------------------------------------
"groundnut": {
    "Leaf Miner": {
        "temp_gt": 30,
        "season": ["June", "July", "August"],
        "symptoms": "Silvery leaf tunnels.",
        "preventive": "Use pheromone traps.",
        "corrective": "Spray Chlorantraniliprole 0.3 ml/ltr."
    },
    "Tikka Leaf Spot": {
        "humidity_gt": 80,
        "temp_range": [20, 30],
        "symptoms": "Brown circular spots on leaves.",
        "preventive": "Use disease-free seeds.",
        "corrective": "Spray Mancozeb 2 gm/ltr."
    }
},

# --------------------------------------------------
# 🍌 BANANA
# --------------------------------------------------
"banana": {
    "Sigatoka Leaf Spot": {
        "humidity_gt": 80,
        "temp_range": [25, 32],
        "symptoms": "Yellow streaks turning into brown spots.",
        "preventive": "Improve aeration, remove infected leaves.",
        "corrective": "Spray Propiconazole 1 ml/ltr."
    },
    "Banana Weevil": {
        "temp_gt": 28,
        "symptoms": "Tunneling in pseudostem.",
        "preventive": "Use clean suckers.",
        "corrective": "Apply Carbofuran at base."
    }
},

# --------------------------------------------------
# 🌱 TURMERIC
# --------------------------------------------------
"turmeric": {
    "Rhizome Rot": {
        "rainfall_gt": 1500,
        "humidity_gt": 85,
        "symptoms": "Yellowing & rotting of rhizomes.",
        "preventive": "Ensure proper drainage.",
        "corrective": "Drench with Copper Oxychloride 3 gm/ltr."
    }
},

# --------------------------------------------------
# 🍬 SUGARCANE
# --------------------------------------------------
"sugarcane": {
    "Early Shoot Borer": {
        "temp_gt": 28,
        "season": ["March", "April", "May"],
        "symptoms": "Dead hearts in early growth.",
        "preventive": "Trash mulching.",
        "corrective": "Apply Chlorantraniliprole granules."
    },
    "Red Rot": {
        "humidity_gt": 70,
        "rainfall_gt": 1200,
        "symptoms": "Red discoloration, foul smell in stem.",
        "preventive": "Use resistant varieties.",
        "corrective": "Remove infected clumps."
    }
},

# --------------------------------------------------
# 🌶 CHILLI
# --------------------------------------------------
"chilli": {
    "Thrips": {
        "temp_range": [25, 32],
        "humidity_lt": 60,
        "symptoms": "Leaf curl, silver streaks.",
        "preventive": "Avoid monocropping.",
        "corrective": "Spray Spinosad 0.3 ml/ltr."
    },
    "Powdery Mildew": {
        "temp_lt": 28,
        "humidity_gt": 70,
        "symptoms": "White fungal growth on leaves.",
        "preventive": "Increase spacing.",
        "corrective": "Spray Sulphur 2 gm/ltr."
    }
},

# --------------------------------------------------
# ☕ COFFEE
# --------------------------------------------------
"coffee": {
    "White Stem Borer": {
        "temp_gt": 28,
        "season": ["March", "April", "May"],
        "symptoms": "Exit holes on stem, yellowing leaves.",
        "preventive": "Shade regulation.",
        "corrective": "Remove and burn affected stems."
    },
    "Leaf Rust": {
        "humidity_gt": 85,
        "symptoms": "Orange rust spots under leaves.",
        "preventive": "Use resistant varieties.",
        "corrective": "Spray Bordeaux mixture."
    }
},

# --------------------------------------------------
# 🌶 PEPPER
# --------------------------------------------------
"pepper": {
    "Quick Wilt": {
        "rainfall_gt": 2000,
        "humidity_gt": 80,
        "season": ["July", "August", "September"],
        "symptoms": "Sudden wilting & dropping leaves.",
        "preventive": "Improve drainage & apply Trichoderma.",
        "corrective": "Drench with Metalaxyl 2 gm/ltr."
    },
    "Pollu Beetle": {
        "temp_gt": 28,
        "symptoms": "Bored holes in berries.",
        "preventive": "Keep field clean.",
        "corrective": "Use pheromone traps."
    }
},

# --------------------------------------------------
# 🍅 TOMATO
# --------------------------------------------------
"tomato": {
    "Fruit Borer": {
        "temp_range": [25, 30],
        "symptoms": "Bored holes in fruits.",
        "preventive": "Use pheromone traps.",
        "corrective": "Spray Emamectin Benzoate 0.4 gm/ltr."
    },
    "Leaf Curl Virus": {
        "humidity_lt": 60,
        "symptoms": "Curled & yellowed leaves.",
        "preventive": "Control whiteflies.",
        "corrective": "Spray Imidacloprid."
    }
},

# --------------------------------------------------
# 🧅 ONION
# --------------------------------------------------
"onion": {
    "Purple Blotch": {
        "humidity_gt": 85,
        "symptoms": "Purple lesions with yellow halo.",
        "preventive": "Good spacing and airflow.",
        "corrective": "Spray Mancozeb."
    }
},

# --------------------------------------------------
# 🍇 GRAPES
# --------------------------------------------------
"grapes": {
    "Downy Mildew": {
        "humidity_gt": 85,
        "temp_range": [18, 26],
        "symptoms": "Oily spots on upper leaf surface.",
        "preventive": "Maintain canopy.",
        "corrective": "Spray Metalaxyl."
    },
    "Powdery Mildew": {
        "humidity_lt": 60,
        "temp_range": [20, 30],
        "symptoms": "White powdery patches.",
        "preventive": "Improve aeration.",
        "corrective": "Spray Sulphur."
    }
},
# --------------------------------------------------
# 🌱 SOYBEAN
# --------------------------------------------------
"soybean": {
    "Girdle Beetle": {
        "temp_range": [25, 32],
        "humidity_gt": 65,
        "symptoms": "Girdled stem near base, drying leaves.",
        "preventive": "Deep ploughing, remove alternate hosts.",
        "corrective": "Spray Quinalphos 2 ml/ltr."
    },
    "Yellow Mosaic Virus": {
        "humidity_lt": 60,
        "symptoms": "Bright yellow patches on leaves.",
        "preventive": "Control whiteflies.",
        "corrective": "Spray Imidacloprid 0.3 ml/ltr."
    }
},

# --------------------------------------------------
# 🌻 SUNFLOWER
# --------------------------------------------------
"sunflower": {
    "Powdery Mildew": {
        "humidity_lt": 65,
        "temp_range": [18, 27],
        "symptoms": "White powder on leaves.",
        "preventive": "Wide spacing, resistant varieties.",
        "corrective": "Spray Sulphur 2g/ltr."
    },
    "Cutworm": {
        "temp_gt": 25,
        "symptoms": "Cut seedlings at ground level.",
        "preventive": "Clean cultivation.",
        "corrective": "Apply Chlorpyrifos bait."
    }
},

# --------------------------------------------------
# 🌾 JOWAR (SORGHUM)
# --------------------------------------------------
"jowar": {
    "Shoot Fly": {
        "temp_gt": 28,
        "symptoms": "Dead heart in seedlings.",
        "preventive": "Timely sowing before June 15.",
        "corrective": "Spray Dimethoate 2 ml/ltr."
    },
    "Anthracnose": {
        "humidity_gt": 75,
        "symptoms": "Circular leaf spots with concentric rings.",
        "preventive": "Use disease-free seeds.",
        "corrective": "Spray Mancozeb 2g/ltr."
    }
},

# --------------------------------------------------
# 🌾 WHEAT
# --------------------------------------------------
"wheat": {
    "Rust": {
        "temp_range": [12, 22],
        "humidity_gt": 80,
        "symptoms": "Rusty orange pustules on leaves.",
        "preventive": "Use rust-resistant varieties.",
        "corrective": "Spray Propiconazole 1 ml/ltr."
    }
},

# --------------------------------------------------
# 🌿 HORSE GRAM
# --------------------------------------------------
"horse gram": {
    "Leaf Spot": {
        "humidity_gt": 70,
        "symptoms": "Irregular brown spots.",
        "preventive": "Use clean seeds.",
        "corrective": "Spray Carbendazim 1g/ltr."
    }
},

# --------------------------------------------------
# 🌿 GREEN GRAM
# --------------------------------------------------
"green gram": {
    "Pod Borer": {
        "temp_range": [22, 30],
        "symptoms": "Holes on pods, feeding damage.",
        "preventive": "Use pheromone traps.",
        "corrective": "Spray Emamectin Benzoate."
    }
},

# --------------------------------------------------
# 🌿 BLACK GRAM
# --------------------------------------------------
"black gram": {
    "Aphids": {
        "temp_range": [18, 28],
        "humidity_gt": 60,
        "symptoms": "Black insects on tender leaves.",
        "preventive": "Apply neem oil.",
        "corrective": "Spray Imidacloprid."
    }
},

# --------------------------------------------------
# 🌿 PIGEON PEA (TUR DAL)
# --------------------------------------------------
"pigeon pea": {
    "Pod Fly": {
        "temp_gt": 28,
        "symptoms": "Tunnels in pods, premature pod drop.",
        "preventive": "Remove crop residue.",
        "corrective": "Spray Cypermethrin."
    }
},

# --------------------------------------------------
# 🍉 CUCUMBER / MELONS
# --------------------------------------------------
"cucumber": {
    "Powdery Mildew": {
        "humidity_lt": 55,
        "temp_range": [23, 28],
        "symptoms": "White powdery patches.",
        "preventive": "Avoid dense planting.",
        "corrective": "Spray Sulphur."
    },
    "Downy Mildew": {
        "humidity_gt": 80,
        "symptoms": "Yellow angular leaf spots.",
        "preventive": "Improve aeration.",
        "corrective": "Spray Metalaxyl."
    }
},

# --------------------------------------------------
# 🍉 WATERMELON
# --------------------------------------------------
"watermelon": {
    "Fruit Rot": {
        "humidity_gt": 80,
        "symptoms": "Sunken lesions on rind.",
        "preventive": "Avoid water logging.",
        "corrective": "Spray Carbendazim."
    }
},

# --------------------------------------------------
# 🍍 PAPAYA
# --------------------------------------------------
"papaya": {
    "Papaya Mealybug": {
        "humidity_gt": 75,
        "temp_range": [25, 32],
        "symptoms": "White waxy clusters with honeydew.",
        "preventive": "Introduce parasitoids.",
        "corrective": "Spray Neem oil 2%."
    },
    "Ring Spot Virus": {
        "symptoms": "Ring marks on fruits and mosaic on leaves.",
        "preventive": "Remove infected plants.",
        "corrective": "Control aphids."
    }
},

# --------------------------------------------------
# 🥭 MANGO
# --------------------------------------------------
"mango": {
    "Powdery Mildew": {
        "humidity_lt": 60,
        "temp_range": [20, 30],
        "symptoms": "White powder on panicles.",
        "preventive": "Maintain orchard aeration.",
        "corrective": "Spray Wettable sulphur."
    },
    "Fruit Fly": {
        "temp_gt": 28,
        "season": ["April", "May", "June"],
        "symptoms": "Maggots in ripening fruits.",
        "preventive": "Use methyl eugenol traps.",
        "corrective": "Destroy fallen fruits."
    }
},

# --------------------------------------------------
# 🍎 GUAVA
# --------------------------------------------------
"guava": {
    "Fruit Borer": {
        "temp_range": [25, 32],
        "symptoms": "Bore holes on fruits.",
        "preventive": "Bag the fruits.",
        "corrective": "Spray Spinosad."
    }
},

# --------------------------------------------------
# 🍆 BRINJAL
# --------------------------------------------------
"brinjal": {
    "Shoot and Fruit Borer": {
        "temp_gt": 30,
        "symptoms": "Bored holes in fruit & wilted shoots.",
        "preventive": "Use pheromone traps.",
        "corrective": "Spray Emamectin Benzoate."
    }
},

# --------------------------------------------------
# 🥬 CABBAGE / CAULIFLOWER
# --------------------------------------------------
"cabbage": {
    "Diamondback Moth": {
        "temp_range": [20, 28],
        "symptoms": "Skeletonized leaves.",
        "preventive": "Remove weeds.",
        "corrective": "Spray Spinosad."
    }
},

"cauliflower": {
    "Black Rot": {
        "humidity_gt": 80,
        "symptoms": "V-shaped yellow lesions.",
        "preventive": "Use certified seeds.",
        "corrective": "Spray Copper Oxychloride."
    }
},

# --------------------------------------------------
# 🌿 SPINACH / LEAFY GREENS
# --------------------------------------------------
"spinach": {
    "Leaf Miner": {
        "temp_range": [18, 28],
        "symptoms": "Irregular tunnels in leaves.",
        "preventive": "Remove infested leaves.",
        "corrective": "Spray Neem oil."
    }
},

# --------------------------------------------------
# 🌿 CORIANDER
# --------------------------------------------------
"coriander": {
    "Stem Rot": {
        "humidity_gt": 85,
        "symptoms": "Rotting of stem base.",
        "preventive": "Ensure drainage.",
        "corrective": "Spray Carbendazim."
    }
},

}
