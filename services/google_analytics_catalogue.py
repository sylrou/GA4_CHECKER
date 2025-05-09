'''
This is the GA4 data_catalogue form offcial Google documentation :
'''

# 2025-03-21 - Dictionary mapping event names to their descriptions
GA4_RECOMMENDED_EVENT_LIST = [
    "add_payment_info", "add_shipping_info", "add_to_cart",
    "add_to_wishlist", "begin_checkout", "close_convert_lead",
    "close_unconvert_lead", "disqualify_lead", "earn_virtual_currency",
    "generate_lead", "join_group", "level_end",
    "level_start", "level_up", "login",
    "post_score", "purchase", "qualify_lead",
    "refund", "remove_from_cart", "search",
    "select_content", "select_item", "select_promotion",
    "share", "sign_up", "spend_virtual_currency",
    "tutorial_begin", "tutorial_complete", "unlock_achievement",
    "view_cart", "view_item", "view_item_list",
    "view_promotion", "working_lead"
]

# 2025-03-21 - Dictionary mapping event names to their descriptions
GA4_RECOMMENDED_EVENT_ALL = {
    "ad_impression": "sees an advertisement, for apps only",
    "earn_virtual_currency": "earns virtual currency (coins, gems, tokens, etc.)",
    "generate_lead": "submits a form or a request for information",
    "join_group": "joins a group",
    "login": "logs in",
    "purchase": "completes a purchase",
    "refund": "receives a refund",
    "search": "searches your website or app",
    "select_content": "selects content on your website or app",
    "share": "shares content from your website or app",
    "sign_up": "signs up for an account on your website or app",
    "spend_virtual_currency": "spends virtual currency (coins, gems, tokens, etc.)",
    "tutorial_begin": "begins a tutorial during an on-boarding process",
    "tutorial_complete": "completes a tutorial during an on-boarding process"
}

# 2025-03-21 - Dictionary mapping event names to their descriptions
GA4_RECOMMENDED_EVENT_ECOMMERCE = {
    "add_payment_info": "Submits their payment information during checkout",
    "add_shipping_info": "Submits their shipping information during checkout",
    "add_to_cart": "Adds items to their shopping cart",
    "add_to_wishlist": "Adds items to their wishlist",
    "begin_checkout": "Begins checkout",
    "purchase": "Completes a purchase",
    "refund": "Receives a refund",
    "remove_from_cart": "Removes items from their shopping cart",
    "select_item": "Selects an item from a list of items or offerings",
    "select_promotion": "Selects a promotion",
    "view_cart": "Views their shopping cart",
    "view_item": "Views an item",
    "view_item_list": "Views a list of items or offerings",
    "view_promotion": "Views a promotion on your website or app"
}

# 2025-03-21 - Dictionary mapping event names to their descriptions
GA4_RECOMMENDED_EVENT_LEAD_GEN = {
    "generate_lead": "Submits a form online or provides information offline",
    "qualify_lead": "Is marked as fitting the criteria to become a qualified lead",
    "disqualify_lead": "Is marked as disqualified from becoming a lead for one of several reasons",
    "working_lead": "Contacts or is contacted by a representative",
    "close_convert_lead": "Becomes a converted lead (a customer)",
    "close_unconvert_lead": "Is marked as not becoming a converted lead for one of several reasons"
}

# 2025-03-21 - Dictionary mapping event names to their descriptions
GA4_RECOMMENDED_EVENT_GAME = {
    "earn_virtual_currency": "earns virtual currency (coins, gems, tokens, etc.)",
    "join_group": "joins a group",
    "level_end": "completes a level in a game",
    "level_start": "starts a new level in a game",
    "level_up": "levels-up in the game",
    "post_score": "posts their score",
    "select_content": "selects content",
    "spend_virtual_currency": "spends virtual currency (coins, gems, tokens, etc.)",
    "tutorial_begin": "begins a tutorial during an on-boarding process",
    "tutorial_complete": "completes a tutorial during an on-boarding process",
    "unlock_achievement": "unlocks an achievement"
}

# 2025-03-21 - Dictionary about ecommerce the items structures
GA4_ITEM_STRUCTURE = {
    "fields": {
        "required": [
            "item_id", "item_name", "price",
            "quantity"
        ],
        "optional": [
            "affiliation", "coupon", "discount",
            "index", "item_brand", "item_category",
            "item_category2", "item_category3", "item_category4",
            "item_category5", "item_list_id", "item_list_name",
            "item_variant", "in_stock", "location_id"
        ]
    }
}

# 2025-03-21 - Dictionary about ecommerce events structures
GA4_MANDATORY_DIMENSION_IN_RECOMMENDED_EVENT = {
    "add_payment_info": {
        "fields": {
            "required": ["currency", "value"] + GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon", "payment_type"] + GA4_ITEM_STRUCTURE["fields"]["optional"],
            "description": "Submits their payment information during checkout",
        }
    },
    "add_shipping_info": {
        "fields": {
            "required": ["currency", "value"] + GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon", "shipping_tier"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "purchase": {
        "fields": {
            "required": ["currency", "value", "transaction_id"] + GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon", "shipping", "tax"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "add_to_cart": {
        "fields": {
            "required": GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "add_to_wishlist": {
        "fields": {
            "required": GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "begin_checkout": {
        "fields": {
            "required": GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "view_cart": {
        "fields": {
            "required": GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "remove_from_cart": {
        "fields": {
            "required": GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "select_item": {
        "fields": {
            "required": GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "view_item": {
        "fields": {
            "required": GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "view_item_list": {
        "fields": {
            "required": ["item_list_id", "item_list_name"] + GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "select_promotion": {
        "fields": {
            "required": ["promotion_id", "promotion_name"] + GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "view_promotion": {
        "fields": {
            "required": ["promotion_id", "promotion_name"] + GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "refund": {
        "fields": {
            "required": ["transaction_id","currency", "value"] + GA4_ITEM_STRUCTURE["fields"]["required"],
            "not_required": ["coupon", "tax", "shipping"] + GA4_ITEM_STRUCTURE["fields"]["optional"]
        }
    },
    "share": {
        "fields": {
            "required": '',
            "not_required": ''
        }
    },
    "sign_up": {
        "fields": {
                    "required": '',
                    "not_required": ''
                }
    },
    "qualify_lead": {
        "fields": {
            "required": ["currency", "value"]
        }
    },
    "login": {
        "fields": {
                    "required": '',
                    "not_required": ''
                }
    }
}

event_params_dict = {
    'batch_ordering_id': 'standard',
    'batch_page_id': 'standard',
    'campaign': 'standard',
    'click_text': 'standard',
    'click_url': 'standard',
    'debug_mode': 'standard',
    'engaged_session_event': 'standard',
    'engagement_time_msec': 'standard',
    'entrances': 'standard',
    'ga_session_id': 'standard',
    'ga_session_number': 'standard',
    'ignore_referrer': 'standard',
    'link_classes': 'standard',
    'link_domain': 'standard',
    'link_id': 'standard',
    'link_url': 'standard',
    'medium': 'standard',
    'outbound': 'standard',
    'page_location': 'standard',
    'page_path': 'standard',
    'page_referrer': 'standard',
    'page_title': 'standard',
    'page_url': 'standard',
    'percent_scrolled': 'standard',
    'session_engaged': 'standard',
    'source': 'standard',
    'term': 'standard'
}