from flask import Flask, render_template, jsonify, request
import random
import json

app = Flask(__name__)

# Store the last recommended item in memory (no database needed)
last_recommended_item = None

# Comprehensive list of recommended items based on our analysis
RECOMMENDED_ITEMS = [
    # Plant-Based Expansion (High Priority)
    {
        "name": "PRSL PLT BF GRD ALT 80/20",
        "description": "Artisanal plant-based ground beef alternative with premium pea protein",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Captures growing plant-based market with 15-20% annual growth"
    },
    {
        "name": "PRSL PLT CHK STRIPS GNG",
        "description": "Crispy plant-based chicken strips with golden breading",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Perfect alternative to your top-selling chicken products"
    },
    {
        "name": "PRSL PLT SSG ITALIAN PK",
        "description": "Savory plant-based Italian sausage with fennel and herbs",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Expands your sausage line with sustainable option"
    },
    {
        "name": "PRSL PLT CHS SHRED MOZZ",
        "description": "Creamy plant-based mozzarella shreds that melt perfectly",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Complements your strong cheese category"
    },
    {
        "name": "PRSL PLT YGT VAN PROB",
        "description": "Luxurious plant-based probiotic yogurt with Madagascar vanilla",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Combines plant-based trend with functional foods"
    },
    {
        "name": "PRSL PLT ICE CRM CHOC",
        "description": "Decadent plant-based chocolate ice cream with Belgian cocoa",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Premium frozen dessert for health-conscious consumers"
    },
    
    # Functional Foods & Health Trends (High Priority)
    {
        "name": "PRSL KOMBUCHA GINGER TURM",
        "description": "Sparkling kombucha with fresh ginger and golden turmeric",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Gut health trend with 25% annual growth"
    },
    {
        "name": "PRSL KIMCHI TRAD KOREAN",
        "description": "Authentic traditional Korean kimchi with napa cabbage and gochugaru",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Fermented foods for digestive health"
    },
    {
        "name": "PRSL PROB YGT MIX BERRY",
        "description": "Creamy probiotic yogurt with antioxidant-rich mixed berries",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Health-focused consumers seeking functional benefits"
    },
    {
        "name": "PRSL ADAPT TEA ASHWAGAND",
        "description": "Soothing adaptogen tea with ancient ashwagandha root",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Stress relief and wellness positioning"
    },
    {
        "name": "PRSL SUPERFRT SMOOTHIE PK",
        "description": "Nutrient-dense superfruit smoothie packs with acai and goji",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Convenient superfood nutrition"
    },
    {
        "name": "PRSL GUT HLTH GRANOLA",
        "description": "Prebiotic-rich gut health granola with ancient grains",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Breakfast category with health benefits"
    },
    
    # Global Fusion & Ethnic Flavors (Medium Priority)
    {
        "name": "PRSL UBE SWT POTATO CHIPS",
        "description": "Crispy Filipino ube sweet potato chips with purple yam",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "International flavors attracting diverse demographics"
    },
    {
        "name": "PRSL YUZU CITRUS DRSNG",
        "description": "Zesty Japanese yuzu citrus dressing with sesame oil",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Asian cuisine trend in mainstream markets"
    },
    {
        "name": "PRSL SUYA SPICE BLEND",
        "description": "Aromatic West African suya spice blend with peanuts",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "African flavors gaining popularity"
    },
    {
        "name": "PRSL TACO SEASONING PK",
        "description": "Authentic Mexican taco seasoning packet with chipotle",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Hispanic market expansion"
    },
    {
        "name": "PRSL CURRY PASTE THAI",
        "description": "Fragrant Thai curry paste with lemongrass and galangal",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Southeast Asian cuisine popularity"
    },
    {
        "name": "PRSL HARISSA SPICE MIX",
        "description": "Fiery North African harissa spice mix with roasted peppers",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Middle Eastern and North African flavors"
    },
    
    # Sustainable & Zero-Waste Products (Medium Priority)
    {
        "name": "PRSL VEG SCRAP CHIPS MIX",
        "description": "Crispy vegetable scrap chips variety pack from upcycled produce",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Zero-waste cooking trend and sustainability"
    },
    {
        "name": "PRSL UPCLD BREAD CRUMBS",
        "description": "Golden upcycled bread crumbs from artisan sourdough",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Food waste reduction and circular economy"
    },
    {
        "name": "PRSL REGEN BEEF GRD",
        "description": "Grass-fed regenerative agriculture beef from sustainable farms",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Environmental consciousness in meat category"
    },
    {
        "name": "PRSL COMPOST PKG CHIPS",
        "description": "Crispy chips in fully compostable packaging",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Eco-friendly packaging innovation"
    },
    {
        "name": "PRSL ZERO WASTE SOUP",
        "description": "Hearty zero-waste vegetable soup with root-to-stem cooking",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Sustainability-focused prepared foods"
    },
    
    # Premium Snacks & Convenience (Medium Priority)
    {
        "name": "PRSL ARTISAN CRACKER MIX",
        "description": "Handcrafted artisan cracker variety mix with sea salt",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Premium snacking market expansion"
    },
    {
        "name": "PRSL GOURMET NUT BLEND",
        "description": "Luxurious gourmet mixed nuts blend with Himalayan salt",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "High-margin snack category"
    },
    {
        "name": "PRSL PROTEIN BALLS 6CT",
        "description": "Nutritious protein energy balls 6-count with dates and nuts",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Health-focused convenience snacks"
    },
    {
        "name": "PRSL DARK CHOC TRUFFLES",
        "description": "Decadent dark chocolate truffles with single-origin cocoa",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Premium dessert and gifting category"
    },
    {
        "name": "PRSL SEAWEED SNACK MIX",
        "description": "Crispy seaweed snack variety mix with sesame seasoning",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Asian-inspired healthy snacking"
    },
    
    # Frozen Meal Solutions (Low-Medium Priority)
    {
        "name": "PRSL FROZEN BOWL ASIAN",
        "description": "Savory frozen Asian-inspired bowl with teriyaki and vegetables",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Convenience-focused global cuisine"
    },
    {
        "name": "PRSL FROZEN BOWL MED",
        "description": "Mediterranean frozen bowl with quinoa and roasted vegetables",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Healthy convenience meal option"
    },
    {
        "name": "PRSL FROZEN PIZZA ART",
        "description": "Artisanal frozen pizza with wood-fired crust and fresh mozzarella",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Premium frozen meal category"
    },
    {
        "name": "PRSL FROZEN SOUP PK",
        "description": "Gourmet frozen soup variety pack with bone broth",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Convenient meal prep solution"
    },
    
    # Additional Ultra-Specific Items
    {
        "name": "PRSL KOREAN KIMCHI KOMBUCHA BBQ BF BWL",
        "description": "Spicy Korean kimchi kombucha BBQ beef bowl with fermented vegetables",
        "category": "Global Fusion",
        "priority": "High",
        "reason": "Ultra-specific fusion cuisine with trending ingredients"
    },
    {
        "name": "PRSL TRUFFLE MUSHROOM WILD RICE RISOTTO",
        "description": "Creamy truffle mushroom wild rice risotto with porcini and shiitake",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Luxury comfort food with premium ingredients"
    },
    {
        "name": "PRSL SMOKED PAPRIKA QUINOA CRUNCH MIX",
        "description": "Crunchy smoked paprika quinoa crunch mix with roasted chickpeas",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Superfood snacking with bold flavors"
    },
    {
        "name": "PRSL CARDAMOM ROSE WATER TURKISH DELIGHT",
        "description": "Fragrant cardamom rose water Turkish delight with pistachios",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Exotic Middle Eastern confectionery"
    },
    {
        "name": "PRSL MISO CARAMEL SEA SALT DARK CHOC BAR",
        "description": "Rich miso caramel sea salt dark chocolate bar with umami notes",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Sophisticated flavor combinations"
    },
    {
        "name": "PRSL FERMENTED GARLIC HONEY HOT SAUCE",
        "description": "Tangy fermented garlic honey hot sauce with ghost peppers",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Artisanal condiments with complex flavors"
    },
    {
        "name": "PRSL BLACK GARLIC BALSAMIC VINEGAR GLAZE",
        "description": "Aged black garlic balsamic vinegar glaze with fig reduction",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Gourmet cooking ingredients for food enthusiasts"
    },
    {
        "name": "PRSL SMOKED SEA SALT CARAMEL POPCORN",
        "description": "Artisanal smoked sea salt caramel popcorn with bourbon vanilla",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Elevated movie theater snack experience"
    },
    {
        "name": "PRSL PICKLED WATERMELON RIND RELISH",
        "description": "Sweet-tart pickled watermelon rind relish with jalapeños",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Zero-waste cooking with unexpected ingredients"
    },
    {
        "name": "PRSL CHARRED CORN ELOTE STREET FOOD MIX",
        "description": "Spicy charred corn elote street food mix with cotija cheese",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Authentic Mexican street food flavors"
    }
]

def get_random_recommendation():
    """Get a random recommendation that's different from the last one"""
    global last_recommended_item
    
    # Filter out the last recommended item
    available_items = [item for item in RECOMMENDED_ITEMS if item != last_recommended_item]
    
    # If we only have one item, reset the filter
    if not available_items:
        available_items = RECOMMENDED_ITEMS
        last_recommended_item = None
    
    # Select random item
    selected_item = random.choice(available_items)
    last_recommended_item = selected_item
    
    return selected_item

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint to get a random recommendation"""
    try:
        recommendation = get_random_recommendation()
        return jsonify({
            'success': True,
            'recommendation': recommendation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stats')
def stats():
    """Get statistics about recommendations"""
    categories = {}
    priorities = {}
    
    for item in RECOMMENDED_ITEMS:
        cat = item['category']
        pri = item['priority']
        
        categories[cat] = categories.get(cat, 0) + 1
        priorities[pri] = priorities.get(pri, 0) + 1
    
    return jsonify({
        'total_items': len(RECOMMENDED_ITEMS),
        'categories': categories,
        'priorities': priorities
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
