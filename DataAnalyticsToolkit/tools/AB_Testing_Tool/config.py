"""Secret key to encrypt sessions cookies"""
TEST_LOCATION_OPTIONS = [
    {
        "name": "checkout",
        "mcvr_standard": "eventAction in (\"transaction\")",
        "mcvr_standard_descr": "User places a transaction"
    },
    {
        "name": "login",
        "mcvr_standard": "eventAction in (\"login.succeeded\",\"register.completed\")",
        "mcvr_standard_descr": "User successfully logs in or registers"
    },
    {
        "name": "home/launcher",
        "mcvr_standard": "eventAction in (\"shop_details.loaded\")",
        "mcvr_standard_descr": "User enters shop details"
    },
    {
        "name": "shop_list",
        "mcvr_standard": "eventAction in (\"shop_details.loaded\")",
        "mcvr_standard_descr": "User enters to shop's profile"
    },
    {
        "name": "show_details",
        "mcvr_standard": "eventAction in (\"checkout.loaded\")",
        "mcvr_standard_descr": "User loads the checkout"
    }
]

MAIN_KPI_OPTIONS = [
    "CVR", "session mCVR1", "session mCVR2", "session mCVR3", "session mCVR4", "session macroCVR1", "session macroCVR2",
    "session macroCVR3", "session macroCVR4", "Location mCVR", "Login/Register CVR", "Avg. Time to order",
    "GMV per session", "GFV per session", "GMV per user", "GFV per user", "Orders With Voucher",
    "Gross Cancellation/Fail Rate", "Contact per Order/Contact Rate", "Promised DT (MIN)", "Avg Delivery Distance",
    "Avg Delivery Time (MIN)", "NPS AO"
]

SQUAD_OPTIONS = [
    "Acquisition", "Activation", "Cart and Checkout",
    "Delivery", "New Verticals", "Partners", "Payments",
    "Restaurants", "Retention", "Search", "Wallet"
]

TRIBE_OPTIONS = [
    "Delivery", "Growth", "Partners", "Payments", "Shopping", "Wallet"
]

PLATFORM_OPTIONS = [
    "Android", "IOS", "Web Mobile", "Web Desktop"
]
