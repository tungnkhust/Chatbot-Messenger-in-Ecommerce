import json
from typing import Dict, List, Text
import shopify
from db_api.config import API_KEY, API_VERSION, APP_PASSWORD, SHOP_URL


def create_order(
    email: Text,
    address: Text,
    city: Text,
    province: Text,
    country: Text,
    zip: Text,
    firstname: Text,
    lastname: Text,
    items: List[Dict[Text, int]],
):
    with shopify.Session.temp(SHOP_URL, API_VERSION, APP_PASSWORD):
        response = shopify.GraphQL().execute(
            """
        mutation draftOrderCreate($input: DraftOrderInput!) {
            draftOrderCreate(input: $input) {
                draftOrder {
                    # DraftOrder fields
                    id
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """,
            variables={
                "input": {
                    "email": email,
                    "shippingAddress": {
                        "address1": address,
                        "city": city,
                        "province": province,
                        "country": country,
                        "zip": zip,
                        "firstName": firstname,
                        "lastName": lastname,
                    },
                    "lineItems": items,
                }
            },
        )

    return json.loads(response)