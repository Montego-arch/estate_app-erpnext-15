// Copyright (c) 2023, Montego and contributors
// For license information, please see license.txt

frappe.ui.form.on("Estate Settings", {
	refresh(frm) {
        const btn = frm.add_custom_button("Sync Products Now", () => {
            frappe.call({
                method: "estate_app.tasks.sync_products_from_printrove",
                btn
            }).then(() => {
                frappe.show_alert({ message: "Store Products Synced Successfully!", indicator: "green"})
            })
        })

	},
});
