import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def clean_text(text):
    """Clean text by removing commas, trimming whitespace, and removing dollar signs"""
    if pd.isna(text):
        return ""
    return str(text).replace(',', '').replace('$', '').strip()

def analyze_excel_file(file_path):
    """Analyze the Excel file and extract insights about items"""
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        print("=== FILE STRUCTURE ANALYSIS ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few rows:")
        print(df.head())
        
        # Clean the data based on memory about removing commas, trimming whitespace, and removing dollar signs
        for col in df.columns:
            df[col] = df[col].apply(clean_text)
        
        print("\n=== DEPARTMENT ANALYSIS ===")
        dept_col = 'FT Department'
        if dept_col in df.columns:
            dept_counts = df[dept_col].value_counts()
            print("Department distribution:")
            print(dept_counts)
        
        print("\n=== ITEM ANALYSIS ===")
        item_col = 'GTIN Description'
        if item_col in df.columns:
            items = df[item_col].dropna()
            print(f"Total unique items: {items.nunique()}")
            print(f"Total item entries: {len(items)}")
            
            # Show some sample items
            print("\nSample items:")
            for i, item in enumerate(items.head(20)):
                print(f"{i+1:2d}. {item}")
        
        print("\n=== SALES ANALYSIS ===")
        sales_col = '52 WK Scanned Retail'
        if sales_col in df.columns:
            # Convert sales to numeric, handling any non-numeric values
            sales_series = pd.to_numeric(df[sales_col], errors='coerce')
            print(f"Sales statistics:")
            print(f"  Total sales: ${sales_series.sum():,.2f}")
            print(f"  Average sales: ${sales_series.mean():,.2f}")
            print(f"  Median sales: ${sales_series.median():,.2f}")
            print(f"  Min sales: ${sales_series.min():,.2f}")
            print(f"  Max sales: ${sales_series.max():,.2f}")
        
        return df
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def analyze_item_patterns(df):
    """Analyze patterns in item names and abbreviations"""
    item_col = 'GTIN Description'
    if item_col not in df.columns:
        return
    
    print("\n=== ITEM PATTERN ANALYSIS ===")
    items = df[item_col].dropna().str.upper()
    
    # Common abbreviations and patterns
    print("Common abbreviations and patterns:")
    
    # Look for common food abbreviations
    abbreviations = {
        'PRSL': 'private selection',
        'PS': 'private selection',
        'BF': 'beef',
        'CHK': 'chicken',
        'PORK': 'pork',
        'SSG': 'sausage',
        'FISH': 'fish',
        'VEG': 'vegetable',
        'ORG': 'organic',
        'FRZ': 'frozen',
        'FRESH': 'fresh',
        'GRND': 'ground',
        'CHOP': 'chopped',
        'SLD': 'salad',
        'DRS': 'dressing',
        'SOS': 'sauce',
        'SPC': 'spice',
        'HERB': 'herb',
        'SEA': 'seasoning',
        'MIX': 'mix',
        'BLD': 'blend',
        'PKG': 'package',
        'PKT': 'packet',
        'BTL': 'bottle',
        'JAR': 'jar',
        'CAN': 'can',
        'BOX': 'box',
        'BAG': 'bag',
        'LB': 'pound',
        'OZ': 'ounce',
        'CT': 'count',
        'PK': 'pack',
        'EA': 'each',
        'ANG': 'angus',
        'SRLN': 'sirloin',
        'GRD': 'ground',
        'CLM': 'calamari',
        'POUCH': 'pouch',
        'GOLD': 'gold',
        'JUMBO': 'jumbo',
        'MINI': 'mini'
    }
    
    found_abbreviations = {}
    for item in items:
        for abbr, full in abbreviations.items():
            if abbr in item:
                if abbr not in found_abbreviations:
                    found_abbreviations[abbr] = []
                found_abbreviations[abbr].append(item)
    
    for abbr, examples in found_abbreviations.items():
        print(f"{abbr} ({abbreviations[abbr]}): {len(examples)} items")
        if len(examples) <= 5:
            print(f"  Examples: {', '.join(examples[:5])}")
        else:
            print(f"  Examples: {', '.join(examples[:3])}... (+{len(examples)-3} more)")

def categorize_items(df):
    """Categorize items by type and department"""
    item_col = 'GTIN Description'
    dept_col = 'FT Department'
    sales_col = '52 WK Scanned Retail'
    
    if item_col not in df.columns or dept_col not in df.columns:
        return
    
    print("\n=== ITEM CATEGORIZATION ===")
    
    # Create categories based on common food patterns
    categories = {
        'Meat & Protein': ['CHK', 'BEEF', 'PORK', 'SSG', 'FISH', 'TURKEY', 'HAM', 'BACON', 'MEAT', 'ANGUS', 'SRLN', 'GRND'],
        'Dairy & Eggs': ['MILK', 'CHEESE', 'EGG', 'YOGURT', 'BUTTER', 'CREAM', 'DAIRY'],
        'Produce': ['VEG', 'FRUIT', 'LETTUCE', 'TOMATO', 'ONION', 'PEPPER', 'CARROT', 'POTATO', 'CUCUMBER', 'BLUEBERRY'],
        'Pantry': ['RICE', 'PASTA', 'BEAN', 'GRAIN', 'CEREAL', 'FLOUR', 'SUGAR', 'OIL'],
        'Frozen': ['FRZ', 'FROZEN', 'ICE'],
        'Beverages': ['JUICE', 'SODA', 'WATER', 'TEA', 'COFFEE', 'DRINK'],
        'Snacks': ['CHIP', 'CRACKER', 'NUT', 'COOKIE', 'CANDY', 'SNACK'],
        'Condiments': ['SOS', 'DRS', 'SPC', 'HERB', 'SEA', 'VINEGAR', 'MUSTARD', 'KETCHUP'],
        'Bakery': ['BREAD', 'ROLL', 'BAGEL', 'MUFFIN', 'CAKE', 'PIE', 'COOKIE'],
        'Prepared Foods': ['SALAD', 'SLD', 'SOUP', 'STEW', 'CASSEROLE', 'ENTREE']
    }
    
    item_categories = {}
    for _, row in df.iterrows():
        item = str(row[item_col]).upper()
        dept = str(row[dept_col]).upper()
        sales = row.get(sales_col, 0)
        
        categorized = False
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in item:
                    if category not in item_categories:
                        item_categories[category] = []
                    item_categories[category].append({
                        'item': row[item_col],
                        'department': row[dept_col],
                        'sales': sales
                    })
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            if 'Other' not in item_categories:
                item_categories['Other'] = []
            item_categories['Other'].append({
                'item': row[item_col],
                'department': row[dept_col],
                'sales': sales
            })
    
    for category, items in item_categories.items():
        print(f"\n{category} ({len(items)} items):")
        # Show top items by sales if available
        if sales_col in df.columns:
            sorted_items = sorted(items, key=lambda x: float(x['sales']) if str(x['sales']).replace('.', '').isdigit() else 0, reverse=True)
            for item in sorted_items[:10]:  # Show top 10
                print(f"  - {item['item']} (Dept: {item['department']}, Sales: ${item['sales']})")
        else:
            for item in items[:10]:  # Show first 10
                print(f"  - {item['item']} (Dept: {item['department']})")

def analyze_departments(df):
    """Analyze department performance and item distribution"""
    dept_col = 'FT Department'
    sales_col = '52 WK Scanned Retail'
    item_col = 'GTIN Description'
    
    if dept_col not in df.columns or sales_col not in df.columns:
        return
    
    print("\n=== DEPARTMENT PERFORMANCE ANALYSIS ===")
    
    # Convert sales to numeric
    df[sales_col] = pd.to_numeric(df[sales_col], errors='coerce')
    
    # Group by department
    dept_analysis = df.groupby(dept_col).agg({
        sales_col: ['sum', 'mean', 'count'],
        item_col: 'nunique'
    }).round(2)
    
    dept_analysis.columns = ['Total_Sales', 'Avg_Sales', 'Item_Count', 'Unique_Items']
    dept_analysis = dept_analysis.sort_values('Total_Sales', ascending=False)
    
    print("Department Performance (sorted by total sales):")
    print(dept_analysis)
    
    return dept_analysis

if __name__ == "__main__":
    file_path = "PrivateSelectionItems.xlsx"
    df = analyze_excel_file(file_path)
    
    if df is not None:
        analyze_item_patterns(df)
        categorize_items(df)
        dept_analysis = analyze_departments(df)