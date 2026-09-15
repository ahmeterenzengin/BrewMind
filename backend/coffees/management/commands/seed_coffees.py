"""
Management command to seed the database with coffee data and generate embeddings.
Usage: python manage.py seed_coffees
"""
from django.core.management.base import BaseCommand
from coffees.models import Coffee
from rag.embeddings import get_embedding, get_coffee_text

COFFEES = [
    {
        "name": "Espresso",
        "description": "A concentrated coffee shot with rich crema. Bold, intense, and deeply aromatic. The foundation of most coffee drinks.",
        "category": "hot",
        "milk_type": "none",
        "sweetness": "none",
        "intensity": "strong",
        "ingredients": ["espresso"],
        "price": 35.00, "image_url": "espresso.jpg",
    },
    {
        "name": "Americano",
        "description": "Espresso diluted with hot water creating a smooth, full-bodied black coffee. Clean and refreshing with a mild bitterness.",
        "category": "hot",
        "milk_type": "none",
        "sweetness": "none",
        "intensity": "medium",
        "ingredients": ["espresso", "hot water"],
        "price": 40.00, "image_url": "americano.jpg",
    },
    {
        "name": "Latte",
        "description": "A creamy and smooth coffee made with espresso and steamed whole milk. Mild coffee flavor with velvety texture. Perfect for those who prefer a gentle coffee experience.",
        "category": "hot",
        "milk_type": "whole",
        "sweetness": "low",
        "intensity": "light",
        "ingredients": ["espresso", "steamed whole milk", "milk foam"],
        "price": 55.00, "image_url": "latte.jpg",
    },
    {
        "name": "Cappuccino",
        "description": "Equal parts espresso, steamed milk, and rich milk foam. Balanced between bold coffee and creamy texture. A classic Italian morning staple.",
        "category": "hot",
        "milk_type": "whole",
        "sweetness": "low",
        "intensity": "medium",
        "ingredients": ["espresso", "steamed milk", "milk foam"],
        "price": 55.00, "image_url": "cappuccino.jpg",
    },
    {
        "name": "Mocha",
        "description": "A delightful combination of espresso, rich chocolate sauce, and steamed milk topped with whipped cream. Sweet, chocolatey, and indulgent.",
        "category": "hot",
        "milk_type": "whole",
        "sweetness": "high",
        "intensity": "medium",
        "ingredients": ["espresso", "chocolate sauce", "steamed milk", "whipped cream"],
        "price": 65.00, "image_url": "mocha.jpg",
    },
    {
        "name": "Flat White",
        "description": "A bold espresso-forward drink with a thin layer of velvety microfoam milk. Stronger than a latte with a silkier texture. Australian café favorite.",
        "category": "hot",
        "milk_type": "whole",
        "sweetness": "none",
        "intensity": "strong",
        "ingredients": ["double espresso", "steamed whole milk"],
        "price": 60.00, "image_url": "flat_white.jpg",
    },
    {
        "name": "Turkish Coffee",
        "description": "Finely ground coffee simmered in a cezve pot, served unfiltered with rich sediment. Thick, aromatic, and intensely flavorful. A centuries-old tradition.",
        "category": "hot",
        "milk_type": "none",
        "sweetness": "medium",
        "intensity": "strong",
        "ingredients": ["very finely ground coffee", "water"],
        "price": 40.00, "image_url": "turkish_coffee.jpg",
    },
    {
        "name": "Caramel Macchiato",
        "description": "Layers of vanilla syrup, steamed milk, espresso, and caramel drizzle. Sweet, rich, and visually stunning. A treat for caramel lovers.",
        "category": "hot",
        "milk_type": "whole",
        "sweetness": "high",
        "intensity": "medium",
        "ingredients": ["espresso", "vanilla syrup", "steamed milk", "caramel sauce"],
        "price": 70.00, "image_url": "caramel_macchiato.jpg",
    },
    {
        "name": "Cortado",
        "description": "Equal parts espresso and warm milk to reduce acidity. Small, balanced, and sophisticated. Popular in Spain and Latin America.",
        "category": "hot",
        "milk_type": "whole",
        "sweetness": "none",
        "intensity": "strong",
        "ingredients": ["double espresso", "warm whole milk"],
        "price": 50.00,
        "image_url": "cortado.jpg",
    },
    {
        "name": "Irish Coffee",
        "description": "Hot coffee with Irish whiskey, brown sugar, and a layer of thick cream. Warming, rich, and indulgent. Perfect for cold evenings.",
        "category": "hot",
        "milk_type": "cream",
        "sweetness": "medium",
        "intensity": "medium",
        "ingredients": ["coffee", "irish whiskey", "brown sugar", "heavy cream"],
        "price": 85.00,
        "image_url": "irish_coffee.jpg",
    },
    {
        "name": "Matcha Latte",
        "description": "Ceremonial grade matcha whisked with oat milk and a touch of honey. Earthy, creamy, and naturally energizing. A Japanese-inspired wellness drink.",
        "category": "hot",
        "milk_type": "oat",
        "sweetness": "medium",
        "intensity": "light",
        "ingredients": ["matcha powder", "oat milk", "honey"],
        "price": 65.00, "image_url": "matcha_latte.jpg",
    },
    {
        "name": "Chai Latte",
        "description": "Spiced black tea blended with steamed milk and warming spices like cinnamon, cardamom, and ginger. Cozy, aromatic, and comforting.",
        "category": "hot",
        "milk_type": "whole",
        "sweetness": "medium",
        "intensity": "light",
        "ingredients": ["black tea", "cinnamon", "cardamom", "ginger", "steamed milk"],
        "price": 60.00,
        "image_url": "chai_latte.jpg",
    },
    {
        "name": "Almond Milk Latte",
        "description": "Smooth espresso with creamy almond milk. Light, nutty, and dairy-free. A great plant-based alternative to the classic latte.",
        "category": "hot",
        "milk_type": "almond",
        "sweetness": "low",
        "intensity": "light",
        "ingredients": ["espresso", "steamed almond milk"],
        "price": 60.00,
        "image_url": "almond_milk_latte.jpg",
    },
    {
        "name": "V60 Pour Over",
        "description": "Specialty single-origin coffee brewed slowly through a V60 filter. Clean, bright, and complex with distinct fruity or floral notes depending on origin.",
        "category": "hot",
        "milk_type": "none",
        "sweetness": "none",
        "intensity": "medium",
        "ingredients": ["specialty ground coffee", "filtered water"],
        "price": 65.00,
        "image_url": "v60_pour_over.jpg",
    },
    {
        "name": "Iced Latte",
        "description": "Chilled espresso poured over ice with cold whole milk. Smooth, refreshing, and creamy. The perfect cool-down coffee on a warm day.",
        "category": "cold",
        "milk_type": "whole",
        "sweetness": "low",
        "intensity": "light",
        "ingredients": ["espresso", "cold whole milk", "ice"],
        "price": 60.00, "image_url": "iced_latte.jpg",
    },
    {
        "name": "Iced Americano",
        "description": "Espresso shots poured over ice and cold water. Crisp, bold, and refreshing without any milk. Great for hot days when you need a caffeine kick.",
        "category": "cold",
        "milk_type": "none",
        "sweetness": "none",
        "intensity": "medium",
        "ingredients": ["espresso", "cold water", "ice"],
        "price": 45.00,
        "image_url": "iced_americano.jpg",
    },
    {
        "name": "Cold Brew",
        "description": "Coffee steeped in cold water for 12-24 hours resulting in an ultra-smooth, low-acid concentrate. Bold, rich, and naturally sweet. No heat involved.",
        "category": "cold",
        "milk_type": "none",
        "sweetness": "none",
        "intensity": "strong",
        "ingredients": ["coarse ground coffee", "cold water"],
        "price": 65.00, "image_url": "cold_brew.jpg",
    },
    {
        "name": "Iced Mocha",
        "description": "Espresso, chocolate sauce, and cold milk over ice, topped with whipped cream. Sweet, chocolatey, and refreshing. A chilled dessert in a cup.",
        "category": "cold",
        "milk_type": "whole",
        "sweetness": "high",
        "intensity": "medium",
        "ingredients": ["espresso", "chocolate sauce", "cold milk", "ice", "whipped cream"],
        "price": 70.00,
        "image_url": "iced_mocha.jpg",
    },
    {
        "name": "Affogato",
        "description": "A scoop of vanilla gelato drowned in a hot espresso shot. The contrast of hot and cold, bitter and sweet makes it a unique Italian dessert-coffee.",
        "category": "cold",
        "milk_type": "none",
        "sweetness": "high",
        "intensity": "strong",
        "ingredients": ["espresso", "vanilla gelato"],
        "price": 75.00, "image_url": "affogato.jpg",
    },
    {
        "name": "Frappuccino",
        "description": "A blended iced coffee drink with milk, ice, flavored syrup, and whipped cream. Sweet, thick, and indulgent. The ultimate summer coffee treat.",
        "category": "frappe",
        "milk_type": "whole",
        "sweetness": "high",
        "intensity": "light",
        "ingredients": ["espresso", "milk", "ice", "vanilla syrup", "whipped cream"],
        "price": 75.00, "image_url": "frappuccino.jpg",
    },
]


class Command(BaseCommand):
    help = "Seed the database with coffee data and generate embeddings"

    def handle(self, *args, **options):
        self.stdout.write("Seeding coffees...")

        created_count = 0
        updated_count = 0

        for data in COFFEES:
            coffee, created = Coffee.objects.update_or_create(
                name=data["name"],
                defaults=data,
            )

            # Generate and save embedding
            self.stdout.write(f"  Generating embedding for {coffee.name}...")
            text = get_coffee_text(coffee)
            coffee.embedding = get_embedding(text)
            coffee.save()

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Created: {created_count}, Updated: {updated_count} coffees."
            )
        )
