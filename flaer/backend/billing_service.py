"""
Billing and subscription management service
Integrates with Stripe for payment processing
"""
import os
import stripe
from typing import Dict, Optional
from datetime import datetime, timedelta, timezone

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy")

# Pricing configuration
PRICING_TIERS = {
    "free": {
        "price": 0,
        "stripe_price_id": None,
        "max_data_centers": 3,
        "max_users": 2,
        "api_calls_per_month": 1000,
        "features": ["basic_monitoring", "carbon_calculator"]
    },
    "starter": {
        "price": 49,
        "stripe_price_id": os.getenv("STRIPE_PRICE_STARTER", "price_starter"),
        "max_data_centers": 10,
        "max_users": 5,
        "api_calls_per_month": 10000,
        "features": ["basic_monitoring", "carbon_calculator", "forecasting", "email_alerts"]
    },
    "professional": {
        "price": 199,
        "stripe_price_id": os.getenv("STRIPE_PRICE_PRO", "price_pro"),
        "max_data_centers": 50,
        "max_users": 20,
        "api_calls_per_month": 100000,
        "features": ["all_features", "priority_support", "custom_reports", "api_access"]
    },
    "enterprise": {
        "price": "custom",
        "stripe_price_id": os.getenv("STRIPE_PRICE_ENTERPRISE", "price_enterprise"),
        "max_data_centers": 999999,
        "max_users": 999999,
        "api_calls_per_month": 999999999,
        "features": ["all_features", "dedicated_support", "sla", "white_label", "on_premise"]
    }
}


class BillingService:
    """Handle billing and subscription operations"""
    
    @staticmethod
    def get_pricing_tiers() -> Dict:
        """Get all pricing tiers"""
        return PRICING_TIERS
    
    @staticmethod
    def get_tier_limits(tier: str) -> Dict:
        """Get limits for a specific tier"""
        return PRICING_TIERS.get(tier, PRICING_TIERS["free"])
    
    @staticmethod
    def create_customer(email: str, name: str, organization_id: str) -> str:
        """Create Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={"organization_id": organization_id}
            )
            return customer.id
        except stripe.error.StripeError as e:
            print(f"Stripe error creating customer: {e}")
            return None
    
    @staticmethod
    def create_checkout_session(
        customer_id: str,
        price_id: str,
        organization_id: str,
        success_url: str,
        cancel_url: str
    ) -> Optional[Dict]:
        """Create Stripe checkout session for subscription"""
        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={'organization_id': organization_id},
                allow_promotion_codes=True,
                billing_address_collection='required'
            )
            return {
                "session_id": session.id,
                "url": session.url
            }
        except stripe.error.StripeError as e:
            print(f"Stripe error creating checkout session: {e}")
            return None
    
    @staticmethod
    def create_portal_session(customer_id: str, return_url: str) -> Optional[str]:
        """Create Stripe customer portal session"""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url
            )
            return session.url
        except stripe.error.StripeError as e:
            print(f"Stripe error creating portal session: {e}")
            return None
    
    @staticmethod
    def cancel_subscription(subscription_id: str) -> bool:
        """Cancel a subscription"""
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except stripe.error.StripeError as e:
            print(f"Stripe error cancelling subscription: {e}")
            return False
    
    @staticmethod
    def update_subscription(subscription_id: str, new_price_id: str) -> bool:
        """Update subscription to new plan"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            stripe.Subscription.modify(
                subscription_id,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': new_price_id,
                }],
                proration_behavior='create_prorations'
            )
            return True
        except stripe.error.StripeError as e:
            print(f"Stripe error updating subscription: {e}")
            return False
    
    @staticmethod
    def handle_webhook(payload: bytes, sig_header: str) -> Optional[Dict]:
        """Handle Stripe webhook events"""
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        
        if not webhook_secret:
            print("Warning: STRIPE_WEBHOOK_SECRET not set")
            return None
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError:
            print("Invalid payload")
            return None
        except stripe.error.SignatureVerificationError:
            print("Invalid signature")
            return None
        
        # Handle different event types
        event_type = event['type']
        event_data = event['data']['object']
        
        result = {
            "type": event_type,
            "organization_id": event_data.get('metadata', {}).get('organization_id'),
            "action": None
        }
        
        if event_type == 'checkout.session.completed':
            # Payment successful, activate subscription
            result["action"] = "activate_subscription"
            result["subscription_id"] = event_data.get('subscription')
            result["customer_id"] = event_data.get('customer')
            
        elif event_type == 'customer.subscription.updated':
            # Subscription updated (plan change, etc.)
            result["action"] = "update_subscription"
            result["subscription_id"] = event_data.get('id')
            result["status"] = event_data.get('status')
            
        elif event_type == 'customer.subscription.deleted':
            # Subscription cancelled
            result["action"] = "cancel_subscription"
            result["subscription_id"] = event_data.get('id')
            
        elif event_type == 'invoice.payment_failed':
            # Payment failed, suspend account
            result["action"] = "suspend_account"
            result["subscription_id"] = event_data.get('subscription')
            
        elif event_type == 'invoice.payment_succeeded':
            # Payment succeeded, ensure account is active
            result["action"] = "activate_account"
            result["subscription_id"] = event_data.get('subscription')
        
        return result
    
    @staticmethod
    def calculate_trial_end() -> datetime:
        """Calculate trial end date (14 days from now)"""
        return datetime.now(timezone.utc) + timedelta(days=14)
    
    @staticmethod
    def is_trial_expired(trial_ends_at: Optional[datetime]) -> bool:
        """Check if trial has expired"""
        if not trial_ends_at:
            return False
        return datetime.now(timezone.utc) > trial_ends_at


# Singleton instance
billing_service = BillingService()

# Made with Bob
