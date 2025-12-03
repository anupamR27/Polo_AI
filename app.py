# #!/usr/bin/env python3
# """
# polo_demo_gui.py

# Cross-platform tkinter demo GUI for a voice assistant named "Polo".
# This is a standalone demo screen only (no AI / voice command logic included).
# """

# import tkinter as tk
# from tkinter import ttk, scrolledtext, messagebox
# import threading
# import queue
# import time

# APP_TITLE = "Polo — Demo"
# WINDOW_SIZE = "700x480"

# class PoloDemoGUI:
#     def __init__(self, root):
#         self.root = root
#         root.title(APP_TITLE)
#         root.geometry(WINDOW_SIZE)
#         root.minsize(520, 360)

#         # Main frames
#         self._create_top_bar()
#         self._create_center_area()
#         self._create_status_bar()

#         # Internal state
#         self._msg_queue = queue.Queue()
#         self._listening = False
#         self._worker_thread = None

#         # Periodic UI update from queue
#         root.after(150, self._poll_queue)

#     def _create_top_bar(self):
#         top = ttk.Frame(self.root, padding=(8, 8, 8, 0))
#         top.pack(fill=tk.X)

#         self.start_btn = ttk.Button(top, text="Start Listening", command=self._start_demo)
#         self.start_btn.pack(side=tk.LEFT, padx=(0, 6))

#         self.stop_btn = ttk.Button(top, text="Stop Listening", command=self._stop_demo, state=tk.DISABLED)
#         self.stop_btn.pack(side=tk.LEFT)

#         ttk.Separator(top, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)

#         self.cmd_entry = ttk.Entry(top)
#         self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
#         self.cmd_entry.bind("<Return>", lambda e: self._on_send())

#         self.send_btn = ttk.Button(top, text="Send", command=self._on_send)
#         self.send_btn.pack(side=tk.LEFT)

#     def _create_center_area(self):
#         center = ttk.Frame(self.root, padding=8)
#         center.pack(fill=tk.BOTH, expand=True)

#         # Left: controls / info
#         left = ttk.Frame(center)
#         left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8))

#         about = ttk.Label(left, text="Polo (Demo UI)", font=("Helvetica", 14, "bold"))
#         about.pack(anchor="nw", pady=(0,10))

#         info_text = ("This is a demo interface for Polo.\n\n"
#                      "- Start/Stop buttons simulate listening.\n"
#                      "- Use the entry to type a command and press Send.\n"
#                      "- The log area shows events and responses.\n\n"
#                      "No voice or AI logic is included here.")
#         lbl = ttk.Label(left, text=info_text, wraplength=220, justify=tk.LEFT)
#         lbl.pack(anchor="nw")

#         # Right: a large log area
#         right = ttk.Frame(center)
#         right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         log_label = ttk.Label(right, text="Activity Log")
#         log_label.pack(anchor="w")

#         self.log_area = scrolledtext.ScrolledText(right, wrap=tk.WORD, state=tk.DISABLED, height=15)
#         self.log_area.pack(fill=tk.BOTH, expand=True, pady=(6,0))

#     def _create_status_bar(self):
#         self.status_var = tk.StringVar(value="Idle")
#         status_frame = ttk.Frame(self.root)
#         status_frame.pack(fill=tk.X, side=tk.BOTTOM, ipady=4)
#         status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor="w")
#         status_label.pack(fill=tk.X, padx=8)

#     # UI helpers
#     def _log(self, message: str):
#         """Thread-safe enqueue of a log message."""
#         self._msg_queue.put(("log", message))

#     def _set_status(self, text: str):
#         self._msg_queue.put(("status", text))

#     def _append_log(self, message: str):
#         self.log_area.configure(state=tk.NORMAL)
#         self.log_area.insert(tk.END, message + "\n")
#         self.log_area.see(tk.END)
#         self.log_area.configure(state=tk.DISABLED)

#     # Simulated start/stop actions (no actual microphone)
#     def _start_demo(self):
#         if self._listening:
#             return
#         self._listening = True
#         self.start_btn.config(state=tk.DISABLED)
#         self.stop_btn.config(state=tk.NORMAL)
#         self._set_status("Listening (demo)")
#         self._log("Demo: Started listening.")
#         # Spawn a worker thread to simulate background events
#         self._worker_thread = threading.Thread(target=self._demo_worker, daemon=True)
#         self._worker_thread.start()

#     def _stop_demo(self):
#         if not self._listening:
#             return
#         self._listening = False
#         self.start_btn.config(state=tk.NORMAL)
#         self.stop_btn.config(state=tk.DISABLED)
#         self._set_status("Idle")
#         self._log("Demo: Stopped listening.")

#     def _demo_worker(self):
#         """Simulate events from a background listener — just for demo purposes."""
#         counter = 0
#         while self._listening and counter < 10:
#             time.sleep(2)
#             # simulate "heard text" events
#             self._log(f"Simulated: Heard 'Demo command {counter+1}'")
#             self._log(f"Simulated: Handled 'Demo command {counter+1}'")
#             counter += 1
#         # when loop exits, update UI
#         if self._listening:
#             self._log("Demo: Background worker finished.")
#         else:
#             self._log("Demo: Background worker stopped early.")
#         # ensure we set listening flag false in case stop was not pressed
#         self._listening = False
#         self._msg_queue.put(("ui", "stop_buttons"))

#     def _on_send(self):
#         text = self.cmd_entry.get().strip()
#         if not text:
#             messagebox.showinfo("Empty command", "Please type a command or use Start Listening.")
#             return
#         self._append_log(f"You (typed): {text}")
#         # Demo: show a simple fake response
#         self._append_log(f"Polo (demo): Acknowledged '{text}'")
#         self.cmd_entry.delete(0, tk.END)

#     def _poll_queue(self):
#         """Process queued messages from background threads."""
#         try:
#             while True:
#                 typ, payload = self._msg_queue.get_nowait()
#                 if typ == "log":
#                     self._append_log(payload)
#                 elif typ == "status":
#                     self.status_var.set(payload)
#                 elif typ == "ui" and payload == "stop_buttons":
#                     # ensure buttons are in a consistent state
#                     self.start_btn.config(state=tk.NORMAL)
#                     self.stop_btn.config(state=tk.DISABLED)
#                     self.status_var.set("Idle")
#         except queue.Empty:
#             pass
#         finally:
#             self.root.after(150, self._poll_queue)

# def main():
#     root = tk.Tk()
#     # Use ttk theme if available for a nicer look
#     try:
#         style = ttk.Style(root)
#         style.theme_use('clam')  # 'clam', 'alt', 'default' are common; falls back if not available
#     except Exception:
#         pass

#     app = PoloDemoGUI(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()




from tkinter import *

root = Tk()

#creating a label widget
myLabel = Label(root , text = "Hello")
myLabel.pack() #shoving it in the loop

root.mainloop()