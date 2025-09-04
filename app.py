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
        "description": "Plant-based ground beef alternative",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Captures growing plant-based market with 15-20% annual growth"
    },
    {
        "name": "PRSL PLT CHK STRIPS GNG",
        "description": "Plant-based chicken strips",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Perfect alternative to your top-selling chicken products"
    },
    {
        "name": "PRSL PLT SSG ITALIAN PK",
        "description": "Plant-based Italian sausage",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Expands your sausage line with sustainable option"
    },
    {
        "name": "PRSL PLT CHS SHRED MOZZ",
        "description": "Plant-based mozzarella shreds",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Complements your strong cheese category"
    },
    {
        "name": "PRSL PLT YGT VAN PROB",
        "description": "Plant-based probiotic yogurt",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Combines plant-based trend with functional foods"
    },
    {
        "name": "PRSL PLT ICE CRM CHOC",
        "description": "Plant-based chocolate ice cream",
        "category": "Plant-Based",
        "priority": "High",
        "reason": "Premium frozen dessert for health-conscious consumers"
    },
    
    # Functional Foods & Health Trends (High Priority)
    {
        "name": "PRSL KOMBUCHA GINGER TURM",
        "description": "Kombucha with ginger and turmeric",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Gut health trend with 25% annual growth"
    },
    {
        "name": "PRSL KIMCHI TRAD KOREAN",
        "description": "Traditional Korean kimchi",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Fermented foods for digestive health"
    },
    {
        "name": "PRSL PROB YGT MIX BERRY",
        "description": "Probiotic yogurt with mixed berries",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Health-focused consumers seeking functional benefits"
    },
    {
        "name": "PRSL ADAPT TEA ASHWAGAND",
        "description": "Adaptogen tea with ashwagandha",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Stress relief and wellness positioning"
    },
    {
        "name": "PRSL SUPERFRT SMOOTHIE PK",
        "description": "Superfruit smoothie packs",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Convenient superfood nutrition"
    },
    {
        "name": "PRSL GUT HLTH GRANOLA",
        "description": "Gut health granola with prebiotics",
        "category": "Functional Foods",
        "priority": "High",
        "reason": "Breakfast category with health benefits"
    },
    
    # Global Fusion & Ethnic Flavors (Medium Priority)
    {
        "name": "PRSL UBE SWT POTATO CHIPS",
        "description": "Filipino ube sweet potato chips",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "International flavors attracting diverse demographics"
    },
    {
        "name": "PRSL YUZU CITRUS DRSNG",
        "description": "Japanese yuzu citrus dressing",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Asian cuisine trend in mainstream markets"
    },
    {
        "name": "PRSL SUYA SPICE BLEND",
        "description": "West African suya spice blend",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "African flavors gaining popularity"
    },
    {
        "name": "PRSL TACO SEASONING PK",
        "description": "Mexican taco seasoning packet",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Hispanic market expansion"
    },
    {
        "name": "PRSL CURRY PASTE THAI",
        "description": "Thai curry paste",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Southeast Asian cuisine popularity"
    },
    {
        "name": "PRSL HARISSA SPICE MIX",
        "description": "North African harissa spice mix",
        "category": "Global Fusion",
        "priority": "Medium",
        "reason": "Middle Eastern and North African flavors"
    },
    
    # Sustainable & Zero-Waste Products (Medium Priority)
    {
        "name": "PRSL VEG SCRAP CHIPS MIX",
        "description": "Vegetable scrap chips variety pack",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Zero-waste cooking trend and sustainability"
    },
    {
        "name": "PRSL UPCLD BREAD CRUMBS",
        "description": "Upcycled bread crumbs",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Food waste reduction and circular economy"
    },
    {
        "name": "PRSL REGEN BEEF GRD",
        "description": "Regenerative agriculture beef",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Environmental consciousness in meat category"
    },
    {
        "name": "PRSL COMPOST PKG CHIPS",
        "description": "Compostable packaging chips",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Eco-friendly packaging innovation"
    },
    {
        "name": "PRSL ZERO WASTE SOUP",
        "description": "Zero-waste vegetable soup",
        "category": "Sustainable",
        "priority": "Medium",
        "reason": "Sustainability-focused prepared foods"
    },
    
    # Premium Snacks & Convenience (Medium Priority)
    {
        "name": "PRSL ARTISAN CRACKER MIX",
        "description": "Artisan cracker variety mix",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Premium snacking market expansion"
    },
    {
        "name": "PRSL GOURMET NUT BLEND",
        "description": "Gourmet mixed nuts blend",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "High-margin snack category"
    },
    {
        "name": "PRSL PROTEIN BALLS 6CT",
        "description": "Protein energy balls 6-count",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Health-focused convenience snacks"
    },
    {
        "name": "PRSL DARK CHOC TRUFFLES",
        "description": "Dark chocolate truffles",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Premium dessert and gifting category"
    },
    {
        "name": "PRSL SEAWEED SNACK MIX",
        "description": "Seaweed snack variety mix",
        "category": "Premium Snacks",
        "priority": "Medium",
        "reason": "Asian-inspired healthy snacking"
    },
    
    # Frozen Meal Solutions (Low-Medium Priority)
    {
        "name": "PRSL FROZEN BOWL ASIAN",
        "description": "Frozen Asian-inspired bowl",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Convenience-focused global cuisine"
    },
    {
        "name": "PRSL FROZEN BOWL MED",
        "description": "Frozen Mediterranean bowl",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Healthy convenience meal option"
    },
    {
        "name": "PRSL FROZEN PIZZA ART",
        "description": "Frozen artisan pizza",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Premium frozen meal category"
    },
    {
        "name": "PRSL FROZEN SOUP PK",
        "description": "Frozen soup variety pack",
        "category": "Frozen Meals",
        "priority": "Low-Medium",
        "reason": "Convenient meal prep solution"
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
