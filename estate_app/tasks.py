import frappe

from frappe.integrations.utils import make_get_request, make_post_request

BASE_URL =  "https://api.printrove.com/"
SECONDS_IN_YEAR = 364 * 24 * 60  * 60


@frappe.whitelist()
def sync_products_from_printrove():
    access_token = get_printrove_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    products_route = "api/external/products"
    all_products = make_get_request(f"{BASE_URL}{products_route}", headers=headers)
    all_products = all_products["products"]

    for product in all_products:
        product_data = {
                "front_mockup": product["mockup"]["front_mockup"],
                "back_mockup":product["mockup"]["back_mockup"],
        }
        if not frappe.db.exists("Store Product", {"estate_id":product["id"]}):
            doc = frappe.get_doc({
                "doctype": "Store Product",
                "name": product["name"],
                "estate_id": product["id"],
                **product_data
            }).insert(ignore_permissions=True)
        else:
            # update the product
            doc = frappe.get_doc("Store Product", {"estate_id":product["id"]})
            doc.update({
                **product_data
            })
            doc.save(ignore_permissions=True)



def get_printrove_access_token():
    token = frappe.cache.get_value("estate_access_token")
    if token:
        return token
    estate_settings = frappe.get_cached_doc("Estate Settings")
    auth_route = "api/external/token"
    response = make_post_request(
        f"{BASE_URL}{auth_route}", 
        data={
            "email": estate_settings.email, 
            "password": estate_settings.get_password("password"),
            },
        )
    
    access_token = response["access_token"]

    frappe.cache.set_value("estate_access_token", access_token, expires_in_sec=SECONDS_IN_YEAR)

    return access_token

