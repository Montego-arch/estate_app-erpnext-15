import frappe

@frappe.whitelist()

def handle_checkout_submit():
    data = frappe.form_dict
    
    #TODO  redirect to payment page
    pass