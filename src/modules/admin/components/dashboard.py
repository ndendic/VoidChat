from typing import Type

from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *
from monsterui import *
from monsterui.franken import *
from monsterui.franken import Grid as Grd

def InfoCard(title, value, change):
    return Div(Card(Div(H3(value), P(change, cls=TextFont.muted_sm)), header=H4(title)))


rev = InfoCard("Total Revenue", "$45,231.89", "+20.1% from last month")
sub = InfoCard("Subscriptions", "+2350", "+180.1% from last month")
sal = InfoCard("Sales", "+12,234", "+19% from last month")
act = InfoCard("Active Now", "+573", "+201 since last hour")

top_info_row = Grd(rev, sub, sal, act, cols_min=1, cols_max=4)

def AvatarItem(name, email, amount):
    return Div(cls="flex items-center")(
        DiceBearAvatar(name, 9, 9),
        Div(cls="ml-4 space-y-1")(
            P(name, cls=TextFont.bold_sm), P(email, cls=TextFont.muted_sm)
        ),
        Div(amount, cls="ml-auto font-medium"),
    )


recent_sales = Card(
    Div(cls="space-y-8")(
        *[
            AvatarItem(n, e, d)
            for (n, e, d) in (
                ("Olivia Martin", "olivia.martin@email.com", "+$1,999.00"),
                ("Jackson Lee", "jackson.lee@email.com", "+$39.00"),
                ("Isabella Nguyen", "isabella.nguyen@email.com", "+$299.00"),
                ("William Kim", "will@email.com", "+$99.00"),
                ("Sofia Davis", "sofia.davis@email.com", "+$39.00"),
            )
        ]
    ),
    header=Div(
        H3("Recent Sales"), P("You made 265 sales this month.", cls=TextFont.muted_sm)
    ),
    cls="col-span-3",
)


teams = [["Alicia Koch"], ["Acme Inc", "Monster Inc."], ["Create a Team"]]

opt_hdrs = ["Personal", "Team", ""]

team_dropdown = UkSelect(
    Optgroup(label="Personal Account")(Option(A("Alicia Koch"))),
    Optgroup(label="Teams")(Option(A("Acme Inc")), Option(A("Monster Inc."))),
    Option(A("Create a Team")),
)

rt = APIRouter()


def dashboard_page(request):
    return Div(cls="space-y-4")(
        H2("Dashboard"),
        TabContainer(
            Li(A("Overview", cls="uk-active")),
            Li(A("Analytics")),
            Li(A("Reports")),
            Li(A("Notifications")),
            uk_switcher="connect: #component-nav; animation: uk-animation-fade",
            alt=True,
        ),
        Ul(id="component-nav", cls="uk-switcher")(
            Li(
                top_info_row,
                Grd(
                    Card(H3("Overview to show here..."), cls="col-span-4"),
                    recent_sales,
                    gap=4,
                    cols=7,
                ),
                cls="space-y-4",
            ),
            Li(
                top_info_row,
                Grd(
                    Card(H3("Analytics to show here..."), cls="col-span-4"),
                    recent_sales,
                    gap=4,
                    cols=7,
                ),
                cls="space-y-4",
            ),
        ),
    )
