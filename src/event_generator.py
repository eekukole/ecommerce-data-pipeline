from faker import Faker
import json
import random
from datetime import datetime, timedelta
import os

fake = Faker()

def generate_page_view():
    """Generate a page view event"""
    categories = ['electronics', 'clothing', 'books', 'home', 'sports', 'toys']
    return {
        'event_type': 'page_view',
        'event_id': fake.uuid4(),
        'user_id': random.randint(1000, 9999),
        'session_id': fake.uuid4(),
        'timestamp': datetime.now().isoformat(),
        'page_url': f'/products/{random.choice(categories)}/{fake.uri_page()}',
        'device': random.choice(['mobile', 'desktop', 'tablet']),
        'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge'])
    }

def generate_add_to_cart():
    """Generate add to cart event"""
    return {
        'event_type': 'add_to_cart',
        'event_id': fake.uuid4(),
        'user_id': random.randint(1000, 9999),
        'session_id': fake.uuid4(),
        'timestamp': datetime.now().isoformat(),
        'product_id': random.randint(100, 999),
        'product_name': fake.catch_phrase(),
        'price': round(random.uniform(10.0, 500.0), 2),
        'quantity': random.randint(1, 3)
    }

def generate_purchase():
    """Generate a purchase transaction"""
    num_items = random.randint(1, 5)
    item_total = sum([round(random.uniform(10.0, 200.0), 2) for _ in range(num_items)])
    
    return {
        'event_type': 'purchase',
        'event_id': fake.uuid4(),
        'order_id': fake.uuid4(),
        'user_id': random.randint(1000, 9999),
        'timestamp': datetime.now().isoformat(),
        'total_amount': round(item_total, 2),
        'items_count': num_items,
        'payment_method': random.choice(['credit_card', 'paypal', 'debit_card', 'apple_pay']),
        'shipping_address': {
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip': fake.zipcode()
        }
    }

def generate_product_review():
    """Generate a product review event"""
    return {
        'event_type': 'product_review',
        'event_id': fake.uuid4(),
        'user_id': random.randint(1000, 9999),
        'product_id': random.randint(100, 999),
        'timestamp': datetime.now().isoformat(),
        'rating': random.randint(1, 5),
        'review_text': fake.sentence(nb_words=10),
        'verified_purchase': random.choice([True, False])
    }

def save_events(events, filename='events'):
    """Save events to JSON file"""
    output_dir = 'data/events'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f'{output_dir}/{filename}_{timestamp}.json'
    
    with open(filepath, 'w') as f:
        json.dump(events, f, indent=2)
    
    print(f'[SUCCESS] Saved {len(events)} events to {filepath}')
    return filepath

def main():
    """Generate sample e-commerce events"""
    print('=' * 60)
    print('E-COMMERCE EVENT GENERATOR')
    print('=' * 60)
    
    events = []
    
    # Generate different types of events
    print('Generating page view events...')
    for _ in range(100):
        events.append(generate_page_view())
    
    print('Generating add-to-cart events...')
    for _ in range(30):
        events.append(generate_add_to_cart())
    
    print('Generating purchase events...')
    for _ in range(20):
        events.append(generate_purchase())
    
    print('Generating product reviews...')
    for _ in range(15):
        events.append(generate_product_review())
    
    # Shuffle events to make them more realistic
    random.shuffle(events)
    
    # Save to file
    print('\nSaving events to file...')
    filepath = save_events(events)
    
    print('\n' + '=' * 60)
    print(f'[COMPLETE] Generated {len(events)} total events')
    print(f'Breakdown:')
    print(f'  - Page views: 100')
    print(f'  - Add to cart: 30')
    print(f'  - Purchases: 20')
    print(f'  - Reviews: 15')
    print('=' * 60)
    print(f'\nFile location: {filepath}')
    print('Ready for next step: Loading into MySQL!')

if __name__ == '__main__':
    main()