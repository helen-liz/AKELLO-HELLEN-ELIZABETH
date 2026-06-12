"""
E-Commerce System with Price Calculation and Login Authentication
Features:
- User authentication with role-based access control
- Price calculation with coupon codes and tax rates
- Nested conditions for discount and tax scenarios
- Three user types: Admin, Customer, Cashier
"""

import json
from datetime import datetime

# ============================================================================
# USER DATABASE AND CREDENTIALS
# ============================================================================

USER_DATABASE = {
    # Admin users
    "admin1": {
        "password": "admin123",
        "role": "admin",
        "name": "Administrator"
    },
    # Customer users
    "customer1": {
        "password": "cust123",
        "role": "customer",
        "name": "John Doe"
    },
    "customer2": {
        "password": "cust456",
        "role": "customer",
        "name": "Jane Smith"
    },
    # Cashier users
    "cashier1": {
        "password": "cash123",
        "role": "cashier",
        "name": "Bob Johnson"
    },
    "cashier2": {
        "password": "cash456",
        "role": "cashier",
        "name": "Alice Williams"
    }
}

# Valid coupon codes and their discount percentages
COUPON_CODES = {
    "SAVE10": 10,      # 10% discount
    "SAVE15": 15,      # 15% discount
    "SUMMER20": 20,    # 20% discount
    "WELCOME5": 5,     # 5% discount
    "BULK25": 25       # 25% discount
}

# Tax rates by location
TAX_RATES = {
    "NY": 0.08,        # 8% tax
    "CA": 0.0725,      # 7.25% tax
    "TX": 0.0625,      # 6.25% tax
    "FL": 0.06,        # 6% tax
    "WA": 0.065,       # 6.5% tax
    "default": 0.07    # 7% default tax
}

# ============================================================================
# AUTHENTICATION SYSTEM
# ============================================================================

class AuthenticationSystem:
    """Handles user login and authentication"""
    
    def __init__(self):
        self.current_user = None
        self.login_attempts = {}
    
    def login(self, username, password):
        """
        Authenticate user with username and password
        Returns: (success: bool, message: str, user_info: dict)
        """
        if username not in USER_DATABASE:
            message = f" User '{username}' not found in the system."
            return False, message, None
        
        user = USER_DATABASE[username]
        
        if user["password"] != password:
            message = " Incorrect password. Access denied."
            return False, message, None
        
        self.current_user = {
            "username": username,
            "role": user["role"],
            "name": user["name"]
        }
        
        message = f" Login successful! Welcome {user['name']} ({user['role'].upper()})"
        return True, message, self.current_user
    
    def logout(self):
        """Logout the current user"""
        if self.current_user:
            username = self.current_user["username"]
            self.current_user = None
            return f" Logged out successfully. Goodbye {username}!"
        return "⚠️  No user is currently logged in."
    
    def is_logged_in(self):
        """Check if a user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get information about the current logged-in user"""
        return self.current_user

# ============================================================================
# PRICE CALCULATION SYSTEM
# ============================================================================

class PriceCalculator:
    """Handles price calculations with discounts, coupons, and tax"""
    
    @staticmethod
    def validate_coupon(coupon_code):
        """
        Validate if coupon code exists and return discount percentage
        Uses nested conditions to handle different scenarios
        """
        if coupon_code is None or coupon_code.strip() == "":
            return True, 0, "No coupon code applied"
        
        coupon_code = coupon_code.upper().strip()
        
        # Nested condition: Check if coupon exists
        if coupon_code in COUPON_CODES:
            discount_percent = COUPON_CODES[coupon_code]
            return True, discount_percent, f"Valid coupon code '{coupon_code}' applied: {discount_percent}% discount"
        else:
            return False, 0, f"Invalid coupon code '{coupon_code}'. No discount applied."
    
    @staticmethod
    def calculate_subtotal_discount(subtotal):
        """
        Apply discount based on subtotal amount using nested conditions
        Discount tiers:
        - $0-$50: 0% discount
        - $50-$100: 2% discount
        - $100-$500: 5% discount
        - $500+: 10% discount
        """
        if subtotal < 50:
            discount_percent = 0
            tier = "No bulk discount"
        elif subtotal < 100:
            discount_percent = 2
            tier = "Tier 1 (2% bulk discount)"
        elif subtotal < 500:
            discount_percent = 5
            tier = "Tier 2 (5% bulk discount)"
        else:
            discount_percent = 10
            tier = "Tier 3 (10% bulk discount)"
        
        discount_amount = (subtotal * discount_percent) / 100
        return discount_amount, discount_percent, tier
    
    @staticmethod
    def get_tax_rate(location):
        """
        Get tax rate based on location using nested conditions
        """
        location = location.upper().strip()
        
        if location in TAX_RATES:
            tax_rate = TAX_RATES[location]
            location_name = location
        else:
            tax_rate = TAX_RATES["default"]
            location_name = "Default (Unknown Location)"
        
        return tax_rate, location_name
    
    @staticmethod
    def calculate_final_price(subtotal, coupon_code=None, location="default"):
        """
        Calculate final price with all discounts and tax applied
        Uses nested conditions for different scenarios
        
        Returns: dict with breakdown of all calculations
        """
        result = {
            "subtotal": subtotal,
            "coupon_code": coupon_code if coupon_code else "None",
            "location": location,
            "breakdown": {}
        }
        
        # Validate subtotal
        if subtotal <= 0:
            result["error"] = " Subtotal must be greater than 0"
            return result
        
        # Step 1: Validate coupon code
        coupon_valid, coupon_discount, coupon_msg = PriceCalculator.validate_coupon(coupon_code)
        result["breakdown"]["coupon_validation"] = {
            "message": coupon_msg,
            "discount_percent": coupon_discount
        }
        
        # Nested condition: Calculate coupon discount
        if coupon_valid and coupon_discount > 0:
            coupon_discount_amount = (subtotal * coupon_discount) / 100
        else:
            coupon_discount_amount = 0
        
        result["breakdown"]["coupon_discount"] = coupon_discount_amount
        
        # Step 2: Calculate subtotal-based bulk discount
        bulk_discount_amount, bulk_discount_percent, bulk_tier = PriceCalculator.calculate_subtotal_discount(subtotal)
        result["breakdown"]["bulk_discount"] = {
            "amount": bulk_discount_amount,
            "percent": bulk_discount_percent,
            "tier": bulk_tier
        }
        
        # Step 3: Calculate subtotal after discounts
        # Nested condition: Apply both discounts
        total_discount = coupon_discount_amount + bulk_discount_amount
        subtotal_after_discount = subtotal - total_discount
        
        # Ensure subtotal after discount doesn't go below 0
        if subtotal_after_discount < 0:
            subtotal_after_discount = 0
        
        result["breakdown"]["subtotal_after_discount"] = subtotal_after_discount
        result["breakdown"]["total_discount"] = total_discount
        
        # Step 4: Get tax rate based on location
        tax_rate, location_name = PriceCalculator.get_tax_rate(location)
        result["breakdown"]["tax_info"] = {
            "location": location_name,
            "tax_rate_percent": tax_rate * 100
        }
        
        # Step 5: Calculate tax on discounted subtotal
        tax_amount = subtotal_after_discount * tax_rate
        result["breakdown"]["tax_amount"] = tax_amount
        
        # Step 6: Calculate final price
        final_price = subtotal_after_discount + tax_amount
        result["final_price"] = round(final_price, 2)
        
        # Add summary
        result["summary"] = {
            "Original Subtotal": f"${subtotal:.2f}",
            "Coupon Discount": f"-${coupon_discount_amount:.2f}",
            "Bulk Discount": f"-${bulk_discount_amount:.2f}",
            "Total Discounts": f"-${total_discount:.2f}",
            "Subtotal After Discount": f"${subtotal_after_discount:.2f}",
            f"Tax ({location_name})": f"${tax_amount:.2f}",
            "FINAL PRICE": f"${final_price:.2f}"
        }
        
        return result

# ============================================================================
# ROLE-BASED ACCESS CONTROL
# ============================================================================

class AccessControl:
    """Manages role-based access to features"""
    
    PERMISSIONS = {
        "admin": {
            "view_products": True,
            "purchase": True,
            "process_payment": True,
            "view_reports": True,
            "manage_users": True,
            "manage_inventory": True,
            "view_sales_history": True,
            "manage_coupons": True,
            "generate_invoice": True
        },
        "customer": {
            "view_products": True,
            "purchase": True,
            "process_payment": True,
            "view_reports": False,
            "manage_users": False,
            "manage_inventory": False,
            "view_sales_history": True,  # Only own history
            "manage_coupons": False,
            "generate_invoice": True
        },
        "cashier": {
            "view_products": True,
            "purchase": False,
            "process_payment": True,
            "view_reports": False,
            "manage_users": False,
            "manage_inventory": False,
            "view_sales_history": False,
            "manage_coupons": False,
            "generate_invoice": True
        }
    }
    
    @staticmethod
    def check_permission(user_role, feature):
        """
        Check if a user role has permission to access a feature
        """
        if user_role not in AccessControl.PERMISSIONS:
            return False
        
        return AccessControl.PERMISSIONS[user_role].get(feature, False)
    
    @staticmethod
    def get_accessible_features(user_role):
        """Get all accessible features for a user role"""
        if user_role not in AccessControl.PERMISSIONS:
            return {}
        
        return AccessControl.PERMISSIONS[user_role]

# ============================================================================
# MAIN E-COMMERCE SYSTEM
# ============================================================================

class ECommerceSystem:
    """Main e-commerce platform"""
    
    def __init__(self):
        self.auth = AuthenticationSystem()
        self.price_calc = PriceCalculator()
        self.access_control = AccessControl()
        self.transactions = []
    
    def display_welcome_menu(self):
        """Display welcome menu"""
        print("\n" + "=" * 70)
        print("          🛍️  WELCOME TO E-COMMERCE SYSTEM 🛍️")
        print("=" * 70)
        print("\nPlease choose an option:")
        print("  1. Login to your account")
        print("  2. Exit")
        print("=" * 70)
    
    def display_main_menu(self, user):
        """Display main menu based on user role"""
        print("\n" + "=" * 70)
        print(f"  Welcome {user['name']} | Role: {user['role'].upper()}")
        print("=" * 70)
        
        if user["role"] == "admin":
            print("\n  Admin Dashboard Options:")
            print("  1. Calculate Product Price")
            print("  2. View All Users")
            print("  3. View Transaction History")
            print("  4. Manage Coupons")
            print("  5. View System Statistics")
        
        elif user["role"] == "customer":
            print("\n  Customer Dashboard Options:")
            print("  1. Calculate Product Price")
            print("  2. View Your Transaction History")
            print("  3. View Account Details")
        
        elif user["role"] == "cashier":
            print("\n  Cashier Dashboard Options:")
            print("  1. Calculate Product Price")
            print("  2. Generate Invoice")
            print("  3. View Transaction Log")
        
        print("  0. Logout")
        print("=" * 70)
    
    def calculate_price_interactive(self):
        """Interactive price calculation"""
        print("\n" + "-" * 70)
        print("              📊 PRICE CALCULATION")
        print("-" * 70)
        
        try:
            subtotal = float(input("Enter product subtotal ($): "))
            coupon = input("Enter coupon code (leave blank for none): ")
            location = input("Enter location (NY/CA/TX/FL/WA): ") or "default"
            
            result = self.price_calc.calculate_final_price(subtotal, coupon, location)
            
            if "error" in result:
                print(f"\n{result['error']}")
                return
            
            # Display results
            print("\n" + "=" * 70)
            print("                   💰 PRICE BREAKDOWN 💰")
            print("=" * 70)
            
            for key, value in result["summary"].items():
                print(f"  {key:<30} {value:>15}")
            
            print("=" * 70)
            
            # Store transaction
            self.transactions.append({
                "user": self.auth.current_user["username"],
                "role": self.auth.current_user["role"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subtotal": subtotal,
                "coupon": coupon or "None",
                "location": location,
                "final_price": result["final_price"]
            })
            
            print(f"\n✅ Transaction recorded successfully!")
            
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def view_transaction_history(self):
        """View transaction history"""
        print("\n" + "-" * 70)
        print("              📋 TRANSACTION HISTORY")
        print("-" * 70)
        
        user_transactions = [t for t in self.transactions 
                            if t["user"] == self.auth.current_user["username"]]
        
        if not user_transactions:
            print("No transactions found.")
            return
        
        print(f"\n{'#':<3} {'Date/Time':<20} {'Subtotal':<12} {'Final Price':<12} {'Coupon':<15}")
        print("-" * 70)
        
        for idx, trans in enumerate(user_transactions, 1):
            print(f"{idx:<3} {trans['timestamp']:<20} ${trans['subtotal']:<11.2f} "
                  f"${trans['final_price']:<11.2f} {trans['coupon']:<15}")
    
    def display_coupon_menu(self):
        """Display available coupons"""
        print("\n" + "-" * 70)
        print("              🎟️  AVAILABLE COUPONS 🎟️")
        print("-" * 70)
        print(f"\n{'Coupon Code':<20} {'Discount':<15} {'Description':<20}")
        print("-" * 70)
        
        coupon_descriptions = {
            "SAVE10": "General Discount",
            "SAVE15": "Member Discount",
            "SUMMER20": "Summer Special",
            "WELCOME5": "First-Time Buyer",
            "BULK25": "Bulk Purchase"
        }
        
        for code, discount in COUPON_CODES.items():
            desc = coupon_descriptions.get(code, "Special Offer")
            print(f"{code:<20} {discount}%{'':<10} {desc:<20}")
    
    def view_user_permissions(self):
        """View available features for current user"""
        print("\n" + "-" * 70)
        print("              🔐 YOUR PERMISSIONS")
        print("-" * 70)
        
        role = self.auth.current_user["role"]
        features = self.access_control.get_accessible_features(role)
        
        print(f"\nAvailable features for {role.upper()}:")
        for feature, allowed in features.items():
            status = "✅ Allowed" if allowed else "❌ Restricted"
            print(f"  {feature:<25} {status}")
    
    def run(self):
        """Main application loop"""
        while True:
            if not self.auth.is_logged_in():
                self.display_welcome_menu()
                choice = input("\nEnter your choice (1-2): ").strip()
                
                if choice == "1":
                    print("\n" + "-" * 70)
                    print("              🔐 LOGIN")
                    print("-" * 70)
                    username = input("Username: ").strip()
                    password = input("Password: ").strip()
                    
                    success, message, user_info = self.auth.login(username, password)
                    print(f"\n{message}")
                    
                    if not success:
                        input("\nPress Enter to continue...")
                
                elif choice == "2":
                    print("\n👋 Thank you for using E-Commerce System. Goodbye!")
                    break
                
                else:
                    print(" Invalid choice. Please try again.")
            
            else:
                user = self.auth.get_current_user()
                self.display_main_menu(user)
                choice = input("\nEnter your choice: ").strip()
                
                if choice == "0":
                    print(f"\n{self.auth.logout()}")
                    input("Press Enter to continue...")
                
                elif choice == "1":
                    # Check permission
                    if not self.access_control.check_permission(user["role"], "purchase"):
                        print(f"\n Access Denied! Your role ({user['role']}) cannot perform this action.")
                        input("\nPress Enter to continue...")
                    else:
                        self.calculate_price_interactive()
                        input("\nPress Enter to continue...")
                
                elif choice == "2":
                    if user["role"] == "admin":
                        print("\n" + "-" * 70)
                        print("              👥 ALL USERS")
                        print("-" * 70)
                        print(f"\n{'Username':<15} {'Role':<15} {'Name':<20}")
                        print("-" * 70)
                        for username, info in USER_DATABASE.items():
                            print(f"{username:<15} {info['role']:<15} {info['name']:<20}")
                    else:
                        self.view_transaction_history()
                    input("\nPress Enter to continue...")
                
                elif choice == "3":
                    if user["role"] == "admin":
                        print("\n" + "-" * 70)
                        print("              📊 SYSTEM STATISTICS")
                        print("-" * 70)
                        print(f"Total Transactions: {len(self.transactions)}")
                        if self.transactions:
                            total_value = sum(t["final_price"] for t in self.transactions)
                            print(f"Total Revenue: ${total_value:.2f}")
                        print(f"Total Users: {len(USER_DATABASE)}")
                        print(f"Active Users by Role:")
                        for role in ["admin", "customer", "cashier"]:
                            count = sum(1 for u in USER_DATABASE.values() if u["role"] == role)
                            print(f"  - {role.capitalize()}: {count}")
                    else:
                        self.view_user_permissions()
                    input("\nPress Enter to continue...")
                
                elif choice == "4":
                    if user["role"] == "admin":
                        self.display_coupon_menu()
                    else:
                        print("❌ Access Denied! Only admins can manage coupons.")
                    input("\nPress Enter to continue...")
                
                elif choice == "5" and user["role"] == "admin":
                    self.view_transaction_history()
                    input("\nPress Enter to continue...")
                
                else:
                    print("Invalid choice. Please try again.")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    system = ECommerceSystem()
    system.run()
