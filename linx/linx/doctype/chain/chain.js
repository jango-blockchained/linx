// Copyright (c) 2024, jango_blockchained and contributors
// For license information, please see license.txt

frappe.ui.form.on("Chain", {
    refresh(frm) {
        frm.trigger('set_mandatory_group_fields');
        frm.trigger('set_mandatory_layer_fields');
        frm.trigger('display_group_fields');
        frm.trigger('display_layer_fields');
        // --
        frm.set_query('parent_chain', () => {
            return {
                filters: {
                    layer: ['<', frm.doc.layer],
                    name: ['!=', frm.doc.name]
                }
            }
        });
    },
    is_group: function(frm) {
        frm.trigger('set_mandatory_group_fields');
        frm.trigger('set_mandatory_layer_fields');
        frm.trigger('display_group_fields');
    },
    layer: function(frm) {
        frm.trigger('display_layer_fields');
        frm.trigger('set_mandatory_layer_fields');
    },
    set_mandatory_group_fields(frm) {
        frm.toggle_reqd('chain_id', frm.doc.is_group === 0);
        frm.toggle_reqd('rpc_url', frm.doc.is_group === 0);
        frm.toggle_reqd('layer', frm.doc.is_group === 0);
    },
    set_mandetory_layer_fields(frm) {
        frm.toggle_reqd('parent_chain', frm.doc.layer > 1);
    },
    display_group_fields(frm) {
        frm.toggle_display('chain_id', frm.doc.is_group === 0);
        frm.toggle_display('column_break_naming', frm.doc.is_group === 0);
        frm.toggle_display('type', frm.doc.is_group === 0);
        frm.toggle_display('0x_id', frm.doc.is_group === 0);
        frm.toggle_display('urls_section', frm.doc.is_group === 0);
        frm.toggle_display('rpc_url', frm.doc.is_group === 0);
        frm.toggle_display('block_explorer_url', frm.doc.is_group === 0);
        frm.toggle_display('layer_section', frm.doc.is_group === 0);
    },
    display_layer_fields(frm) {
        frm.toggle_display('column_break_layer', frm.doc.layer > 1);
        frm.toggle_display('parent_chain', frm.doc.layer > 1);
    }
});
