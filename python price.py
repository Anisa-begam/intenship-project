price = float(input("Enter product price: "))

discount = float(input("Enter discount percentage: "))

gst = float(input("Enter GST percentage: "))

discount_amount = (price * discount) / 100
price_after_discount = price - discount_amount

gst_amount = (price_after_discount * gst) / 100
final_price = price_after_discount + gst_amount

print("Price after discount:", price_after_discount)
print("GST amount:", gst_amount)
print("Final price:", final_price)