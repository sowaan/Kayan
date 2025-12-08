from erpnext.accounts.doctype.journal_entry.journal_entry import JournalEntry as ERPNextJournalEntry
import frappe
from frappe import _

class CustomJournalEntry(ERPNextJournalEntry):
    def queue_action(self, action, **kwargs):
        # Save current state (parent + children) before queueing,
        # so the worker sees the latest accounts table.
        #frappe.msgprint("Update Started")

        if getattr(self, "__unsaved", False) or self.is_new():
            self.save(ignore_permissions=True)

        return super().queue_action(action, **kwargs)

    def submit(self):
        if len(self.accounts) > 100:
            frappe.msgprint(_("The task has been enqueued as a background job."), alert=True)
            return self.queue_action("submit", timeout=4600)
        else:
            return self._submit()

    def cancel(self):
        if len(self.accounts) > 100:
            frappe.msgprint(_("The task has been enqueued as a background job."), alert=True)
            return self.queue_action("cancel", timeout=4600)
        else:
            return self._cancel()