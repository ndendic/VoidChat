Objective:  Generate valid, functional, and well-styled FastHTML code using MonsterUI components.  All code should be executable and follow best practices.

Key Principles:

1.  `to_xml` Output:  Every code snippet MUST end with a `print(to_xml(<COMPONENT CODE>))` statement.  The agent's primary output is valid, styled HTML generated from FastHTML components.  This is non-negotiable.

2.  MonsterUI Focus: Leverage MonsterUI components as the primary building blocks. Use Tailwind CSS and daisyUI classes available through monsterui Themes only when styling adjustments are necessary *beyond* what MonsterUI provides. Avoid using custom or inline styles if the MonsterUI or Tailwind/daisyUI has equivalent classes.

3.  FastHTML Conventions: Follow FastHTML conventions for routing, data handling, and component composition. Refer to FastHTML documentation when in doubt.

4.  Example-Driven: Prioritize providing clear, executable examples. The more examples, the better the agent can learn and generalize.

5.  Contextual Awareness: Strive to understand the surrounding context of a component.  For example, a Button within a Form should have the appropriate `type` attribute.

6.  Correctness: Generated code *must* be valid Python and produce syntactically correct HTML when rendered by FastHTML.

7. Code should be concise and well-structured.

8. Use type annotations.

9. Use clear and self explanatory comments.

10. Provide detailed explanation of the example



# --------------------------------------------------------------------------
# I. Basic Elements and Examples
# --------------------------------------------------------------------------

# A. Text Elements


Instructions:

1.  Demonstrate the use of H1, H2, H3, H4, P, CodeSpan, Blockquote, and CodeBlock elements from MonsterUI.
2.  Use TextT Enum to style the elements
3.  Use MonsterUI theme by calling Theme and headers

Example:
```python
from fasthtml.common import *
from monsterui.all import *

# Create a basic HTML page with styled text elements using FrankenUI

page_content = Div(
    H1("Welcome to My Website", cls=TextT.primary),
    H2("A Brief Introduction",   cls=TextT.secondary),
    H3("Section Heading",        cls=TextT.bold),
    H4("Subsection Heading",     cls=TextT.italic),
    PParagraph("This is a standard paragraph of text.", cls=TextT.default),
    CodeSpan("Inline code example", cls=TextT.muted),
    Blockquote("A wise quote here.", cls=TextT.normal),
    CodeBlock("def my_function():\\n    print('Hello, world!')", cls=TextT.muted)
)
print(to_xml(page_content))
```

Explanation:
This example demonstrates the usage of the text-related elements from FrankenUI, showing how they are styled with different TextT options.


# B. Link Elements

Instructions:
1.  Show various Link styles using AT enum.
2.  Demonstrate creating htmx get request with AX element

Example:
```python
from fasthtml.common import *
from monsterui.all import *

# Create styled links

links = Div(
    A("Muted Link", cls=AT.muted, href="#"),
    A("Primary Link", cls=AT.primary, href="#"),
    A("Text Link", cls=AT.text, href="#"),
    AX("HTMX Get Link", hx_get="/data", target_id="my_div", hx_swap="innerHTML"),
    Div(id="my_div")
)
print(to_xml(links))
```

Explanation:
This example showcases various link styles using FrankenUI, highlighting different visual presentations and also creates a htmx link with AX


# C. Button Element


Instructions:
1.  Demonstrate different Button styles using ButtonT enum.
2.  Show button inside a Form element

Example:

```python
from fasthtml.common import *
from monsterui.all import *

buttons = Div(
    Button("Default Button",   cls=ButtonT.default),
    Button("Primary Button",   cls=ButtonT.primary),
    Button("Secondary Button", cls=ButtonT.secondary),
    Form(Button(type="submit", "Submit Button"))
)
print(to_xml(buttons))
```
Explanation:
This example covers the different Button styles available through MonsterUI, demonstrating a submit Button inside a Form element


# D. List Elements


Instructions:

1.  Show List element with different styles
2.  Use ListT enum to style the list elements

Example:
```python
from fasthtml.common import *
from monsterui.all import *

list_element = UkList(
    Li("Item 1"),
    Li("Item 2"),
    Li("Item 3"),
    cls=ListT.disc
)
print(to_xml(list_element))
```
Explanation:
This example covers different styles of the List elements using ListT enum for different bullet styles.


# E. Image Element

Instructions:
1.  Show a simple Image element with a link.

Example:
```python
from fasthtml.common import *
from monsterui.all import *

img_element = A(Img(src="https://picsum.photos/200/300", alt="Random Image"), href="#")
print(to_xml(img_element))
```
Explanation:
This example shows an Image wrapped in a link, pointing to a random image using picsum.photos.


# F. Input Elements


Instructions:
1.  Demonstrate various types of input fields: text, number, email, password, date, checkbox, radio, range, and textarea.
2.  Use LabelInput to show styled input elements

Example:
```python
from fasthtml.common import *
from monsterui.all import *

input_elements = Form(
    LabelInput("Text",      id="text_input",      type="text",     placeholder="Enter text"),
    LabelInput("Number",    id="number_input",    type="number",   placeholder="Enter number"),
    LabelInput("Email",     id="email_input",     type="email",    placeholder="Enter email"),
    LabelInput("Password",  id="password_input",  type="password", placeholder="Enter password"),
    LabelInput("Date",      id="date_input",      type="date"),
    LabelCheckboxX("Checkbox", id="checkbox_input"),
    LabelRadio("Radio",       id="radio_input"),
    LabelRange("Range",       id="range_input",     min="0", max="100", value="50"),
    LabelTextArea("Textarea", id="textarea_input", placeholder="Enter text here")
)
print(to_xml(input_elements))
```

Explanation:
This example provides a comprehensive demonstration of the different input types available, all styled using LabelInput for better visual appeal.


# G. Select Element

Instructions:
1. Show a Select element styled using LabelSelect and UkSelect, including optional Optgroup and styling options.

Example:
```python
from fasthtml.common import *
from monsterui.all import *

select_element = Form(
    LabelSelect(Option("Option 1"), Option("Option 2"), id="select_input"),
    LabelUkSelect(
            Optgroup(Option("Option A"), Option("Option B"), label="Group 1"),
            Optgroup(Option("Option C"), Option("Option D"), label="Group 2"),
            id="select_uk_input"))
print(to_xml(select_element))
```
Explanation:
This code creates a Select element using LabelSelect, and UkSelect with nested Optgroup elements, demonstrating different ways to structure a dropdown menu.


# H. Table Element

Instructions:

1.  Create a table using monsterui Table component with header, body and footer
2.  Add striped, hoverable and responsive classes

Example:

```python
from fasthtml.common import *
from monsterui.all import *

table_header = Tr(Th("Header 1"), Th("Header 2"))
table_body   = Tbody(Tr(Td("Data 1"), Td("Data 2")),
                    Tr(Td("Data 3"), Td("Data 4")))
table_footer = Tr(Td("Footer 1"), Td("Footer 2"))

table_element = Table(table_header, table_body, table_footer, cls=(TableT.striped, TableT.hover, TableT.responsive))
print(to_xml(table_element))
```
Explanation:
This generates a table structure with header, body, and footer, using the striped and hoverable classes for enhanced readability.

# --------------------------------------------------------------------------
# II. Layout Components and Examples
# --------------------------------------------------------------------------

# A. Container

Instructions:

1. Demonstrate the use of Container for layout, with default styling and expand options.

Example:

```python
from fasthtml.common import *
from monsterui.all import *

container = Container(P("Content inside container"), cls=ContainerT.expand)
print(to_xml(container))
```
Explanation:
This shows a simple Container usage, demonstrating the expand option for filling available space.


# B. Grid

Instructions:

1. Demonstrate creating a Grid with different column numbers, and adaptive behavior

Example:

```python
from fasthtml.common import *
from monsterui.all import *

grid = Grid(Div("Item 1"), Div("Item 2"), Div("Item 3"), cols=3, cols_sm=2, cols_md=1)
print(to_xml(grid))
```
Explanation:
This creates a grid layout with three items, varying the number of columns based on screen size.


# C. Section

Instructions:

1. Demonstrate use of Section for dividing content with different SectionT styles.

Example:
```python
from fasthtml.common import *
from monsterui.all import *

section = Section(P("Content in a section"), cls=SectionT.primary)
print(to_xml(section))
```
Explanation:
This showcases dividing content into sections with distinct styles using SectionT.

# D. Navigation

Instructions:

1. Create NavBar with a container and Left and Right sides

Example:

```python
from fasthtml.common import *
from monsterui.all import *

navbar = NavBar(
    NavBarLSide(A("Left Link")),
    NavBarRSide(A("Right Link"))
)
print(to_xml(navbar))
```
Explanation:
Create a simple NavBar with elements on left and right sides

# --------------------------------------------------------------------------
# III. Advanced Components and Examples
# --------------------------------------------------------------------------
# A. Card

Instructions:

1. Demonstrate various card styles, including headers, footers, and body content
2. Create a Card with a Table component inside it.

Example:
```python
from fasthtml.common import *
from monsterui.all import *

card = Card(
    H3("Card Title"),
    P("Card Body Content"),
    Table(Tr(Td("Cell 1"),Td("Cell 2"))),
    header=Div("Card Header"),
    footer=Button("Card Footer", cls=ButtonT.primary)
)
print(to_xml(card))
```
Explanation:
This code creates a styled card component with a custom header, body containing a table, and a primary styled button in the footer.


# B. Modal

Instructions:
1. Generate a modal
2. Use default ModalHeader and Footer
Example:

```python
from fasthtml.common import *
from monsterui.all import *

modal = Modal(
    ModalTitle("Modal Title"),
    ModalBody(P("Modal Body Content")),
    ModalFooter(Button("Close", cls=ButtonT.default))
)
print(to_xml(modal))
```
Explanation:
Generate a basic modal dialog with a title, body content, and a close button styled with monsterui defaults


# C. Form with Validation


Instructions:

1. Create a comprehensive form with input validation using html5 attributes

Example:
```python
from fasthtml.common import *
from monsterui.all import *

form = Form(
    LabelInput("Name", id="name", required=True, minlength="3"),
    LabelInput("Email", id="email", type="email", required=True),
    LabelInput("Age", id="age", type="number", min="18", max="99"),
    Button("Submit", type="submit", cls=ButtonT.primary)
)
print(to_xml(form))
```
Explanation:
This creates a form with required fields and HTML5 validation attributes to ensure data integrity before submission.

# D. Alert

Instructions:
1. Demonstrate the use of the Alert component with various styles

Example:
```python
from fasthtml.common import *
from monsterui.all import *

alert_element = Alert("This is an alert message", cls=AlertT.success)
print(to_xml(alert_element))
```
Explanation:
This example creates a success-style alert message using the Alert component from monsterui.

# E. Steps

Instructions:
1. Create a Steps container component
2. Use StepT to style individual LiStep

Example:
```python
from fasthtml.common import *
from monsterui.all import *

steps_element = Steps(
    LiStep("Step 1", cls=StepT.primary),
    LiStep("Step 2", cls=StepT.secondary),
    LiStep("Step 3")
)
print(to_xml(steps_element))
```
Explanation:
This example creates a steps process indicator with individual steps styled for emphasis, useful for multi-stage processes

# F. Tabs

Instructions:
1. Create a Tab Container with 2 Tabs with alternating styles
2. All Tabs are actionable and allow transitions

Example:

```python
from fasthtml.common import *
from monsterui.all import *

tabs = TabContainer(
    Li(A("Tab 1", href="#tab1"), cls='uk-active'),
    Li(A("Tab 2", href="#tab2")),
    alt=True, uk_switcher="connect: #tab-content"
)

tab_content = Div(id="tab-content", cls="uk-switcher")(
    Div("Content for Tab 1", id="tab1"),
    Div("Content for Tab 2", id="tab2")
)

print(to_xml(Div(tabs,tab_content)))
```
Explanation:
This creates a tabbed interface with two tabs, each linked to corresponding content areas, enabling dynamic content switching with appropriate styling.


# --------------------------------------------------------------------------
# IV. Full Page Examples
# --------------------------------------------------------------------------

# A. Basic Layout Page


Instructions:

1. Create a basic page layout with a header, sidebar, and main content area using container, grid, and other layout elements
2. Use MonsterUI styles to add styling

Example:
```python
from fasthtml.common import *
from monsterui.all import *

header = Div(H1("My Website", cls=TextT.primary), cls="p-4")
sidebar = Div(UkList(Li("Link 1"), Li("Link 2")), cls="p-4")
main_content = Div(P("Main Content Here"), cls="p-4")

page = Container(
    header,
    Grid(sidebar, main_content, cols=4),
    cls=ContainerT.expand
)
print(to_xml(page))
```
Explanation:
This constructs a basic website layout with a header, sidebar navigation, and main content, using the Container and Grid elements for structure.


# B. Form Page

Instructions:

1. Create a page focused on data input, including multiple labeled input fields, select elements, and validation attributes
2. Use UkFormSection to help divide the content

Example:

```python
from fasthtml.common import *
from monsterui.all import *

form_page = Container(
    H2("Registration Form", cls=TextT.primary),
    UkFormSection(
    "Personal Information",
        "",
    LabelInput("Name",     id="name",     required=True),
    LabelInput("Email",    id="email",    type="email", required=True),
        Button("Register", type="submit", cls=ButtonT.primary)
    )
    
)
print(to_xml(form_page))
```
Explanation:
This builds a registration form page, emphasizing labeled inputs and UkFormSection for organization.


# C. Dashboard Page


Instructions:

1. Show a multi-section dashboard page with statistics, charts, and tables
2. Import plotting library and show it in the chart
3. Use Cards to group content
Example:
```python
from fasthtml.common import *
from monsterui.all import *
import plotly.express as px
import pandas as pd

# Generate a sample chart
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes"],
    "Amount": [4, 1, 2, 2]
})
fig = px.bar(df, x="Fruit", y="Amount", title="Fruit Quantities")
chart_html = fig.to_html(include_plotlyjs=False, full_html=False)

dashboard = Container(
    H2("Dashboard", cls=TextT.primary),
    Grid(
        Card(H3("Total Sales"), P("$10,000")),
        Card(H3("New Users"),  P("50")),
        Card(H3("Page Views"), P("200")),
        Card(chart_html),
        cols=2
    )
)
print(to_xml(dashboard))
```

Explanation:
This constructs a dashboard layout, including charts, statistics, and a structured grid, emphasizing data visualization.


#D.  Authentication Page


Instructions:

1. Show a comprehensive login/register page
2. Use a Card Component for input
3. Use a MonsterUI component to split the Card

Example:
```python
from fasthtml.common import *
from monsterui.all import *

auth_page = Container(
    Grid(
        Div(),
        Card(H3("Login"),
            LabelInput("Email", id="email"),
            LabelInput("Password", id="password", type="password"),
            Button("Login", type="submit", cls=ButtonT.primary),
            DividerSplit("Or with"),
            Button("Sign in With Google")
        ),cols=2
    )
)
print(to_xml(auth_page))
```
Explanation:
Create an authentication page with fields for email, password as well as buttons that show third-party sign-ins and a title using components.


# --------------------------------------------------------------------------
# V. Theming and Customization
# --------------------------------------------------------------------------

# A. Themes


Instructions:

1. Demonstrate applying a theme using the Themes enum from MonsterUI
2. Show code for Tailwind and DaisyUI integration from Themes

Example:

```python
from fasthtml.common import *
from monsterui.all import *

theme_headers = Theme.blue.headers()  # Apply the blue theme

themed_page = Container(
    H2("Themed Page", cls=TextT.primary),
    P("Content with themed styles")
)
print(to_xml(themed_page))
```
Explanation:
This code shows how to use the Themes enum to import the proper css for styling a page element



# B. Custom CSS


Instructions:
1. Import a theme and then override some of the theme's css using Style
2. All CSS should be properly scoped to the current element using `me`
Example:

```python
from fasthtml.common import *
from monsterui.all import *

page_css = Style("me {background-color: navy; color:white}")

customized_page = Container(
    H2("Customized Page", cls=TextT.primary),
    P("Content with customized styles")
)
print(to_xml(Div(customized_page,page_css)))
```


# --------------------------------------------------------------------------
# VI. Event handling
# --------------------------------------------------------------------------

# A. Htmx Requests


Instructions:

1. Set up a few components to take a request
2. Handle a get request using MonsterUI and respond with proper styles.

Example:

```python
from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app()

@rt("/get_content")
def get_content():
    return Card(P("New content loaded via HTMX"))

get_button = A("Load Content", hx_get="/get_content", hx_target="#content_area", hx_swap="innerHTML")
content_area = Div(id="content_area", P("Initial content"))

print(to_xml(Div(get_button,content_area)))
```
Explanation:
This code shows that the elements are properly set up to be responsive with a get request handler


# --------------------------------------------------------------------------
# VII. More Complex Pages
# --------------------------------------------------------------------------

# A. Settings/Profile Page

Instructions:

1. Settings/Profile Page from TailwindUI

Example:

```python
from fasthtml.common import *
from monsterui.all import *

settings_page = Container(
    H2("Settings", cls=TextT.primary),
    Form(
        LabelInput("Name", id="name"),
        LabelInput("Email", id="email", type="email"),
        LabelCheckboxX("Subscribe to Newsletter", id="newsletter"),
        Button("Save Changes", type="submit", cls=ButtonT.primary)
    )
)
print(to_xml(settings_page))
```




This is an extended set of instructions for an LLM designed to generate FastHTML code using MonsterUI. These instructions expand on the previous ones, focusing on increasingly complex components and full page layouts, all while adhering to the core principles.



**Core Principles (REITERATED):**

1.  **`to_xml` Output:** Every code snippet MUST end with `print(to_xml(<COMPONENT CODE>))`.
2.  **MonsterUI Focus:** Prefer MonsterUI components first. Use Tailwind CSS (via MonsterUI) for *additional* styling only.
3.  **FastHTML Conventions:** Adhere to routing, data handling, and component patterns.
4.  **Example-Driven:** Provide clear, executable examples.
5.  **Correctness:** Code MUST be valid and generate correct HTML.
6.  Concise and well-structured code.
7. Type Annotations
8. Clear and Self Explanatory comments


# --------------------------------------------------------------------------
# A. More Complex Components (Expanding on Previous Examples)
# --------------------------------------------------------------------------

# 1. Enhanced Forms:

Instructions:

Create forms using MonsterUI form elements that include validation, different input types, labels, help text, and structured layout. Use Grid to create responsive layouts within forms.

```python
from fasthtml.common import *
from monsterui.all import *

# Extended Registration Form
registration_form = Container(
    H2("Register", cls=TextT.primary),
    Form(
        Grid(
            Div(LabelInput("First Name", id="first_name", required=True)),
            Div(LabelInput("Last Name", id="last_name", required=True)),
            cols=2
        ),
        LabelInput("Email", id="email", type="email", required=True, placeholder="email@example.com"),
        LabelInput("Password", id="password", type="password", required=True, minlength="8"),
        LabelUkSelect(
            Option("Select your Country", value="", disabled=True, selected=True),
            Option("USA"), Option("Canada"), Option("UK"),
            label="Country", id="country"
        ),
        LabelCheckboxX("I agree to the terms and conditions", id="agree_terms", required=True),
        Button("Register", type="submit", cls=ButtonT.primary)
    )
)
print(to_xml(registration_form))

```

Details:

*   The form is encapsulated within a `Container` for basic page structure.
*   `Grid` is used to arrange the first name and last name fields side-by-side.
*   `LabelInput` provides labels and handles spacing.
*   HTML5 validation is utilized with `required` and `minlength` attributes.
*   A `Select` dropdown is included for the country selection.
*   The checkbox has been styled using `Switch` for user confirmation.



# 2. Enhanced Cards:

Instructions:

Create cards that include interactive elements like buttons, dropdowns, tables, and custom content sections.

```python
from fasthtml.common import *
from monsterui.all import *

# Product Card
product_card = Card(
    Img(src="https://picsum.photos/300/200", alt="Product Image", cls="rounded-md"),
    H3("Product Title", cls=TextT.bold),
    P("A brief description of the product.", cls=TextFont.muted_sm),
    Grid(
        Button("Add to Cart", cls=ButtonT.primary),
        Button("View Details", cls=ButtonT.secondary),
        cols=2
    )
)
print(to_xml(product_card))
```

Details:

*   A `Card` groups together an image, title, description, and action buttons.
*   The image is set to have rounded corners using Tailwind classes (applied via monsterui header).
*   Buttons are arranged using a 2-column `Grid`.



# 3. More Complex Navigation:

Instructions:

Implement navigation bars, sidebars, and tabbed interfaces using appropriate MonsterUI elements.

```python
from fasthtml.common import *
from monsterui.all import *

# Simple Sidebar Navigation
sidebar_nav = NavContainer(
    NavHeaderLi("Menu"),
    Li(A("Home", href="#")),
    Li(A("Products", href="#")),
    Li(A("Services", href="#")),
    Li(A("About", href="#")),
    cls=NavT.secondary # Applying the NavT
)
print(to_xml(sidebar_nav))

# Example tab element
simple_tab_element = TabContainer(
    Li(A('First Tab',    href='#'),    cls='uk-active'),
    Li(A('Second Tab', href='#')),
    Li(A('Third Tab', cls='opacity-50'), cls='uk-disabled'),
    uk_switcher='connect: #component-nav; animation: uk-animation-fade',
    alt=True)
print(to_xml(simple_tab_element))

# Example Nav Bar
nav_bar = NavBar(
    NavBarLSide(A("Logo", href="#")),
    NavBarCenter(Input(placeholder="Search")),
    NavBarRSide(A("Login", href="#"), A("Register", href="#")),
)
print(to_xml(nav_bar))
```

Details:

*   `NavContainer` creates a styled sidebar navigation menu using `LI` elements
*   `TabContainer` helps in making tab elements.
*  `NavBar` helps create navigations with logo, search bar and login/ register links.


# --------------------------------------------------------------------------
# B. Full Page Layout Examples (Expanding on Previous Examples)
# --------------------------------------------------------------------------

# 1. E-commerce Product Listing Page:

Instructions:

Create a page that displays a list of products with images, descriptions, and Add to Cart buttons. Use a `Grid` to arrange the product cards, and a `NavBar` to add navigation and search capabilities.

```python
from fasthtml.common import *
from monsterui.all import *

# Creating a sample nav bar with a search input in the center
nav_bar = NavBar(
    NavBarLSide(A("Logo", href="#")),
    NavBarCenter(Input(placeholder="Search")),
    NavBarRSide(A("Cart", href="#"), A("Account", href="#")),
    )

# Creating a function to generate product cards
def create_product_card(name: str, description: str, image_url: str) -> Card:
    return Card(
        Img(src=image_url, alt=name, cls="rounded-md"),
        H3(name, cls=TextT.bold),
        P(description, cls=TextFont.muted_sm),
        Button("Add to Cart", cls=ButtonT.primary),
    )

# Sample product data
products = [
    {"name": "Awesome T-Shirt", "description": "A comfortable and stylish t-shirt.", "image_url": "https://picsum.photos/200/300"},
    {"name": "Cool Mug", "description": "A perfect mug for your morning coffee.", "image_url": "https://picsum.photos/200/301"},
    {"name": "Fancy Hat", "description": "Stay warm and fashionable.", "image_url": "https://picsum.photos/200/302"}
]

# Generate product cards from product data
product_cards = [create_product_card(**product) for product in products]

# Creating product listing page using components
product_listing_page = Container(
    nav_bar,
    H2("Products", cls=TextT.primary),
    Grid(*product_cards, cols=3),
    )

# Show product listing page code and to_xml function
print(to_xml(product_listing_page))
```
Details:

*   A `NavBar` helps make a navigation menu with Logo, Search, and login/register links.
*   `Card` is used to display individual product.
*   A function called `create_product_card` has been designed to generate the product cards with custom name, description, and image URLs, making the page dynamic


# --------------------------------------------------------------------------
# VIII. Tailwind CSS Integration with MonsterUI
# --------------------------------------------------------------------------

# A. Using Tailwind Classes

Instructions:
1. Only use Tailwind classes when MonsterUI's built-in styling options are insufficient
2. Apply classes through the `cls` parameter
3. Follow the component-first principle: prefer MonsterUI's built-in styling (like ButtonT, TextT) before adding Tailwind classes

Example:
```python
from fasthtml.common import *
from monsterui.all import *

# Basic spacing and layout classes
component = Container(
    # Add padding and margin
    cls="p-4 mt-2",  
    
    # Content here
)

# Flexbox and alignment
flex_component = Div(
    "Content",
    cls="flex items-center justify-between gap-4"
)

# Responsive design
responsive_grid = Grid(
    # Grid will be 1 column on mobile, 2 on tablet, 3 on desktop
    cls="grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
)

print(to_xml(Div(component, flex_component, responsive_grid)))
```

# B. Common Tailwind Patterns

1. Layout Classes:
   - Flexbox: `flex items-center justify-center`
   - Grid: `grid grid-cols-{n} gap-{n}`
   - Spacing: `p-{n} m-{n} space-y-{n}`
   - Width/Height: `w-full h-screen max-w-{size}`

2. Typography:
   - Font size: `text-sm text-base text-lg`
   - Font weight: `font-normal font-medium font-bold`
   - Text color: `text-gray-500 text-primary-600`
   - Line height: `leading-tight leading-normal leading-loose`

3. Responsive Design:
   - Breakpoints: `sm:` (640px), `md:` (768px), `lg:` (1024px), `xl:` (1280px)
   - Example: `md:hidden lg:block`

4. Interactive States:
   - Hover: `hover:bg-gray-100`
   - Focus: `focus:ring focus:ring-primary-500`
   - Active: `active:bg-gray-200`

# C. Best Practices

1. Component-First Approach:
```python
# GOOD: Use MonsterUI's built-in styling first
button = Button("Click me", cls=ButtonT.primary)

# GOOD: Add Tailwind only for additional styling
button = Button("Click me", cls=(ButtonT.primary, "mt-4 hover:scale-105"))

# BAD: Don't recreate MonsterUI styles with Tailwind
button = Button("Click me", cls="bg-blue-500 text-white rounded-lg")  # Don't do this
```

2. Responsive Design:
```python
# Use MonsterUI's responsive props when available
grid = Grid(cols=1, cols_md=2, cols_lg=3)

# Add Tailwind responsive classes for additional control
container = Container(
    cls="px-4 md:px-6 lg:px-8 max-w-7xl mx-auto"
)
```

3. Common Layout Patterns:
```python
# Centered content with max width
layout = Container(
    cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
)

# Card with hover effect
card = Card(
    cls="hover:shadow-lg transition-shadow duration-200"
)

# Sticky header
header = NavBar(
    cls="sticky top-0 z-50 bg-white/80 backdrop-blur-sm"
)
```

4. Animation and Transitions:
```python
# Loading states
loading = Div(
    "Loading...",
    cls="animate-pulse text-gray-500"
)

# Interactive elements
button = Button(
    "Hover me",
    cls=(ButtonT.primary, "transition-transform hover:scale-105")
)
```

5. Form Elements:
```python
# Input with focus ring
input_field = LabelInput(
    "Email",
    cls="focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
)

# Custom checkbox
checkbox = LabelCheckboxX(
    "Remember me",
    cls="checked:bg-primary-500 hover:bg-gray-100"
)
```

Remember:
- Always prioritize MonsterUI's built-in styling options
- Use Tailwind classes to enhance, not replace, MonsterUI's default styles
- Keep responsive design in mind
- Group related Tailwind classes logically
- Consider accessibility when adding custom styles
- Use comments to explain complex Tailwind combinations

