from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *
from monsterui import *
from monsterui.franken import *
from config import Settings
from modules.shared.templates import page_template
from ..components.pricing import PricingHeader,PricingTiers,ComparisonSection

rt = APIRouter()
config = Settings()

tiers = [
        {
            "id": "524123",
            "name": "True Starter",
            "price": "Free",
            "description": "Start here if you still suck",
            "features": [
                "All core features",
                "Up to 5 team members",
                "5GB storage",
                "Basic support",
                "Community access",
            ],
            "highlight": False,
            "cta": "Buy Now",
        },
        {
            "id": "pro",
            "name": "Fake Pro",
            "price": "$0.99",
            "description": "Best for collapsing enterprise teams and businesses",
            "features": [
                "Everything in Starter",
                "Up to 20 team members",
                "20GB storage",
                "Priority support",
                "API access",
                "Advanced analytics",
            ],
            "highlight": True,
            "cta": "Get Started",
        },
        {
            "id": "enterprise",
            "name": "Fake Enterprise",
            "price": "Ultra Expensive",
            "description": "Conntact us so we can take your measure",
            "features": [
                "Everything in Fake Pro",
                "Unlimited team members",
                "Unlimited storage",
                "24/7 dedicated support",
                "Custom integrations",
                "SLA guarantee",
            ],
            "highlight": False,
            "cta": "Contact Sales",
        },
    ]



@rt("/pricing")
@page_template(title=config.app_name + " - Pricing")
def get(request):
    return Div(cls="py-24 lg:py-16")(
        PricingHeader(),
        PricingTiers(tiers),
        ComparisonSection(),
    )
