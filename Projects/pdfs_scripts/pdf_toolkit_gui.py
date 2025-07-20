#!/usr/bin/env python3
"""
pdf_toolkit_gui.py

Dependencies (install once before first launch):
    pip install tkinterdnd2 PyMuPDF Pillow pikepdf reportlab

A Tkinter GUI for PDF operations:
  • Merge (with index, metadata, encryption)
  • Split (placeholder)
  • Compress (placeholder)
  • Unlock (batch-unlock with password reuse)

"""

import os
import json
import tempfile
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD

# PyMuPDF provides the 'fitz' namespace—ensure you installed PyMuPDF, not another 'fitz' package
import fitz  

from PIL import Image, ImageTk
import PyPDF2, pikepdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- Ensure required directories exist ---
for d in ('static', 'logs', 'output_pages', 'unlocked'):
    os.makedirs(d, exist_ok=True)

# --- Config & Globals ---
HOME = Path.home()
HISTORY_FILE   = HOME / '.pdf_toolkit_history.json'
PROFILES_FILE  = HOME / '.pdf_toolkit_profiles.json'
LOG_FILE       = HOME / '.pdf_toolkit_log.json'
PASSWORDS_FILE = HOME / '.pdf_toolkit_passwords.json'
MAX_HISTORY    = 10

# --- Persistence Helpers ---
def load_json(path):
    try: return json.loads(path.read_text())
    except: return None

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))

def load_history():
    raw = load_json(HISTORY_FILE)
    if isinstance(raw, dict): return raw.get('folders', [])
    if isinstance(raw, list): return raw
    return []

def save_history(folders):
    save_json(HISTORY_FILE, {'folders': folders[:MAX_HISTORY]})

def add_to_history(folder):
    folder = str(Path(folder).resolve())
    hist = load_history()
    if folder in hist: hist.remove(folder)
    hist.insert(0, folder)
    save_history(hist)
    return hist

def load_profiles():
    raw = load_json(PROFILES_FILE)
    return raw if isinstance(raw, dict) else {}

def save_profiles(profiles):
    save_json(PROFILES_FILE, profiles)

def load_log():
    raw = load_json(LOG_FILE)
    if isinstance(raw, dict) and 'entries' in raw: return raw['entries']
    if isinstance(raw, list): return raw
    return []

def save_log(entries):
    save_json(LOG_FILE, {'entries': entries})

def add_log(entry):
    entries = load_log()
    entries.append(entry)
    save_log(entries)

def load_passwords():
    raw = load_json(PASSWORDS_FILE)
    return raw if isinstance(raw, dict) else {}

def save_passwords(store):
    save_json(PASSWORDS_FILE, store)

# --- Tooltip Helper ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget, self.text = widget, text
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    def show(self, _):
        bbox = self.widget.bbox("insert") or (0,0,0,0)
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + bbox[3] + 10
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        lbl = ttk.Label(self.tw, text=self.text,
                        background="#ffffe0", relief='solid', padding=5)
        lbl.pack()
    def hide(self, _):
        if hasattr(self, 'tw'): self.tw.destroy()

# --- PDF Utilities ---
def generate_index_pdf(filenames):
    tf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    c = canvas.Canvas(tf.name, pagesize=letter)
    w,h = letter
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w/2, h-72, "Contents of Merged PDF")
    c.setLineWidth(1)
    c.line(72, h-78, w-72, h-78)
    c.setFont("Helvetica", 12)
    y = h-108
    for i,fn in enumerate(filenames, 1):
        c.drawString(90, y, f"{i}. {Path(fn).name}")
        y -= 18
        if y < 72:
            c.showPage(); c.setFont("Helvetica", 12); y = h-72
    c.save()
    return tf.name

def make_thumbnail(pdf_path, size=(80,100)):
    doc = fitz.Document(str(pdf_path))
    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.thumbnail(size)
    return ImageTk.PhotoImage(img)

def merge_task(inputs, output, options, progress_cb, cancel_event):
    paths = inputs.copy()
    if options['sort']:    paths.sort(key=lambda p: Path(p).name.lower())
    if options['index']:   paths.insert(0, generate_index_pdf(paths))

    merger = PyPDF2.PdfMerger()
    total = len(paths)
    for i,p in enumerate(paths,1):
        if cancel_event.is_set():
            merger.close(); return False
        merger.append(p)
        progress_cb(i/total*100)
    merger.write(output); merger.close()

    meta_info = {}
    for k in ('title','author','subject','keywords'):
        v = options.get(k)
        if v: meta_info[f'/{k.title()}'] = v

    with pikepdf.open(output, allow_overwriting_input=True) as pdf:
        for key,val in meta_info.items():
            pdf.docinfo[key] = val
        pw = options.get('password')
        if pw:
            R = 6 if options.get('encrypt256') else 4
            pdf.save(output, encryption=pikepdf.Encryption(user=pw, owner=pw, R=R))
        else:
            pdf.save(output)
    return True

# --- Main Application ---
class PDFToolkitApp(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)
        master.title("PDF Toolkit")
        self.pack(fill='both', expand=True)

        # Load saved state
        self.history   = load_history()
        self.profiles  = load_profiles()
        self.passwords = load_passwords()
        self.log       = load_log()
        self.executor  = ThreadPoolExecutor(max_workers=1)
        self.cancel    = threading.Event()

        # Top bar: history, profiles, theme
        bar = ttk.Frame(master); bar.pack(fill='x', pady=5, padx=5)
        ttk.Label(bar, text="Recent:").pack(side='left')
        self.hist_cb = ttk.Combobox(bar, values=self.history, state='readonly')
        self.hist_cb.pack(side='left', fill='x', expand=True, padx=(0,10))
        ToolTip(self.hist_cb, "Select working folder")

        ttk.Label(bar, text="Profile:").pack(side='left')
        self.prof_cb = ttk.Combobox(bar, values=list(self.profiles.keys()), state='readonly')
        self.prof_cb.pack(side='left', padx=(0,10))
        ToolTip(self.prof_cb, "Load settings profile")

        ttk.Button(bar, text="Save Profile", command=self.save_profile).pack(side='left')
        ToolTip(bar, "Save current settings as a profile")

        self.theme_var = tk.StringVar(value='light')
        ttk.Button(bar, text="Toggle Theme", command=self.toggle_theme).pack(side='right')
        ToolTip(bar, "Switch light/dark mode")

        # --- Merge Tab ---
        m = ttk.Frame(self); self.add(m, text="Merge")
        self.tree = ttk.Treeview(m, show='tree'); self.tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.thumbs = {}
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', self.on_drop)

        btns = ttk.Frame(m); btns.pack(fill='x', padx=5)
        for txt, cmd in [("Add PDFs", self.add_pdfs), ("Remove", self.remove), ("Undo", self.undo)]:
            ttk.Button(btns, text=txt, command=cmd).pack(side='left', padx=2)

        of = ttk.Frame(m); of.pack(fill='x', pady=5, padx=5)
        ttk.Label(of, text="Output:").pack(side='left')
        self.out_var = tk.StringVar()
        ttk.Entry(of, textvariable=self.out_var).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(of, text="Browse", command=self.browse_output).pack(side='left')

        opts = ttk.LabelFrame(m, text="Options"); opts.pack(fill='x', padx=5, pady=5)
        self.sort_var  = tk.BooleanVar(); ttk.Checkbutton(opts, text="Sort inputs",   variable=self.sort_var).pack(side='left', padx=5)
        self.index_var = tk.BooleanVar(); ttk.Checkbutton(opts, text="Add index page",variable=self.index_var).pack(side='left')

        meta = ttk.LabelFrame(m, text="Metadata"); meta.pack(fill='x', padx=5, pady=5)
        self.meta_vars = {}
        for f in ("title","author","subject","keywords"):
            v = tk.StringVar(); self.meta_vars[f]=v
            ttk.Label(meta, text=f.title()).pack(side='left')
            ttk.Entry(meta, textvariable=v, width=12).pack(side='left', padx=2)

        enc = ttk.LabelFrame(m, text="Security"); enc.pack(fill='x', padx=5, pady=5)
        self.pw_var = tk.StringVar(); self.enc256 = tk.BooleanVar()
        ttk.Label(enc, text="Password:").pack(side='left')
        ttk.Entry(enc, textvariable=self.pw_var, show="*", width=12).pack(side='left', padx=5)
        ttk.Checkbutton(enc, text="AES-256", variable=self.enc256).pack(side='left')

        pr = ttk.Frame(m); pr.pack(fill='x', padx=5, pady=5)
        self.progress = ttk.Progressbar(pr, mode='determinate'); self.progress.pack(fill='x', side='left', expand=True)
        ttk.Button(pr, text="Cancel", command=self.cancel.set).pack(side='left', padx=5)
        ttk.Button(m, text="Run Merge", command=self.run_merge).pack(pady=5)

        # --- Split & Compress Tabs (placeholders) ---
        for name in ("Split","Compress"):
            f = ttk.Frame(self); self.add(f, text=name)
            ttk.Label(f, text=f"({name} functionality here)").pack(pady=20)

        # --- Unlock Tab ---
        u = ttk.Frame(self); self.add(u, text="Unlock")
        self.unlock_tree = ttk.Treeview(u, show='tree')
        self.unlock_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.unlock_tree.drop_target_register(DND_FILES)
        self.unlock_tree.dnd_bind('<<Drop>>', self.on_drop_unlock)

        uf = ttk.Frame(u); uf.pack(fill='x', padx=5)
        ttk.Button(uf, text="Add PDFs", command=self.add_unlock).pack(side='left', padx=2)
        ttk.Button(uf, text="Remove",   command=self.remove_unlock).pack(side='left', padx=2)

        pf = ttk.LabelFrame(u, text="Password Options"); pf.pack(fill='x', padx=5, pady=5)
        self.use_global_pw = tk.BooleanVar(value=True)
        ttk.Checkbutton(pf, text="Use same password for all", variable=self.use_global_pw).pack(side='left', padx=5)
        self.global_pw_var = tk.StringVar()
        ttk.Entry(pf, textvariable=self.global_pw_var, show="*", width=20).pack(side='left', padx=5)

        self.pw_store_cb = ttk.Combobox(pf, values=list(self.passwords.keys()), state='readonly', width=20)
        self.pw_store_cb.pack(side='left', padx=5)
        ttk.Button(pf, text="Save Password", command=self.save_this_password).pack(side='left')

        ttk.Button(u, text="Run Unlock", command=self.run_unlock).pack(pady=5)

        if self.history:
            self.hist_cb['values'] = self.history
            self.hist_cb.current(0)

    # --- Merge Handlers ---
    def on_drop(self, e):
        for f in self.master.tk.splitlist(e.data):
            if f.lower().endswith('.pdf'): self.insert_pdf(f)

    def insert_pdf(self, p):
        thumb = make_thumbnail(p)
        iid = self.tree.insert('', 'end', text=Path(p).name, image=thumb, values=(p,))
        self.thumbs[iid] = thumb
        self.history = add_to_history(Path(p).parent)
        self.hist_cb['values'] = self.history

    def add_pdfs(self):
        init = self.hist_cb.get() or os.getcwd()
        for p in filedialog.askopenfilenames(initialdir=init, filetypes=[("PDF","*.pdf")]):
            self.insert_pdf(p)

    def remove(self):
        for iid in self.tree.selection(): self.tree.delete(iid)

    def undo(self):
        entries = load_log()
        if not entries:
            return messagebox.showinfo("Undo","Nothing to undo.")
        last = entries.pop(); save_log(entries)
        o = last.get('output')
        if o and Path(o).exists(): Path(o).unlink(); return messagebox.showinfo("Undo",f"Deleted {o}")
        messagebox.showinfo("Undo","Could not delete output.")

    def browse_output(self):
        init = self.hist_cb.get() or os.getcwd()
        p = filedialog.asksaveasfilename(initialdir=init, defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
        if p:
            if not p.lower().endswith('.pdf'): p += '.pdf'
            self.out_var.set(p)
            self.history = add_to_history(Path(p).parent)
            self.hist_cb['values'] = self.history

    def run_merge(self):
        out = self.out_var.get().strip()
        if out and not out.lower().endswith('.pdf'):
            out += '.pdf'; self.out_var.set(out)

        inputs = [self.tree.item(i,'values')[0] for i in self.tree.get_children()]
        if not inputs or not out:
            return messagebox.showerror("Error","Select inputs & output.")

        opts = {
            'sort':      self.sort_var.get(),
            'index':     self.index_var.get(),
            'password':  self.pw_var.get(),
            'encrypt256':self.enc256.get(),
            **{k: v.get() for k,v in self.meta_vars.items()}
        }
        self.cancel.clear(); self.progress['value']=0

        fut = self.executor.submit(merge_task, inputs, out, opts,
                                   lambda v: self.progress.step(v-self.progress['value']),
                                   self.cancel)
        def done(_):
            ok = fut.result()
            if ok:
                messagebox.showinfo("Done",f"Merged ⇒ {out}")
                add_log({'time':datetime.now().isoformat(),'action':'merge','inputs':inputs,'output':out,'options':opts})
            else:
                messagebox.showwarning("Cancelled","Merge cancelled.")
        fut.add_done_callback(lambda f:self.tree.after(0,done,f))

    # --- Unlock Handlers ---
    def on_drop_unlock(self, e):
        for f in self.master.tk.splitlist(e.data):
            if f.lower().endswith('.pdf'):
                self.unlock_tree.insert('', 'end', text=Path(f).name, values=(f,))

    def add_unlock(self):
        init = self.hist_cb.get() or os.getcwd()
        for p in filedialog.askopenfilenames(initialdir=init, filetypes=[("PDF","*.pdf")]):
            self.unlock_tree.insert('', 'end', text=Path(p).name, values=(p,))

    def remove_unlock(self):
        for iid in self.unlock_tree.selection():
            self.unlock_tree.delete(iid)

    def save_this_password(self):
        name = simpledialog.askstring("Label","Enter label for this password:")
        if not name: return
        pw = self.global_pw_var.get()
        if not pw:
            return messagebox.showerror("Error","No password to save.")
        self.passwords[name] = pw
        save_passwords(self.passwords)
        self.pw_store_cb['values'] = list(self.passwords.keys())

    def run_unlock(self):
        items = self.unlock_tree.get_children()
        if not items:
            return messagebox.showerror("Error","No PDFs selected to unlock.")
        out_dir = Path(self.hist_cb.get() or os.getcwd()) / 'unlocked'
        out_dir.mkdir(exist_ok=True)
        pw_map = {}
        global_pw = self.global_pw_var.get() if self.use_global_pw.get() else None
        for iid in items:
            path = self.unlock_tree.item(iid,'values')[0]
            if global_pw:
                pw_map[path] = global_pw
            else:
                pw_map[path] = simpledialog.askstring(f"Password for {Path(path).name}",
                                                      "Enter password:", show="*")
        errors = []
        for path,pw in pw_map.items():
            try:
                pdf = pikepdf.open(path, password=pw)
                out_path = out_dir / (Path(path).stem + '_unlocked.pdf')
                pdf.save(str(out_path)); pdf.close()
            except Exception as e:
                errors.append(f"{Path(path).name}: {e}")
        if errors:
            messagebox.showwarning("Done with errors","\n".join(errors))
        else:
            messagebox.showinfo("Success",f"Unlocked PDFs → {out_dir}")

    # --- Profiles & Theme ---
    def save_profile(self):
        p = filedialog.asksaveasfilename(defaultextension=".json",initialdir=HOME,filetypes=[("JSON","*.json")])
        if not p: return
        prof = {
            'sort': self.sort_var.get(),
            'index':self.index_var.get(),
            'password':self.pw_var.get(),
            'encrypt256':self.enc256.get(),
            **{k:v.get() for k,v in self.meta_vars.items()}
        }
        self.profiles[Path(p).stem]=prof
        save_profiles(self.profiles)
        self.prof_cb['values']=list(self.profiles.keys())

    def toggle_theme(self):
        style = ttk.Style(self)
        if self.theme_var.get()=='light':
            style.theme_use('clam'); self.theme_var.set('dark')
        else:
            style.theme_use('default'); self.theme_var.set('light')

if __name__ == '__main__':
    root = TkinterDnD.Tk()
    app = PDFToolkitApp(root)
    root.mainloop()
