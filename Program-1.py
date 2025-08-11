customer_name = input("Enter your name: ")
print(f"Welcome, {customer_name}!")
items = []
total = 0.0
while True:
    item_name = input("\nEnter item name (or 'q' to quit): ").strip()
    if item_name.lower() == 'q':
        break
    try:
        price = float(input("Enter item price: ₹"))
        if price < 0:
            print("❌ Price cannot be negative!")
            continue
        items.append((item_name, price))
        total += price
        print(f"✅ Added {item_name} (₹{price:.2f}) | Total: ₹{total:.2f}")
    except ValueError:
        print("❌ Invalid price! Please enter a valid number.")
tax_percent = 5
tax_amount = (total * tax_percent) / 100
final_total = total + tax_amount
discount = 0.0
if total > 1000:
    discount = 0.1 * total
    final_total -= discount
print("\n" + "=" * 40)
print(f"🛍️  BILL FOR: {customer_name}")
print("=" * 40)
for idx, (name, price) in enumerate(items, 1):
    print(f"{idx}. {name.ljust(20)} ₹{price:.2f}")
print("-" * 40)
print(f"Subtotal:      ₹{total:.2f}")
print(f"GST (5%):      ₹{tax_amount:.2f}")
if discount > 0:
    print(f"Discount (10%): -₹{discount:.2f}")
print(f"Final Total:   ₹{final_total:.2f}")
print("=" * 40)
print("Thank you for shopping with us! 🙏")
print("=" * 40)
